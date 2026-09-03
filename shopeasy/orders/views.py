from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from cart.models import Cart
from store.models import Product
from .models import Order, OrderItem, Coupon


@login_required
def checkout(request):
    buy_now_id = request.GET.get('buy_now') or request.POST.get('buy_now')
    buy_now_product = None
    buy_now_qty = 1

    if buy_now_id:
        buy_now_product = get_object_or_404(Product, id=buy_now_id)
        buy_now_qty = int(request.GET.get('qty') or request.POST.get('qty') or 1)
        if not buy_now_product.in_stock or buy_now_qty > buy_now_product.stock:
            messages.error(request, f"{buy_now_product.name} doesn't have enough stock.")
            return redirect(buy_now_product.get_absolute_url())

        subtotal = buy_now_product.price * buy_now_qty
        display_items = [{'product': buy_now_product, 'quantity': buy_now_qty, 'subtotal': subtotal}]
        cart = None
    else:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('cart:cart_detail')
        subtotal = cart.total
        display_items = cart.items.select_related('product').all()

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        coupon_code = request.POST.get('coupon_code', '').strip()

        context = {'cart': cart, 'display_items': display_items, 'subtotal': subtotal, 'buy_now_product': buy_now_product, 'buy_now_qty': buy_now_qty}

        if not address:
            messages.error(request, "Shipping address is required.")
            return render(request, 'orders/checkout.html', context)

        coupon = None
        discount_amount = 0

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code__iexact=coupon_code)
                if coupon.is_valid():
                    discount_amount = subtotal * coupon.discount_percent / 100
                else:
                    messages.error(request, "Coupon is invalid or expired.")
                    return render(request, 'orders/checkout.html', context)
            except Coupon.DoesNotExist:
                messages.error(request, "Coupon code not found.")
                return render(request, 'orders/checkout.html', context)

        total = subtotal - discount_amount

        try:
            with transaction.atomic():
                if buy_now_product:
                    if buy_now_qty > buy_now_product.stock:
                        raise ValueError(f"Not enough stock for {buy_now_product.name}.")
                else:
                    for item in cart.items.select_related('product'):
                        if item.quantity > item.product.stock:
                            raise ValueError(f"Not enough stock for {item.product.name}.")

                order = Order.objects.create(
                    user=request.user,
                    coupon=coupon,
                    subtotal=subtotal,
                    discount_amount=discount_amount,
                    total=total,
                    shipping_address=address,
                    shipping_city=city,
                    shipping_pincode=pincode,
                )

                if buy_now_product:
                    OrderItem.objects.create(
                        order=order,
                        product=buy_now_product,
                        product_name=buy_now_product.name,
                        price_at_purchase=buy_now_product.price,
                        quantity=buy_now_qty,
                    )
                    buy_now_product.stock -= buy_now_qty
                    buy_now_product.save()
                else:
                    for item in cart.items.select_related('product'):
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            product_name=item.product.name,
                            price_at_purchase=item.product.price,
                            quantity=item.quantity,
                        )
                        item.product.stock -= item.quantity
                        item.product.save()
                    cart.items.all().delete()

                if coupon:
                    coupon.times_used += 1
                    coupon.save()

        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'orders/checkout.html', context)

        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('orders:order_detail', order_id=order.id)

    context = {'cart': cart, 'display_items': display_items, 'subtotal': subtotal, 'buy_now_product': buy_now_product, 'buy_now_qty': buy_now_qty}
    return render(request, 'orders/checkout.html', context)


@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/invoice.html', {'order': order})


@login_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST' and order.status == 'pending':
        with transaction.atomic():
            for item in order.items.select_related('product'):
                if item.product:
                    item.product.stock += item.quantity
                    item.product.save()
            order.status = 'cancelled'
            order.save()
        messages.success(request, f"Order #{order.id} has been cancelled.")
    return redirect('orders:order_detail', order_id=order.id)
