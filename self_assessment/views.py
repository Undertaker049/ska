from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def main(request):
    test = {'info': 'Hi there!'}
    data = {'test': test}
    return render(request, 'self_assessment.html', data)
