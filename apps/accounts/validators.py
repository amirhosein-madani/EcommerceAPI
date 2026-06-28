from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

phone_validator = RegexValidator(
    regex=r"^\+989\d{9}$", message="Phone number must be in format +989xxxxxxxxx"
)


def validate_national_code(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("National code must contain exactly 10 digits.")

    if len(set(value)) == 1:
        raise ValidationError("Invalid national code.")

    check = int(value[-1])
    digits = [int(d) for d in value[:9]]
    total = sum(d * (10 - i) for i, d in enumerate(digits))
    remainder = total % 11

    if remainder < 2:
        valid = check == remainder
    else:
        valid = check == 11 - remainder

    if not valid:
        raise ValidationError("Invalid national code.")


username_validator = RegexValidator(
    regex=r"^[A-Za-zآ-ی ]+$", message="Only letters are allowed."
)
