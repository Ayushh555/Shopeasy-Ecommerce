from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from .forms import SignUpForm, ProfileForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created. Welcome!')
            return redirect('store:product_list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    orders = request.user.orders.all()
    delivered_orders = orders.filter(status='delivered')

    stats = {
        'total_orders': orders.count(),
        'total_spent': orders.exclude(status='cancelled').aggregate(total=Sum('total'))['total'] or 0,
        'pending_orders': orders.filter(status__in=['pending', 'confirmed', 'shipped']).count(),
        'delivered_orders': delivered_orders.count(),
        'wishlist_count': getattr(request.user, 'wishlist', None) and request.user.wishlist.products.count() or 0,
        'member_since': request.user.date_joined,
    }

    context = {'form': form, 'orders': orders[:5], 'stats': stats}
    return render(request, 'accounts/profile.html', context)
