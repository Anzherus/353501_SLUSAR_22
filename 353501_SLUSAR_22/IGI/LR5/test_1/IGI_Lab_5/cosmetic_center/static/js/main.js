/**
 * Main JavaScript file for cosmetic center website
 * This file contains all the main JavaScript functionality
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initMobileMenu();
    initDropdowns();
    initScrollAnimations();
    initSmoothScrolling();
    initFormValidation();
    initCartFunctionality();
});

/**
 * Mobile menu functionality
 * Handles opening/closing mobile menu and overlay
 */
function initMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    const toggleButton = document.querySelector('.mobile-menu-toggle i');
    
    if (!mobileMenu || !overlay || !toggleButton) return;

    // Close mobile menu when clicking on links
    const mobileMenuLinks = document.querySelectorAll('.mobile-menu a');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', function() {
            closeMobileMenu();
        });
    });
}

/**
 * Toggle mobile menu open/close
 */
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    const toggleButton = document.querySelector('.mobile-menu-toggle i');
    
    if (!mobileMenu || !overlay || !toggleButton) return;
    
    if (mobileMenu.classList.contains('active')) {
        closeMobileMenu();
    } else {
        openMobileMenu();
    }
}

/**
 * Open mobile menu - Improved with animations
 */
function openMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    const toggleButton = document.querySelector('.mobile-menu-toggle i');
    
    if (!mobileMenu || !overlay || !toggleButton) return;
    
    mobileMenu.classList.add('active');
    overlay.classList.add('active');
    toggleButton.classList.remove('fa-bars');
    toggleButton.classList.add('fa-times');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
    
    // Add staggered animation for menu items
    const menuItems = mobileMenu.querySelectorAll('.nav-links a');
    menuItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(20px)';
        
        setTimeout(() => {
            item.style.transition = 'all 0.3s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, index * 50);
    });
}

/**
 * Close mobile menu - Improved with animations
 */
function closeMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    const toggleButton = document.querySelector('.mobile-menu-toggle i');
    
    if (!mobileMenu || !overlay || !toggleButton) return;
    
    // Animate menu items out
    const menuItems = mobileMenu.querySelectorAll('.nav-links a');
    menuItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(20px)';
        }, index * 30);
    });
    
    // Close menu after animation
    setTimeout(() => {
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
        toggleButton.classList.remove('fa-times');
        toggleButton.classList.add('fa-bars');
        document.body.style.overflow = ''; // Restore scrolling
        
        // Reset menu items styles
        menuItems.forEach(item => {
            item.style.transition = '';
            item.style.opacity = '';
            item.style.transform = '';
        });
    }, menuItems.length * 30 + 200);
}

/**
 * Initialize dropdown menus
 * Handles user dropdown and "More" dropdown
 */
function initDropdowns() {
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(event) {
        const userMenu = document.querySelector('.user-menu');
        const userDropdown = document.getElementById('userDropdown');
        const moreDropdown = document.getElementById('moreDropdown');
        const dropdown = document.querySelector('.dropdown');
        
        if (userMenu && !userMenu.contains(event.target)) {
            userDropdown.classList.remove('active');
        }
        
        if (dropdown && !dropdown.contains(event.target)) {
            moreDropdown.classList.remove('active');
        }
    });
}

/**
 * Toggle user dropdown menu
 */
function toggleUserDropdown() {
    const dropdown = document.getElementById('userDropdown');
    if (!dropdown) return;
    
    if (dropdown.classList.contains('active')) {
        dropdown.classList.remove('active');
    } else {
        dropdown.classList.add('active');
    }
}

/**
 * Toggle "More" dropdown menu
 */
function toggleDropdown(event) {
    event.preventDefault();
    const dropdown = document.getElementById('moreDropdown');
    if (!dropdown) return;
    
    if (dropdown.classList.contains('active')) {
        dropdown.classList.remove('active');
    } else {
        dropdown.classList.add('active');
    }
}

/**
 * Initialize scroll animations
 * Animates elements when they come into view
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Apply animation to cards and other elements
    const animatedElements = document.querySelectorAll('.card, .fade-in');
    animatedElements.forEach(element => {
        element.classList.add('fade-in');
        observer.observe(element);
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize form validation
 * Adds client-side validation to forms
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form:not([data-skip-validation])');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Validate form fields
 * @param {HTMLFormElement} form - Form element to validate
 * @returns {boolean} - True if form is valid
 */
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
        
        // Email validation
        if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                showFieldError(field, 'Please enter a valid email address');
                isValid = false;
            }
        }
        
        // Phone validation
        if (field.type === 'tel' && field.value) {
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            if (!phoneRegex.test(field.value.replace(/\s/g, ''))) {
                showFieldError(field, 'Please enter a valid phone number');
                isValid = false;
            }
        }
    });
    
    return isValid;
}

/**
 * Show field error message
 * @param {HTMLElement} field - Field element
 * @param {string} message - Error message
 */
function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.style.color = 'var(--danger)';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
    field.classList.add('error');
}

/**
 * Clear field error message
 * @param {HTMLElement} field - Field element
 */
function clearFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    field.classList.remove('error');
}

/**
 * Initialize cart functionality
 * Handles cart operations like add/remove items
 */
function initCartFunctionality() {
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const quantity = this.dataset.quantity || 1;
            addToCart(productId, quantity);
        });
    });
    
    // Update quantity buttons
    const updateQuantityButtons = document.querySelectorAll('.update-quantity');
    updateQuantityButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            const action = this.dataset.action; // 'increase' or 'decrease'
            updateCartQuantity(itemId, action);
        });
    });
    
    // Remove item buttons
    const removeItemButtons = document.querySelectorAll('.remove-item');
    removeItemButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            removeFromCart(itemId);
        });
    });
}

/**
 * Add item to cart
 * @param {string} productId - Product ID
 * @param {number} quantity - Quantity to add
 */
function addToCart(productId, quantity) {
    // This would typically make an AJAX request to the server
    console.log(`Adding product ${productId} with quantity ${quantity} to cart`);
    
    // Show success message
    showNotification('Item added to cart!', 'success');
    
    // Update cart count (if displayed)
    updateCartCount();
}

/**
 * Update cart item quantity
 * @param {string} itemId - Cart item ID
 * @param {string} action - Action to perform ('increase' or 'decrease')
 */
function updateCartQuantity(itemId, action) {
    console.log(`Updating cart item ${itemId} with action ${action}`);
    
    // This would typically make an AJAX request to the server
    showNotification('Cart updated!', 'success');
}

/**
 * Remove item from cart
 * @param {string} itemId - Cart item ID
 */
function removeFromCart(itemId) {
    if (confirm('Are you sure you want to remove this item from your cart?')) {
        console.log(`Removing cart item ${itemId}`);
        
        // This would typically make an AJAX request to the server
        showNotification('Item removed from cart!', 'success');
        updateCartCount();
    }
}

/**
 * Update cart count display
 */
function updateCartCount() {
    const cartCountElements = document.querySelectorAll('.cart-count');
    // This would typically get the actual count from the server
    cartCountElements.forEach(element => {
        const currentCount = parseInt(element.textContent) || 0;
        element.textContent = currentCount + 1;
    });
}

/**
 * Show notification message
 * @param {string} message - Notification message
 * @param {string} type - Notification type ('success', 'error', 'warning', 'info')
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background-color: var(--${type === 'error' ? 'danger' : type});
        color: white;
        border-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

/**
 * Format price for display
 * @param {number} price - Price to format
 * @param {string} currency - Currency code
 * @returns {string} - Formatted price string
 */
function formatPrice(price, currency = 'RUB') {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: currency
    }).format(price);
}

/**
 * Format date for display
 * @param {Date|string} date - Date to format
 * @param {string} locale - Locale code
 * @returns {string} - Formatted date string
 */
function formatDate(date, locale = 'ru-RU') {
    const dateObj = new Date(date);
    return dateObj.toLocaleDateString(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} - Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function to limit function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} - Throttled function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Check if element is in viewport
 * @param {HTMLElement} element - Element to check
 * @returns {boolean} - True if element is in viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/**
 * Lazy load images
 * Load images only when they come into viewport
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

/**
 * Initialize search functionality
 * Handle search input and filtering
 */
function initSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        const debouncedSearch = debounce(function() {
            const query = this.value.toLowerCase();
            const searchableElements = document.querySelectorAll('.searchable');
            
            searchableElements.forEach(element => {
                const text = element.textContent.toLowerCase();
                if (text.includes(query)) {
                    element.style.display = '';
                } else {
                    element.style.display = 'none';
                }
            });
        }, 300);
        
        input.addEventListener('input', debouncedSearch);
    });
}

// Export functions for global use
window.toggleMobileMenu = toggleMobileMenu;
window.closeMobileMenu = closeMobileMenu;
window.toggleUserDropdown = toggleUserDropdown;
window.toggleDropdown = toggleDropdown;
window.showNotification = showNotification;
window.formatPrice = formatPrice;
window.formatDate = formatDate;
