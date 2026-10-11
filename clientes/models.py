from django.conf import settings

from django.db import models
from datetime import *
from django.db.models import Max

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

    def save(self,*args,**kawrgs):
        if self.pk is None:
            ultimo = self.cliente.visita.aggregate(Max("numero"))["numero_max"]
            self.numero = (ultimo or 0) + 1 
        super().save(*args,**kawrgs)

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


