from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('index')

# Create your views here.
def index(request):
    return render(request,"core/index.html")
def about(request):
    return render(request,"core/about.html")
