from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import (
    phone_validator,
    username_validator,
    national_code_validator,
)


# post_save   post_delete pre_save pre_delete4
class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        phone_number,
        national_code,
        password=None,
    ):
        """
        Creates and saves a regular user.
        """

        if not username:
            raise ValueError("Users must have a username.")

        if not phone_number:
            raise ValueError("Users must have a phone number.")

        if not national_code:
            raise ValueError("Users must have a national code.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
            national_code=national_code,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        phone_number,
        national_code,
        password,
        email=None,
    ):
        """
        Creates and saves a superuser.
        """

        user = self.create_user(
            email=email,
            username=username,
            phone_number=phone_number,
            national_code=national_code,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom user model
    """

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )
    username = models.CharField(
        max_length=50, unique=True, validators=[username_validator]
    )
    national_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[national_code_validator],
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[phone_validator],
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number", "national_code"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(
        upload_to="profile_Pictures", blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
