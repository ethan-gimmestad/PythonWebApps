# superheroes/mixins.py

from django.contrib.auth.mixins import LoginRequiredMixin

class AuthorRequiredMixin(LoginRequiredMixin):
    def test_func(self):
        return self.get_object().author == self.request.user
