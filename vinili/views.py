from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from .models import *
from .forms import VinileForm, RegistroForm

#home

def home(request):
    query = request.GET.get('q')
    
    tutti_i_vinili = Vinile.objects.all()

    if query:
        selezione = Vinile.objects.filter(
            Q(titolo__icontains=query) | Q(autore__icontains=query)
        )
        trending = None
    else:
        trending = Vinile.objects.filter(is_trending=True)
        selezione = Vinile.objects.filter(is_selection=True)
        if not selezione.exists():
            selezione = Vinile.objects.all()

    return render(request, 'vinili/home.html', {
        'selezione': selezione,
        'trending': trending,
        'query': query,
        'tutti_i_vinili': tutti_i_vinili,
    })

#dettaglio

def dettaglio(request, id):
    vinile = get_object_or_404(Vinile, id=id)
    return render(request, 'vinili/dettaglio.html', {'vinile': vinile})


#carrello

@login_required
def carrello(request):
    """Visualizza gli elementi nel carrello dell'utente loggato"""
    elementi_carrello = Carrello.objects.filter(utente=request.user).select_related('vinile')

    totale = sum(item.vinile.prezzo * item.qta for item in elementi_carrello)

    return render(request, 'carrello/carrello.html', {
        'elementi': elementi_carrello,
        'totale': totale
    })

@login_required
def aggiungi_carrello(request, vinile_id):
    """Aggiunge un vinile al carrello o ne aumenta la quantità"""
    vinile = get_object_or_404(Vinile, id=vinile_id)
    
    item, created = Carrello.objects.get_or_create(
        utente=request.user,
        vinile=vinile,
        defaults={'qta': 1}
    )
    
    if not created:
        item.qta += 1
        item.save()
    
    messages.success(request, f"{vinile.titolo} aggiunto al carrello!")
    return redirect('carrello')

@login_required
def rimuovi_carrello(request, item_id):
    item = get_object_or_404(Carrello, id=item_id, utente=request.user)
    item.delete()
    messages.success(request, "Vinile rimosso dal carrello.")
    return redirect('carrello')

#wishlist

@login_required
def wishlist(request):
    """Visualizza i desiderati tramite la tabella DesideratoIn"""
    desiderati = DesideratoIn.objects.filter(wishlist__utente=request.user).select_related('vinile')

    return render(request, 'wishlist/wishlist.html', {
        'wishlist_items': desiderati,
    })

@login_required
def aggiungi_wishlist(request, vinile_id):
    """Aggiunge un vinile alla wishlist predefinita dell'utente"""
    vinile_obj = get_object_or_404(Vinile, id=vinile_id)
    
    wish, created = Wishlist.objects.get_or_create(
        utente=request.user,
        nome_wishlist="I miei desideri"
    )
    
    DesideratoIn.objects.get_or_create(vinile=vinile_obj, wishlist=wish)
    
    messages.success(request, f"{vinile_obj.titolo} aggiunto alla wishlist!")
    return redirect('wishlist')

@login_required
def rimuovi_wishlist(request, desiderato_id):
    item = get_object_or_404(DesideratoIn, id=desiderato_id, wishlist__utente=request.user)
    item.delete()
    messages.success(request, "Vinile rimosso dai desideri.")
    return redirect('wishlist')

#profilo

@login_required
def profilo(request):
    collezione = Possiede.objects.filter(utente=request.user).select_related('vinile')

    carrello_items = Carrello.objects.filter(utente=request.user).select_related('vinile')

    wishlist_items = DesideratoIn.objects.filter(wishlist__utente=request.user).select_related('vinile')

    return render(request, 'registration/profile.html', {
        'collezione': collezione,
        'carrello_items': carrello_items,
        'wishlist_items': wishlist_items,
    })



@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    f_vinile = VinileForm()
    if request.method == 'POST':
        if 'btn_vinile' in request.POST:
            f_vinile = VinileForm(request.POST, request.FILES)
            if f_vinile.is_valid():
                f_vinile.save()
                messages.success(request, 'Vinile aggiunto con successo!')
                return redirect('dashboard')
            
    context = {
        'vinili' : Vinile.objects.all(),
        'f_vinile' : f_vinile,
    }
    return render(request, 'vinili/dashboard.html', context)

#autenticazione

def registrazione(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Benvenuto {user.username}!')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registration/register.html', {'form': form})