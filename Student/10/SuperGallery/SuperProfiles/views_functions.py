from django.contrib.auth.mixins import AccessMixin
from .models import Hero, Article
from django.shortcuts import get_object_or_404
from markdown import markdown

class IsHeroCreatorMixin(AccessMixin):
    def test_func(self):
        hero = get_object_or_404(Hero, pk = self.kwargs["pk"])
        return self.request.user == hero.reporter.user

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
class IsArticleCreatorMixin(AccessMixin):
    def test_func(self):
        article = get_object_or_404(Article, pk = self.kwargs["pk"])
        return self.request.user == article.reporter.user

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

def document_card(document):
    d = f'documents/{document}'
    if not d.endswith('.md'):
        d = d + '.md'
    markdown_text = open(d).read()
    return dict(body=markdown(markdown_text), file=document, color='bg-primary text-light p-5', width='')

def card_data(title=None, body=None, link=None, imagePath=None, tagline=None, realName=None, strength1=None, strength2=None, strength3=None, weakness1=None, weakness2=None, weakness3=None):
    return dict(title=title, header=title, body=body, link=link, imagePath=imagePath, tagline=tagline, realName=realName, strength1=strength1, strength2=strength2, strength3=strength3, weakness1=weakness1, weakness2=weakness2, weakness3=weakness3)