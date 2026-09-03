from .models import Cart


def cart_summary(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return {'cart_item_count': cart.total_items}
    return {'cart_item_count': 0}
