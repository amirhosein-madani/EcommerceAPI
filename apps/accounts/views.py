from django.shortcuts import render, redirect
from django.http import HttpResponse

# from  django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_page
from time import sleep
import requests
from .forms import LoginForm
from .tasks import send_email

# Create your views here.


def user_login(request):

    if request.user.is_authenticated:

        return redirect("post_list")

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect("post_list")

            else:

                form.add_error(None, "username or password is incorrect")

    return render(request, "login.html", context={"form": form})


def user_logout(request):
    logout(request)


def sent_email(request):
    send_email.delay()
    return HttpResponse("Email sent successfully!")


def test_cache(request):
    sleep(5)
    return HttpResponse("this is a cache test")


@cache_page(60)
def test_cahing(request):
    response = requests.get("http://localhost:8000/accounts/test-cache/")
    return HttpResponse(response.text)
