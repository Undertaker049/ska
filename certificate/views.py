from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from .forms import *


# Create your views here.

def main(request):
    if request.method == 'GET':
        return render(request, "certificate.html", {"form": CertificateForm()})
    elif request.method == 'POST':
        print(request.FILES["certificate"])
        return redirect('/')
