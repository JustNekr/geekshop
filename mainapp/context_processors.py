from basketapp.models import Basket


def basket(request):
    basket_list = []
    if request.user.is_authenticated:
        users_basket = Basket(user=request.user)
        basket_list = users_basket.get_items_cached
#        basket_list = basket.get_items(request.user).select_related()
#        basket_list = Basket.objects.filter(user=request.user).select_related()
    return {
        'basket': basket_list
    }
