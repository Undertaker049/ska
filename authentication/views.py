from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def main(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["login"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/registration")
    elif request.method == "GET":
        return render(request, "auth.html")


def registration(request):
    if request.method == "POST":
        data = request.POST
        user = User.objects.create_user(username=data["username"],
                                        email=data["email"],
                                        password=data["password"],
                                        first_name=data["first-name"],
                                        last_name=data["last-name"])
        user.save()
        return redirect("/auth")
    elif request.method == "GET":
        return render(request, "register.html")
