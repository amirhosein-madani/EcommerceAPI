from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+989\d{9}$", message="Phone number must be in format +98912xxxxxxx"
)

national_code_validator = RegexValidator(
    regex=r"^\d{10}$", message="National code must contain exactly 10 digits."
)

username_validator = RegexValidator(
    regex=r"^[A-Za-zآ-ی ]+$", message="Only letters are allowed."
)
