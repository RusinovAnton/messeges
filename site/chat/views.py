from django.http import HttpResponse


def index(request):
    print(type(request.user))  
    return HttpResponse("Hello, world. You're at the chat index.")
