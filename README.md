# 🛍️ Shopeasy – Django E-Commerce Website

**Shopeasy** is a full-stack e-commerce web application built with **Python and Django**. It provides a simple and user-friendly platform where customers can browse products, add items to their cart, place orders, and manage their accounts.

> 🚧 **Project Status:** Under Development

---

## ✨ Features

### 👤 User Authentication

* User registration
* User login and logout
* Account management
* Secure authentication using Django

### 🛒 Shopping Cart

* Add products to cart
* Update product quantity
* Remove products from cart
* View cart summary
* Calculate total price

### 📦 Products

* Browse available products
* Product details
* Product images
* Product categories
* Product pricing

### 📋 Orders

* Place orders
* View order information
* Track order details

### 🔐 Admin Panel

* Manage products
* Manage users
* Manage orders
* Manage application data through Django Admin

---

## 🛠️ Technologies Used

| Technology      | Purpose               |
| --------------- | --------------------- |
| 🐍 Python       | Backend programming   |
| 🎯 Django       | Web framework         |
| 🌐 HTML         | Website structure     |
| 🎨 CSS          | Website styling       |
| ⚡ JavaScript    | Frontend interactions |
| 🗄️ SQLite      | Development database  |
| 🔧 Git & GitHub | Version control       |

---

## 📁 Project Structure

```text
Shopeasy-Ecommerce/
│
└── shopeasy/
    │
    ├── accounts/          # User authentication
    ├── cart/              # Shopping cart functionality
    ├── ecommerce/         # Main project configuration
    ├── orders/            # Order management
    ├── store/             # Product and store functionality
    ├── static/            # CSS, JavaScript and static files
    ├── templates/         # HTML templates
    ├── media/             # Product images
    │
    ├── manage.py
    ├── requirements.txt
    └── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ayushh555/Shopeasy-Ecommerce.git
```

### 2. Navigate to the project

```bash
cd Shopeasy-Ecommerce
cd shopeasy
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create an admin account

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

---

## 🔑 Admin Panel

After creating a superuser, you can access the Django administration panel at:

```text
http://127.0.0.1:8000/admin/
```

From there, you can manage the application's data.

---

## 🚀 Future Improvements

The project is currently under development. Planned improvements include:

* 💳 Payment gateway integration
* 🔎 Advanced product search
* 🏷️ Product filtering and sorting
* ❤️ Wishlist functionality
* 📧 Order confirmation emails
* ⭐ Product reviews and ratings
* 📱 Improved responsive design
* 📊 Enhanced admin dashboard
* 🚚 Order status tracking

---

## 🎯 Project Goal

The goal of **Shopeasy** is to build a practical and scalable e-commerce platform using Django while implementing real-world concepts such as authentication, product management, shopping carts, and order processing.

---

## 👨‍💻 Developer

**Ayush Chandel**

GitHub: [@Ayushh555](https://github.com/Ayushh555)

---

## 📌 Project Status

🚧 **Currently under development**

New features and improvements will be added regularly as development continues.

---

⭐ **If you find this project interesting, consider giving the repository a star!**
