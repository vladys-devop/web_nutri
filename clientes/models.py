from django.conf import settings

from django.db import models
from datetime import *
from django.db.models import Max
from django.core.validators import MaxValueValidator,MinValueValidator

class Cliente(models.Model):
    class Sexo(models.TextChoices):
        MUJER = "M", "Mujer",
        HOMBRE = "H", "Hombre",
        OTRO = "O", "Otro"

    nutricionista = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="clientes",
    )
    
    # DATOS CLIENTE
    nombre=models.CharField("Nom", max_length=50)
    apellidos=models.CharField("Cognoms", max_length=50)
    sexo=models.CharField("Sexe", max_length= 1,choices=Sexo.choices)
    fecha_nacimiento=models.DateField("Data de naixement")
    telefono=models.CharField("Telèfon",max_length=30,blank=True)
    email=models.EmailField("Correu electrònic",blank=True)

    # PROTECCIÓN DE DATOS

    activo=models.BooleanField("Actiu", default=True)
    consentimieto_rgpd=models.BooleanField("Consentiment RGPD signat",default=False)
    fecha_consentimiento=models.DateField("Data del consentiment",null=True,blank=True)

    # CONTROL
    creado=models.DateTimeField(auto_now_add=True)
    actualizado=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["apellidos","nombre"]
        verbose_name="client"
        verbose_name_plural="clients"

    def __str__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"

    @property
    def edad(self):
        return self.edad_en(date.today())

    def edad_en(self,fecha):
        n=self.fecha_nacimiento
        return fecha.year - n.year - ((fecha.month, fecha.day) < (n.month , n.day))


class Visita(models.Model):
    class Tipo(models.TextChoices):
        PRIMERA="P", "Primera visita"
        SEGUIMIENTO="S","Vista de seguiment"

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="visitas"
    )

    tipo=models.CharField("Tipus", max_length=1,choices=Tipo.choices)
    numero=models.PositiveSmallIntegerField("Número de de sessió",editable=False)
    fecha=models.DateField("Data de la visita",default=date.today)
    proxima_visita=models.DateField("Propera visita",null=True,blank=True)

    class Meta:
        ordering=["-numero"]
        verbose_name="visita"
        verbose_name_plural="visites"
        constraints=[
            models.UniqueConstraint(                 # ---> Que no haya dos visitas iguales
                fields=["cliente","numero"],
                name="numero_visita_unico_cliente"
            ),
        ]

    def __str__(self):
        return f"{self.cliente} - Sessió:{self.numero} ({self.fecha:%d/%m/%Y})"

    def save(self,*args,**kwargs):
        if self.pk is None:
            ultimo = self.cliente.visitas.aggregate(Max("numero"))["numero__max"]
            self.numero = (ultimo or 0) + 1 
        super().save(*args,**kwargs)

    @property
    def edad_cliente(self):
        return self.cliente.edad_en(self.fecha)

    @property
    def visitga_anterior(self):
        return(
            self.cliente.visitas
            .filter(numero__lt=self.numero)
            .order_by("-numero")
            .first()
        )

class Tabaco(models.TextChoices):
    NO="no","No"
    OCASIONAL="ocasional","Sí, ocasionalment"
    DIARIO="diario","Sí,diàriament"

class Alcohol(models.TextChoices):
    NO="no","No"
    OCASIONAL="ocasional","Ocasionalment"
    SEMANAL="semanal","Setmanalment"
    DIARIO="diario","Diàriament"

class HabitoDeposicional(models.TextChoices):
    REGULAR="regular","Regular"
    ESTRENIMIENTO="estrenimiento","Restrenyiment"
    DIARREA="diarrea","Diarrea"
    IRREGULAR="irregular","Irregular"

class HorasSueno(models.TextChoices):
    MENOS_6="<6","<6"
    ENTRE_6_8="6-8","6-8"
    MAS_8=">8",">8"

class CalidadSueno(models.TextChoices):
    BUENA="buena","Bona"
    REGULAR="regular","Regular"
    MALA="mala","Dolenta"

class CicloMenstrual(models.TextChoices):
    REGULAR="regular","Regular"
    IRREGUALR="irregular","Irregular"
    ABUNDANTE="abundante","Abundant"
    ESCASO="escaso","Escàs"
    NO_APLICA="no_aplica","No aplica"

class DetallePrimeraVisita(models.Model):
    visita = models.OneToOneField(
        Visita,
        on_delete=models.CASCADE,
        related_name="detalle_primera"
    )

    # MOTIVO DE LA CONSULTA
    motivo_principal = models.TextField(
        "Motiu principal",blank=True,
        help_text="Què t'ha portat a la consulta?",
    )

    tiempo_problema=models.TextField("Quant de temps amb el problema?", max_length=200,blank=True)
    intentos_previos=models.TextField(
        "Ha fet alguna cosa abans per solucionar-ho?", blank=True,
        help_text="Dieta? Va funcionar?",
    )

    expectativas=models.TextField("Què espera aconseguir? Expectatives", blank=True)
    preocupacion_actual=models.TextField("Què li preocupa més ara mateix?", blank=True)

    # HISTORIAL MÉDICO Y ANTECEDENTES

    patologias=models.TextField("Patologies diagnosticades",blank=True)
    alergias=models.TextField("Al·lèrgies o intoleràncies",blank=True)
    antecedentes_familiares=models.TextField("Antecedents familiars",blank=True)
    analitica_reciente=models.TextField("Analítica recent",blank=True)

    # HABITOS TOXICOS

    tabaco=models.CharField("Tabac",max_length=200,choices=Tabaco.choices, blank=True)
    alcohol=models.CharField("Alcohol",max_length=200,choices=Alcohol.choices,blank=True)
    medicacion=models.TextField(
        "Medicació actual", blank=True,
        help_text="Nom, dosi, horari",
    )

    suplementacion=models.TextField(
        "Suplementació",blank=True,
        help_text="Tipus, dosi y freqüència, motiu pel qual ho pren, efecte percebut",
        )

    # OTROS ASPECTOS DE LA SALUD

    habito_deposicional=models.CharField(
        "Hàbit deposicional",max_length=20,
        choices=HabitoDeposicional.choices,blank=True
    )

    frequencia_deposicional=models.CharField("Freqüència deposicional",max_length=100,blank=True)

    horas_sueno=models.CharField(
        "Hores de son", max_length=10,
        choices=HorasSueno.choices,blank=True,
    )

    calidad_sueno=models.CharField(
        "Qualitat del son",max_length=20,
        choices=CalidadSueno.choices,blank=True,
        help_text="Descansa bé?",
    )

    estres=models.PositiveSmallIntegerField(
        "Estrès percebut (1-10)",null=True,blank=True,
        validators=[MinValueValidator(1),MaxValueValidator(10)],
    )

    ciclo_menstrual=models.CharField(
        "Cicle menstrual",max_length=20,
        choices=CicloMenstrual.choices,blank=True,
    )

    class Meta:
        verbose_name="detall de primera visita"
        verbose_name_plural="detalls de primera visita"

    def __str__(self):
        return f"Primera visita - {self.visita.cliente}"