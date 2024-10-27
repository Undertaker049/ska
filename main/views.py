from django.shortcuts import render


# Create your views here.

# Хаб-страница, на которой можно выводить обь явления или вести список изменений. Мной не использовалась
def main(request):
    return render(request, 'main.html')
