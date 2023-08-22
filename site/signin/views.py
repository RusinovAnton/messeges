from django.shortcuts import render

def signin(request):
		user = request.POST.get('username')
		return render(request, "signin.html")
