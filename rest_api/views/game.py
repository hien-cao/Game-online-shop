from django.http import HttpResponse
from django.views import View
import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ..models import Game

class GameView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GameView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            body = json.loads(request.body)
            g = Game.objects.get(pk=body['id'])
            return HttpResponse(g)
        except:
            return HttpResponse('404')
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            g = Game.objects.get(pk=body['id'])
            for key, value in body.items():
                if key != 'id':
                    setattr(g, key, value)
            g.save()
            return HttpResponse(g)
        except:
            return HttpResponse('404')

    def put(self, request):
        try:
            body = json.loads(request.body)
            g = Game(
                name=body['name'],
                url=body['url'],
                price=body['price']
            )
            g.save()
            return HttpResponse('put')
        except:
            return HttpResponse('404')  
    
    def delete(self, request):
        try:
            body = json.loads(request.body)
            g = Game.objects.get(pk=body['id'])
            print(g.developer)
            # g.delete()
            return HttpResponse('delete')
        except:
            return HttpResponse('404')
