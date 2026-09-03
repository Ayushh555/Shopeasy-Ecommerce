// ============ Toast Notifications ============
function showToast(msg, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = msg;
    container.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = getCookie('csrftoken');

    // ============ Scroll reveal animations ============
    const revealEls = document.querySelectorAll('.reveal');
    if (revealEls.length && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        revealEls.forEach(el => observer.observe(el));
    } else {
        revealEls.forEach(el => el.classList.add('in-view'));
    }

    // ============ Smooth scroll for anchor links ============
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ============ Hero parallax on scroll ============
    const heroVisual = document.querySelector('.hero-visual');
    const heroBlob = document.querySelector('.hero-blob');
    if (heroVisual && heroBlob) {
        window.addEventListener('scroll', function () {
            const scrolled = window.scrollY;
            if (scrolled < 500) {
                heroVisual.style.transform = `translateY(${scrolled * 0.15}px)`;
                heroBlob.style.opacity = Math.max(0, 1 - scrolled / 400);
            }
        }, { passive: true });
    }

    // ============ Back-to-top button ============
    const backToTop = document.createElement('button');
    backToTop.id = 'back-to-top';
    backToTop.innerHTML = '↑';
    backToTop.setAttribute('aria-label', 'Back to top');
    document.body.appendChild(backToTop);

    window.addEventListener('scroll', function () {
        if (window.scrollY > 400) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    }, { passive: true });

    backToTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ============ Auto-hide flash messages ============
    document.querySelectorAll('.message').forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.4s';
            msg.style.opacity = '0';
            setTimeout(function () { msg.remove(); }, 400);
        }, 4000);
    });

    // ============ Quantity stepper ============
    document.querySelectorAll('.qty-input').forEach(function (input) {
        const minus = input.parentElement.querySelector('.qty-minus');
        const plus = input.parentElement.querySelector('.qty-plus');
        if (minus) minus.addEventListener('click', function () {
            input.value = Math.max(1, parseInt(input.value || 1) - 1);
        });
        if (plus) plus.addEventListener('click', function () {
            input.value = parseInt(input.value || 1) + 1;
        });
    });

    // ============ AJAX Add to Cart (quick-add buttons on product grid) ============
    document.querySelectorAll('.quick-add-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            const productId = btn.dataset.productId;
            btn.disabled = true;
            const originalText = btn.textContent;
            btn.textContent = '...';

            fetch(`/cart/add/${productId}/ajax/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: new URLSearchParams({ quantity: 1 }),
            })
                .then(res => res.json())
                .then(data => {
                    btn.disabled = false;
                    if (data.ok) {
                        btn.textContent = '✓ Added';
                        showToast(data.message, 'success');
                        const cartCountEl = document.getElementById('cart-count');
                        if (cartCountEl) cartCountEl.textContent = `(${data.cart_item_count})`;
                        setTimeout(() => { btn.textContent = originalText; }, 1200);
                    } else {
                        btn.textContent = originalText;
                        showToast(data.error || 'Could not add to cart.', 'error');
                    }
                })
                .catch(() => {
                    btn.disabled = false;
                    btn.textContent = originalText;
                    showToast('Something went wrong.', 'error');
                });
        });
    });

    // ============ AJAX Wishlist toggle (quick-wish buttons on product grid) ============
    document.querySelectorAll('.quick-wish-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            const productId = btn.dataset.productId;

            fetch(`/cart/wishlist/toggle/${productId}/ajax/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
            })
                .then(res => res.json())
                .then(data => {
                    if (data.ok) {
                        btn.textContent = data.added ? '♥' : '♡';
                        btn.classList.toggle('active', data.added);
                        showToast(data.added ? 'Added to wishlist' : 'Removed from wishlist', 'info');
                    }
                });
        });
    });

    // ============ Product detail page: AJAX add to cart ============
    const detailAddBtn = document.getElementById('detail-add-cart-btn');
    if (detailAddBtn) {
        detailAddBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const productId = detailAddBtn.dataset.productId;
            const qtyInput = document.querySelector('.qty-input');
            const quantity = qtyInput ? qtyInput.value : 1;

            fetch(`/cart/add/${productId}/ajax/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: new URLSearchParams({ quantity }),
            })
                .then(res => res.json())
                .then(data => {
                    if (data.ok) {
                        showToast(data.message, 'success');
                        const cartCountEl = document.getElementById('cart-count');
                        if (cartCountEl) cartCountEl.textContent = `(${data.cart_item_count})`;
                    } else {
                        showToast(data.error || 'Could not add to cart.', 'error');
                    }
                });
        });
    }

    // ============ Buy Now button (product detail page) ============
    const buyNowBtn = document.getElementById('buy-now-btn');
    if (buyNowBtn) {
        buyNowBtn.addEventListener('click', function (e) {
            e.preventDefault();
            if (buyNowBtn.classList.contains('disabled')) return;
            const productId = buyNowBtn.dataset.productId;
            const checkoutUrl = buyNowBtn.dataset.checkoutUrl;
            const qtyInput = document.getElementById('buy-qty-input');
            const quantity = qtyInput ? qtyInput.value : 1;
            window.location.href = `${checkoutUrl}?buy_now=${productId}&qty=${quantity}`;
        });
    }

    // ============ Live Search ============
    const searchInput = document.getElementById('live-search-input');
    const suggestionsBox = document.getElementById('search-suggestions');
    let searchTimer = null;

    if (searchInput && suggestionsBox && typeof LIVE_SEARCH_URL !== 'undefined') {
        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimer);
            const query = searchInput.value.trim();
            if (query.length < 2) {
                suggestionsBox.innerHTML = '';
                suggestionsBox.classList.remove('open');
                return;
            }
            searchTimer = setTimeout(() => {
                fetch(`${LIVE_SEARCH_URL}?q=${encodeURIComponent(query)}`)
                    .then(res => res.json())
                    .then(data => {
                        if (!data.results.length) {
                            suggestionsBox.innerHTML = '<div class="suggestion-empty">No matches found</div>';
                        } else {
                            suggestionsBox.innerHTML = data.results.map(p => `
                                <a href="${p.url}" class="suggestion-item">
                                    <span class="suggestion-name">${p.name}</span>
                                    <span class="suggestion-meta">${p.brand || ''} · ₹${p.price}${p.in_stock ? '' : ' · Out of stock'}</span>
                                </a>
                            `).join('');
                        }
                        suggestionsBox.classList.add('open');
                    });
            }, 250);
        });

        document.addEventListener('click', function (e) {
            if (!suggestionsBox.contains(e.target) && e.target !== searchInput) {
                suggestionsBox.classList.remove('open');
            }
        });
    }
});
