# tests.py
from django.test import TestCase
from django.urls import reverse
from .models import SiteInfo, SocialCount, Newsletter

class SiteInfoTestCase(TestCase):
    def test_create_site_info(self):
        site = SiteInfo.objects.create(
            email='info@example.com',
            nom='Mon Site',
            telephone=1234567890,
            description='Description du site',
            logo='path/to/logo.png'
        )
        self.assertEqual(site.nom, 'Mon Site')
        self.assertTrue(site.status)

    def test_site_info_str_method(self):
        site = SiteInfo.objects.create(
            email='info@example.com',
            nom='Mon Site',
            telephone=1234567890,
            description='Description du site',
            logo='path/to/logo.png'
        )
        self.assertEqual(str(site), 'Mon Site')

class SocialCountTestCase(TestCase):
    def test_create_social_count(self):
        social = SocialCount.objects.create(
            nom='Facebook',
            lien='https://facebook.com',
            icones='fa-facebook-f'
        )
        self.assertEqual(social.nom, 'Facebook')
        self.assertEqual(social.icones, 'fa-facebook-f')

    def test_social_count_str_method(self):
        social = SocialCount.objects.create(
            nom='Facebook',
            lien='https://facebook.com',
            icones='fa-facebook-f'
        )
        self.assertEqual(str(social), 'Facebook')

class NewsletterTestCase(TestCase):
    def test_create_newsletter(self):
        newsletter = Newsletter.objects.create(email='user@example.com')
        self.assertEqual(newsletter.email, 'user@example.com')
        self.assertTrue(newsletter.status)

    def test_newsletter_str_method(self):
        newsletter = Newsletter.objects.create(email='user@example.com')
        self.assertEqual(str(newsletter), 'user@example.com')

class IntegrationTestCase(TestCase):
    def test_site_info_and_newsletter_integration(self):
        site = SiteInfo.objects.create(
            email='info@site.com',
            nom='Site Test',
            telephone=9876543210,
            description='Test de description',
            logo='path/to/logo.jpg'
        )
        newsletter = Newsletter.objects.create(email='user@newsletter.com')
        
        # Vérifier l'intégration entre SiteInfo et Newsletter
        self.assertEqual(newsletter.email, 'user@newsletter.com')
        self.assertEqual(site.email, 'info@site.com')
        self.assertTrue(Newsletter.objects.filter(email='user@newsletter.com').exists())

class FunctionalTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_site_info_via_view(self):
        response = self.client.post(reverse('create_site_info'), {
            'email': 'info@newsite.com',
            'nom': 'New Site',
            'telephone': 9876543210,
            'description': 'Nouvelle description',
            'logo': 'path/to/logo.png'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Site')

    def test_create_newsletter_via_view(self):
        response = self.client.post(reverse('create_newsletter'), {
            'email': 'user@newsletter.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user@newsletter.com')
