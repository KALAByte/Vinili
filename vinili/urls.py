from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('vinile/<int:id>/', views.dettaglio, name='dettaglio_vinile'),
    path('registrazione/', views.registrazione, name='register'),
    path('profilo/', views.profilo, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('carrello/', views.carrello, name='carrello'),
    path('aggiungi-al-carrello/<int:vinile_id>/', views.aggiungi_carrello, name='aggiungi_carrello'),
    path('aggiungi-alla-wishlist/<int:vinile_id>/', views.aggiungi_wishlist, name='aggiungi_wishlist'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('rimuovi-dal-carrello/<int:item_id>/', views.rimuovi_carrello, name='rimuovi_carrello'),
    path('rimuovi-dalla-wishlist/<int:desiderato_id>/', views.rimuovi_wishlist, name='rimuovi_wishlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)