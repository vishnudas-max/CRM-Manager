from django.shortcuts import render,redirect

def index(request):
    return render(request, 'index.html')


def start_auth(request):
    
    return redirect('home')