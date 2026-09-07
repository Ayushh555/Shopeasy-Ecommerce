from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Category, Product, Review


def product_list(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True, stock__gt=0)[:4]

    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    sort = request.GET.get('sort', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    in_stock_only = request.GET.get('in_stock', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(brand__icontains=query))
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            min_price = ''
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            max_price = ''
    if in_stock_only:
        products = products.filter(stock__gt=0)
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'featured_products': featured_products,
        'query': query,
        'selected_category': category_slug,
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock_only': in_stock_only,
    }
    return render(request, 'store/product_list.html', context)


def live_search(request):
    """Returns JSON suggestions for search-as-you-type."""
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(brand__icontains=query)
        )[:6]
        results = [
            {
                'name': p.name,
                'brand': p.brand,
                'price': str(p.price),
                'url': p.get_absolute_url(),
                'in_stock': p.in_stock,
            }
            for p in products
        ]
    return JsonResponse({'results': results})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.select_related('user').all()
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    context = {'product': product, 'reviews': reviews, 'user_review': user_review}
    return render(request, 'store/product_detail.html', context)


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        Review.objects.update_or_create(
            product=product, user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, "Review submitted.")
    return redirect('store:product_detail', slug=slug)
