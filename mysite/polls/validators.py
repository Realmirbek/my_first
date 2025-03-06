from django.core.exceptions import ValidationError

class PasswordComplexityValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Пароль должен содержать минимум 8 символов.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("Пароль должен содержать хотя бы одну букву.")

    def get_help_text(self):
        return "Пароль должен содержать минимум 8 символов, одну цифру и одну букву."
