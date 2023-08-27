from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect

def auth(request):
		if request.user.is_authenticated:
			return HttpResponse()

		username = request.POST.get("username")
		password = request.POST.get("password")

		user = User.objects.filter(username=username).first()
		if user is None:
			user = User.objects.create_user(username=username, password=password)
		else:
			user = authenticate(username=username, password=password)
			if user is None:
				return HttpResponseForbidden()

		login(request, user)
		return redirect('chat')

def logout(request):
	logout(request)
	return redirect('chat')
