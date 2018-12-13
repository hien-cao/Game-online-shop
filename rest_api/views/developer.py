from django.http import HttpResponse
from django.views import View
import json

from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ..models import Developer

class DeveloperView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeveloperView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            body = json.loads(request.body)
            u = User.objects.get(pk=body['id'])
            return HttpResponse(u.username)
        except:
            return HttpResponse('404')
            
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            u = User.objects.get(pk=body['id'])
            for key, value in body.items():
                if key != 'id':
                    setattr(u, key, value)
            u.save()
            return HttpResponse(u.username)
        except:
            return HttpResponse('404')

    def put(self, request):
        try:
            body = json.loads(request.body)
            u = User.objects.create_user(
                username=body['username'],
                password=body['password'],
                email=body['email']
            )
            d = Developer(user=u)
            d.save()
            return HttpResponse('put')
        except:
            return HttpResponse('404')
    
    def delete(self, request):
        return HttpResponse('delete')
