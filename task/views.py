from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
  # return HttpResponse("This is Home pag!")
  return render(request,"home.html")

def about(request):
  return render(request,"about.html")

def contact(request):
  return render(request,"contact.html")

def appointment(request):
  return render(request, "appointment.html")

def services(request):
  return render(request,'services.html')
