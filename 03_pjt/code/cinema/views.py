from django.shortcuts import render

# Create your views here.
def login(request):
    email = request.GET.get('email')
    pw = request.GET.get('pw')
    check = request.GET.get('check')
    
    context = {
        'email' : email,
        'pw' : pw,
        'check' : check,
    }
    return render(request, 'cinema/login.html', context)

def home(request):
    return render(request, 'cinema/home.html')

def community(request):
    return render(request, 'cinema/community.html')