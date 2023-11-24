from django.urls import path
from django.contrib import admin
from django.urls import path, include
from superheroes.views import SuperheroListView, SuperheroDetailView, SuperheroCreateView, SuperheroUpdateView, SuperheroDeleteView, UserLoginView, UserLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('superheroes.urls')),
    path('', SuperheroListView.as_view(), name='superhero_list'),
    path('superhero/<int:pk>/', SuperheroDetailView.as_view(), name='superhero_detail'),
    path('superhero/add/', SuperheroCreateView.as_view(), name='superhero_create'),
    path('superhero/<int:pk>/edit/', SuperheroUpdateView.as_view(), name='superhero_update'),
    path('superhero/<int:pk>/delete/', SuperheroDeleteView.as_view(), name='superhero_delete'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]

