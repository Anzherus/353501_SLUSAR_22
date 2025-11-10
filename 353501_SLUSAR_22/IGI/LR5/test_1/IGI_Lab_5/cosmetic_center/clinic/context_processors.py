from .models import Cart, Banner

def cart_items_count(request):
    """Контекстный процессор для добавления количества товаров в корзине на все страницы"""
    cart_items_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items_count = cart.total_items
        except Cart.DoesNotExist:
            cart_items_count = 0
    return {'cart_items_count': cart_items_count}

def banners(request):
    """Контекстный процессор для добавления баннеров на все страницы"""
    left_banners = Banner.objects.filter(is_active=True, position='left').order_by('order')
    right_banners = Banner.objects.filter(is_active=True, position='right').order_by('order')
    return {
        'left_banners': left_banners,
        'right_banners': right_banners,
    }
