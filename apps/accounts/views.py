from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(
            self.request,
            f"🎉 خوش آمدید {form.get_user().username}، ورود شما با موفقیت انجام شد.",
        )
        return super().form_valid(form)


def logout_user(request):
    logout(request)
    return redirect("website:index")
