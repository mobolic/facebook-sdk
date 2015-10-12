from django.http import HttpResponse


def index(request):
    return HttpResponse('Index')


def post(request, pk):
    return HttpResponse('Post {}'.format(pk))
