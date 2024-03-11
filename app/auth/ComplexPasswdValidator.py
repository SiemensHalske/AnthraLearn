from wtforms import ValidationError


class ComplexPasswordValidator:
    def __call__(self, form, field):
        password = field.data
        # Beispielbedingung: Das Passwort muss mindestens eine Ziffer enthalten
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Das Passwort muss mindestens eine Ziffer enthalten.')
