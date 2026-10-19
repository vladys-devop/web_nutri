from django import forms

from .models import Cliente,DetallePrimeraVisita

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


SECCIONES_PRIMERA_VISITA = [
    ("Motiu de la consulta", [
        "motivo_principal","tiempo_problema","intentos_previos",
        "expectativas","preocupacion_actual"
    ]),
    ("Historial mèdic i antecedents", [
        "patologias","alergias","antecedentes_familiares","analitica_reciente",]),
    
    ("Hàbits tòxics i medicació",[
        "tabaco","alcohol","medicacion","suplementacion",
    ]),
    ("Altres aspectes de la salut",[
        "habito_deposicional","frecuencia_deposicional","horas_sueno",
        "calidad_sueno","estres","ciclo_menstrual",
    ]),
    ("Activitat físivca y estil de vida", [
        "deporte_tipo","deporte_frecuencia","deporte_duracion",
        "deporte_momento","deporte_objetivo","trabajo_tipo","trabajo_horario",
    ]),
    ("Historial de pes", [
        "peso_habitual","variaciones_peso","causas_variacion",
        "observaciones_visuales",
    ]),
]

class PrimeraVisitaForm(forms.ModelForm):
    class Meta:
        model = DetallePrimeraVisita
        exclude = ["visita"]

        def secciones(self):
            return [(titulo,[self[campo]for campo in campos])
                    for titulo, campos in SECCIONES_PRIMERA_VISITA
                    ]
        