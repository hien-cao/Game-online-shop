from django.http import HttpResponse
from django.views import View
import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ..models import Game

@csrf_exempt
def add_game(request):
    try:
        assert request.method == 'POST'
        body = json.loads(request.body)
        g = Game(
            name=body['name'],
            url=body['url'],
            price=body['price']
        )
        g.save()
        return HttpResponse('add game')
    except:
        return HttpResponse('404')

@csrf_exempt
def delete_game(request, id):
    try:
        assert request.method == 'POST'
        g = Game.objects.get(pk=id)
        g.delete()
        return HttpResponse('delete game')
    except:
        return HttpResponse('404')

class GameView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GameView, self).dispatch(request, *args, **kwargs)

    def get(self, request, id):
        try:
            g = Game.objects.get(pk=id)
            print(g.developer)
            return HttpResponse(g)
        except:
            return HttpResponse('404')
    
    def post(self, request, id):
        try:
            body = json.loads(request.body)
            g = Game.objects.get(pk=id)
            for key, value in body.items():
                setattr(g, key, value)
            g.save()
            return HttpResponse(g)
        except:
            return HttpResponse('404')
    
    # def delete(self, request, id):
    #     try:
    #         # body = json.loads(request.body)
    #         g = Game.objects.get(pk=id)
    #         # print(g.developer)
    #         g.delete()
    #         return HttpResponse('delete')
    #     except:
    #         return HttpResponse('404')
