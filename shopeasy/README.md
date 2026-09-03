# ShopEasy — Django E-Commerce Store

Full-stack e-commerce website built with Django 5.2, HTML/CSS/JS, and SQLite.

## Stack
- Backend: Django 5.2 (LTS), SQLite
- Frontend: Django templates + vanilla HTML/CSS/JS
- Apps: `store`, `accounts`, `cart`, `orders`

## Features
- Product catalog with categories, search, filter, sort
- User signup/login/profile (Django auth)
- Cart (add/update/remove), stock validation
- Wishlist (toggle save/unsave)
- Coupons (percentage discount, validity window, usage limits)
- Checkout: atomic transaction, auto stock decrement, coupon discount
- Order history per user
- Reviews & ratings per product
- Full Django admin panel for all models

## Setup

```bash
# create + activate venv
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# install dependencies
pip install -r requirements.txt

# run migrations
python manage.py makemigrations
python manage.py migrate

# create admin account
python manage.py createsuperuser

# run server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the store, `http://127.0.0.1:8000/admin/` for the admin panel.

## Seed sample data (optional)

After `createsuperuser`, add a few products via `/admin/` under **Store → Products** and **Store → Categories**, or write a quick script similar to:

```python
# run via: python manage.py shell < seed.py
from store.models import Category, Product

cat, _ = Category.objects.get_or_create(name="Electronics")
Product.objects.get_or_create(
    name="Sample Product", defaults=dict(
        brand="Demo", category=cat, price=999, stock=10,
        description="A sample product."
    )
)
```

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Product list (search, filter, sort) |
| `/product/<slug>/` | Product detail + reviews |
| `/accounts/signup/` | Register |
| `/accounts/login/` | Login |
| `/accounts/profile/` | Profile + recent orders |
| `/cart/` | View cart |
| `/cart/wishlist/` | Wishlist |
| `/orders/checkout/` | Checkout (address + coupon) |
| `/orders/` | Order history |
| `/admin/` | Django admin panel |

## Models

- **Category, Product, Review** (`store` app)
- **Profile** (`accounts` app, auto-created on user signup)
- **Cart, CartItem, Wishlist** (`cart` app)
- **Coupon, Order, OrderItem** (`orders` app)

## Notes
- Django 5.2 is the LTS release — stable, well-supported, recommended for learning/portfolio projects.
- Product images are optional (`ImageField`); Pillow is required for image uploads.
- To create a coupon, go to `/admin/orders/coupon/` and add a code with valid dates.
