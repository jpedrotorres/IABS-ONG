from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def loginScreen(request):
    return render(request, 'contatos/login.html')

#def index(Request):
#    return HttpResponse("Hello World")
