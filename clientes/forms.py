from django import forms

from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nombre",
            "apellidos",
            "sexo",
            "fecha_nacimiento",
            "telefono",
            "email",
            "consentimiento_rgpd",
            "fecha_consentimiento",
        ]

    widgets = {
        "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}, format="%d/%m/%Y"),
        "fecha_consentimiento": forms.DateInput(attrs={"type": "date"}, format="%d/%m/%Y"),
    }