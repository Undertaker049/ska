from django.shortcuts import render


def main(request):
    return render(request, "employee_evaluation.html")
