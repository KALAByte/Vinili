from django.contrib import admin
from .models import *

#registrazione del Genere
admin.site.register(Genere)

#registrazione del  Formato
admin.site.register(Formato)

#registrazione della Wishlist
admin.site.register(Wishlist)

#registrazione del Possiede
admin.site.register(Possiede)

#registrazione del DesideratoIn
admin.site.register(DesideratoIn)

#registrazione Brano
admin.site.register(Brano)
class BranoInline(admin.TabularInline): # Permette di inserire i brani come righe di una tabella
    model = Brano
    extra = 1 # Mostra una riga vuota pronta da compilare

#registrazione del Vinile
@admin.register(Vinile)
class VinileAdmin(admin.ModelAdmin):
    filter_horizontal = ('generi','formati',) 

    list_display = ('autore', 'titolo', 'prezzo', 'stock', 'disponibile')

    search_fields = ('titolo', 'autore')

    list_filter = ('disponibile', 'condizione', 'generi')

    inlines = [BranoInline] # Inserisce la gestione brani dentro il Vinile