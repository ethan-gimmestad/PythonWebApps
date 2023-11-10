from django.contrib import admin
from django.urls import include, path
from hero.views import AuthorDetailView, HeroListView, HeroView, UserUpdateView, RedirectView
from django.contrib.admin import site

urlpatterns = [
    path(r'admin/', site.urls),
    path('', HeroListView.as_view()),
    path('<int:pk>', HeroView.as_view()),

    # Accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/<int:pk>/',          UserUpdateView.as_view(),  name='user_edit'),

    # Author
    path('',                           RedirectView.as_view(url='author/home')),

    path('author/<int:pk>',            AuthorDetailView.as_view(),  name='author_detail'),


    # Article

]
