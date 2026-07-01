from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.cache import cache
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .forms import PasswordResetRequestForm
from .tasks import send_reset_password_email

User = get_user_model()
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

def user_logout(request):
    logout(request)
    return redirect("website:index")

class PasswordResetRequestView(FormView):
    template_name = "accounts/reset_password_request.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("request_to_reset_password")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        cache_key = f"password_reset:{email.lower()}"

        if cache.get(cache_key):
            messages.warning(
                self.request,
                "لطفاً دو دقیقه دیگر دوباره تلاش کنید."
            )
            return super().form_valid(form)

        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = self.request.build_absolute_uri(
                reverse(
                    "accounts:password_reset_confirm",
                    kwargs={
                        "uidb64": uid,
                        "token": token,
                    },
                )
            )

            send_reset_password_email.delay(user.email, reset_link , user.username)

        cache.set(
            cache_key,
            True,
            timeout=settings.PASSWORD_RESET_RATE_LIMIT,
        )

        messages.success(
            self.request,
            "اگر حسابی با این ایمیل وجود داشته باشد، لینک بازیابی ارسال خواهد شد.",
        )

        return super().form_valid(form)



