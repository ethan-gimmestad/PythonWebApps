from django.contrib.auth.mixins import AccessMixin
from .models import Hero, Article
from django.shortcuts import get_object_or_404

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