from django.test import TestCase
from django.contrib.auth.models import User
from .models import Reporter, Hero, Article
from django.urls import reverse
from .views_reporter import get_reporter

class ReporterModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.reporter = Reporter.objects.create(user=self.user, realName='Test Reporter', email='test@example.com', bio='Test Bio')

    def test_reporter_str(self):
        self.assertEqual(str(self.reporter), 'testuser')

    def test_reporter_get_absolute_url(self):
        self.assertEqual(self.reporter.get_absolute_url(), '/reporter/1')

    def test_reporter_name_property(self):
        self.assertEqual(self.reporter.realName, 'Test Reporter')

class HeroModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.reporter = Reporter.objects.create(user=self.user, realName='Test Reporter', email='test@example.com', bio='Test Bio')
        self.hero = Hero.objects.create(reporter=self.reporter, title='Test Hero', realName='Test Hero Real Name', strength1='Strength 1', strength2='Strength 2', strength3='Strength 3', weakness1='Weakness 1', weakness2='Weakness 2', weakness3='Weakness 3', imagePath='test_image.jpg')

    def test_hero_str(self):
        self.assertEqual(str(self.hero), '1. Test Hero - Test Hero Real Name')

class ArticleModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.reporter = Reporter.objects.create(user=self.user, realName='Test Reporter', email='test@example.com', bio='Test Bio')
        self.article = Article.objects.create(reporter=self.reporter, title='Test Article', tagline='Test Tagline', body='Test Body', imagePath='test_image.jpg')

    def test_article_str(self):
        self.assertEqual(str(self.article), '1. Test Article - Test Reporter')

class ReporterViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.reporter = Reporter.objects.create(user=self.user, realName='Test Reporter', email='test@example.com', bio='Test Bio')

    def test_reporter_list_view(self):
        response = self.client.get(reverse('reporter_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reporter/list.html')

    def test_reporter_detail_view(self):
        response = self.client.get(reverse('reporter_detail', args=[str(self.reporter.pk)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reporter/detail.html')

    def test_reporter_add_view(self):
        response = self.client.get(reverse('reporter_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/account_add.html')

    def test_reporter_home_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('reporter_home'))
        self.assertEqual(response.status_code, 302) # Should redirect to reporter's profile page

    def test_reporter_home_view_anonymous_user(self):
        response = self.client.get(reverse('reporter_home'))
        self.assertEqual(response.status_code, 302)  # Should redirect to /hero/

class HeroViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.reporter = Reporter.objects.create(user=self.user, realName='Test Reporter', email='test@example.com', bio='Test Bio')
        self.hero = Hero.objects.create(reporter=self.reporter, title='Test Hero', realName='Test Hero Real Name', strength1='Strength 1', strength2='Strength 2', strength3='Strength 3', weakness1='Weakness 1', weakness2='Weakness 2', weakness3='Weakness 3', imagePath='test_image.jpg')

    def test_hero_list_view(self):
        response = self.client.get(reverse('hero_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hero/list.html')

    def test_hero_detail_view(self):
        response = self.client.get(reverse('hero_detail', args=[str(self.hero.pk)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hero/detail.html')

    def test_hero_add_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('hero_add'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_hero_add_view_anonymous_user(self):
        response = self.client.get(reverse('hero_add'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_hero_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('hero_edit', args=[str(self.hero.pk)]))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

class ArticleViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.reporter = Reporter.objects.create(user=self.user, realName='Test Reporter', email='test@example.com', bio='Test Bio')
        self.article = Article.objects.create(reporter=self.reporter, title='Test Article', tagline='Test Tagline', body='Test Body', imagePath='test_image.jpg')

    def test_article_list_view(self):
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article/list.html')

    def test_article_detail_view(self):
        response = self.client.get(reverse('article_detail', args=[str(self.article.pk)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article/detail.html')

    def test_article_add_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('article_add'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_article_add_view_anonymous_user(self):
        response = self.client.get(reverse('article_add'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_article_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('article_edit', args=[str(self.article.pk)]))
        self.assertEqual(response.status_code, 200)
        self.client.logout()