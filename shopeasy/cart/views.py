from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from store.models import Product
from .models import Cart, CartItem, Wishlist


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if not product.in_stock:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect(product.get_absolute_url())

    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
    if not created:
        item.quantity += quantity
        item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect('cart:cart_detail')


@login_required
@require_POST
def cart_update(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    return redirect('cart:cart_detail')


@login_required
@require_POST
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('cart:cart_detail')


@login_required
@require_POST
def cart_add_ajax(request, product_id):
    """AJAX version of cart_add — returns JSON instead of redirecting."""
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if not product.in_stock:
        return JsonResponse({'ok': False, 'error': f'{product.name} is out of stock.'}, status=400)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
    if not created:
        item.quantity += quantity
        item.save()

    return JsonResponse({
        'ok': True,
        'message': f'{product.name} added to cart.',
        'cart_item_count': cart.total_items,
    })


@login_required
@require_POST
def wishlist_toggle_ajax(request, product_id):
    """AJAX version of wishlist_toggle — returns JSON with new state."""
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        added = False
    else:
        wishlist.products.add(product)
        added = True
    return JsonResponse({'ok': True, 'added': added})


@login_required
def wishlist_detail(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'cart/wishlist.html', {'wishlist': wishlist})


@login_required
@require_POST
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.info(request, f"{product.name} removed from wishlist.")
    else:
        wishlist.products.add(product)
        messages.success(request, f"{product.name} added to wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))
