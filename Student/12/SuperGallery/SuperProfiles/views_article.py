from pathlib import Path
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .views_functions import IsArticleCreatorMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView

from .models import Article
from .views_reporter import get_reporter
    
class ArticleListView(ListView):
    template_name = 'article/list.html'
    model = Article
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        return {
            'object_list': Article.objects.all()
        }

class ArticleDetailView(DetailView):
    template_name = 'article/detail.html'
    model = Article
    context_object_name = 'article'

class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = "article/add.html"
    model = Article
    fields = '__all__'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.reporter = get_reporter(self.request.user)
        return super().form_valid(form)
    

class ArticleUpdateView(IsArticleCreatorMixin, UpdateView):
    template_name = "article/edit.html"
    model = Article
    fields = '__all__'
    success_url = reverse_lazy('article_list')

class ArticleDeleteView(IsArticleCreatorMixin, DeleteView):
    template_name = 'article/delete.html'
    model = Article
    success_url = reverse_lazy('article_list')