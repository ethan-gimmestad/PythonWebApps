from pathlib import Path
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .views_functions import IsHeroCreatorMixin, card_data, document_card
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView
from django.shortcuts import get_object_or_404

from .models import Hero, Article
from .views_reporter import get_reporter
    
class HeroListView(ListView):
    template_name = 'hero/list.html'
    model = Hero
    context_object_name = 'heroes'

    def get_context_data(self, **kwargs):
        return {
            'object_list': Hero.objects.all()
        }

class HeroCarouselView(TemplateView):
    template_name = 'carousel.html'
    model = Hero

    def get_context_data(self, **kwargs):

        def carousel_data():
            data = []
            for hero in Hero.objects.all():
                data.append(dict(image_url=hero.imagePath, label=hero.title, link="/hero/"+str(hero.pk), active=""))
            if data:
                data[0]["active"] = "active"
            return data
        
        carousel = carousel_data()
        return dict(title='Carousel View', carousel=carousel)

class HeroDetailView(DetailView):
    template_name = 'hero/detail.html'
    model = Hero
    context_object_name = 'hero'

class HeroCreateView(LoginRequiredMixin, CreateView):
    template_name = "hero/add.html"
    model = Hero
    fields = '__all__'
    success_url = reverse_lazy('hero_list')

    def form_valid(self, form):
        form.instance.reporter = get_reporter(self.request.user)
        return super().form_valid(form)
    

class HeroUpdateView(IsHeroCreatorMixin, UpdateView):
    template_name = "hero/edit.html"
    model = Hero
    fields = '__all__'
    success_url = reverse_lazy('hero_list')

class HeroDeleteView(IsHeroCreatorMixin, DeleteView):
    template_name = 'hero/delete.html'
    model = Hero
    success_url = reverse_lazy('hero_list')

class HeroTabsView(TemplateView):
    template_name = 'tabs.html'
    model = Hero
    model2 = Article

    def get_context_data(self, **kwargs):

        hero_pk = self.kwargs.get('pk')
        hero = get_object_or_404(Hero, pk=hero_pk)

        def tabs_data():
            def options(i, tab, selected):
                data = tab
                if selected:
                    data.update(dict(name=f'tab{i}', active='active', show='show', selected='true'))
                else:
                    data.update(dict(name=f'tab{i}', active='', show='', selected='false'))
                return data

            def set_options(tabs):
                return [options(i, tab, i == 0) for i, tab in enumerate(tabs)]

            def profile_card_data():
                card = []
                card.append(card_data(title=hero.title, imagePath=hero.imagePath, realName=hero.realName, strength1=hero.strength1, strength2=hero.strength2, strength3=hero.strength3, weakness1=hero.weakness1, weakness2=hero.weakness2, weakness3=hero.weakness3))
                return card

            def article_cards_data():
                cards = []
                for article in Article.objects.all():
                    if (article.hero == hero):
                        cards.append(card_data(title=article.title, tagline=article.tagline, imagePath=article.imagePath, link="/article/"+str(article.pk)))
                return cards

            def create_pane_1():
                data = card_data(title="Profile", body='This is a display of a **hero profile**')
                data['cards'] = profile_card_data()
                return data

            def create_pane_2():
                data = card_data(title="Articles", body='This is a display of **articles**')
                data['cards'] = article_cards_data()
                return data

            def create_tabs():
                return [
                    create_pane_1(),
                    create_pane_2(),
                ]
            
            return set_options(create_tabs())
        
        tabs = tabs_data()
        return dict(title='Tab View', tabs=tabs)