from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Genere(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Generi" # evita "Generes"

class Formato(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Formati" # evita "Formatos"

class Vinile(models.Model):
    titolo = models.CharField(max_length=255)
    autore = models.CharField(max_length=255)
    anno_pubblicazione = models.IntegerField()
    generi = models.ManyToManyField(Genere) #relazione per più generi
    formati = models.ManyToManyField(Formato) #relazione per più formati
    dimensione = models.CharField(max_length=20, blank=True, null=True)
    velocita = models.CharField(max_length=20) 
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=1)
    disponibile = models.BooleanField(default=True)
    condizione = models.CharField(max_length=50)
    copertina = models.ImageField(upload_to='copertine_vinili/', null=True, blank=True) 
    discogs_id = models.IntegerField(null=True, blank=True)
    is_trending = models.BooleanField(default=False, verbose_name="In Tendenza")
    is_selection = models.BooleanField(default=False, verbose_name="Nostra Selezione")
    descrizione = models.TextField(blank=True, null=True, verbose_name="Descrizione")
    
    class Meta:
        verbose_name_plural = "Vinili" # evita "Viniles"

    def __str__(self):
        return f"{self.autore} - {self.titolo}"

class Carrello(models.Model):
    utente = models.ForeignKey(User, on_delete=models.PROTECT)
    vinile = models.ForeignKey(Vinile, on_delete=models.PROTECT)
    qta = models.IntegerField(
        "Quantità", 
        validators=[MinValueValidator(1, message="La quantità deve essere maggiore di 0")]
    )

    def prezzo_totale_riga(self):
        return self.qta * self.vinile.prezzo
    
    class Meta:
        verbose_name_plural = "Carrelli" # evita "Carrellos"

class Wishlist(models.Model):
    nome_wishlist = models.CharField(max_length=100)
    utente = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Wishlist" # evita "Wishlists"

class Possiede(models.Model):
    utente = models.ForeignKey(User, on_delete=models.PROTECT)
    vinile = models.ForeignKey(Vinile, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Possiedi" # evita "Possiedes"

class DesideratoIn(models.Model):
    vinile = models.ForeignKey(Vinile, on_delete=models.PROTECT)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "DesideratiIn" # evita "DesideratoIns"

class Brano(models.Model):
    vinile = models.ForeignKey(Vinile, on_delete=models.PROTECT, related_name='brani')
    titolo = models.CharField(max_length=255)
    durata = models.CharField(max_length=10, blank=True, null=True, help_text="Formato MM:SS")
    posizione = models.CharField(max_length=5, help_text="Esempio: A1, A2, B1...")

    class Meta:
        verbose_name_plural = "Brani"
        ordering = ['posizione'] # Ordina i brani automaticamente per posizione

    def __str__(self):
        return f"{self.posizione} - {self.titolo}"