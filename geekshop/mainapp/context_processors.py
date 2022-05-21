from basketapp.models import Basket


def basket(request):
    print('context_processors basket works')
    basket = []
    if request.user.is_authenticated:
        return Basket.objects.filter(user=request.user)
    else:
        return {
            'basket': basket,
        }