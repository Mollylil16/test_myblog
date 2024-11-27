from django.test import TestCase
from django.urls import reverse
from .models import Curriculum, Contact, Prestation, Presentation, Gallerie
from django.utils import timezone
import json

# --- Tests unitaires ---

class CurriculumTestCase(TestCase):
    def setUp(self):
        self.curriculum = Curriculum.objects.create(
            photo='path/to/photo.jpg',
            nom='John Doe',
            description='<p>Experienced Developer</p>',
            cv='path/to/cv.pdf'
        )

    def test_curriculum_creation(self):
        """Test la création d'un Curriculum"""
        self.assertEqual(self.curriculum.nom, 'John Doe')
        self.assertTrue(self.curriculum.description)
        self.assertIsNotNone(self.curriculum.cv)

class ContactTestCase(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            nom='Jane Smith',
            email='jane@example.com',
            subject='Request Info',
            telephone=1234567890,
            message='Please send more details.',
        )

    def test_contact_creation(self):
        """Test la création d'un contact"""
        self.assertEqual(self.contact.nom, 'Jane Smith')
        self.assertEqual(self.contact.email, 'jane@example.com')
        self.assertTrue(self.contact.message)

class PrestationTestCase(TestCase):
    def setUp(self):
        self.prestation = Prestation.objects.create(
            titre='Web Development',
            description='Building responsive websites',
            image='path/to/image.jpg'
        )

    def test_prestation_creation(self):
        """Test la création d'une prestation"""
        self.assertEqual(self.prestation.titre, 'Web Development')
        self.assertTrue(self.prestation.description)

class PresentationTestCase(TestCase):
    def setUp(self):
        self.presentation = Presentation.objects.create(
            titre='About Us',
            description='<p>We are a web agency.</p>',
            image='path/to/image.jpg'
        )

    def test_presentation_creation(self):
        """Test la création d'une présentation"""
        self.assertEqual(self.presentation.titre, 'About Us')
        self.assertTrue(self.presentation.description)

class GallerieTestCase(TestCase):
    def setUp(self):
        self.gallerie = Gallerie.objects.create(
            titre='Nature Photography',
            gallerie='path/to/image.jpg'
        )

    def test_gallerie_creation(self):
        """Test la création d'une galerie"""
        self.assertEqual(self.gallerie.titre, 'Nature Photography')
        self.assertTrue(self.gallerie.gallerie)

# --- Tests fonctionnels ---

class CurriculumFormTestCase(TestCase):
    def setUp(self):
        self.url = reverse('curriculum_create')
    
    def test_curriculum_form_submission(self):
        """Test la soumission du formulaire de création de curriculum"""
        response = self.client.post(self.url, {
            'photo': 'path/to/photo.jpg',
            'nom': 'John Doe',
            'description': '<p>Experienced Developer</p>',
            'cv': 'path/to/cv.pdf'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Curriculum créé avec succès')

class ContactFormTestCase(TestCase):
    def setUp(self):
        self.url = reverse('contact_create')
    
    def test_contact_form_submission(self):
        """Test la soumission du formulaire de contact"""
        response = self.client.post(self.url, {
            'nom': 'Jane Smith',
            'email': 'jane@example.com',
            'subject': 'Request Info',
            'telephone': 1234567890,
            'message': 'Please send more details.'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact créé avec succès')

# --- Tests d'intégration ---

class CurriculumViewTestCase(TestCase):
    def setUp(self):
        self.curriculum = Curriculum.objects.create(
            photo='path/to/photo.jpg',
            nom='John Doe',
            description='<p>Experienced Developer</p>',
            cv='path/to/cv.pdf'
        )
        self.url = reverse('curriculum_detail', kwargs={'pk': self.curriculum.pk})

    def test_curriculum_detail_view(self):
        """Test la vue détaillée d'un curriculum"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Experienced Developer')

class ContactViewTestCase(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            nom='Jane Smith',
            email='jane@example.com',
            subject='Request Info',
            telephone=1234567890,
            message='Please send more details.'
        )
        self.url = reverse('contact_detail', kwargs={'pk': self.contact.pk})

    def test_contact_detail_view(self):
        """Test la vue détaillée d'un contact"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Smith')
        self.assertContains(response, 'Request Info')

class PrestationViewTestCase(TestCase):
    def setUp(self):
        self.prestation = Prestation.objects.create(
            titre='Web Development',
            description='Building responsive websites',
            image='path/to/image.jpg'
        )
        self.url = reverse('prestation_detail', kwargs={'pk': self.prestation.pk})

    def test_prestation_detail_view(self):
        """Test la vue détaillée d'une prestation"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Development')
        self.assertContains(response, 'Building responsive websites')

class PresentationViewTestCase(TestCase):
    def setUp(self):
        self.presentation = Presentation.objects.create(
            titre='About Us',
            description='<p>We are a web agency.</p>',
            image='path/to/image.jpg'
        )
        self.url = reverse('presentation_detail', kwargs={'pk': self.presentation.pk})

    def test_presentation_detail_view(self):
        """Test la vue détaillée d'une présentation"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Us')
        self.assertContains(response, 'We are a web agency.')

class GallerieViewTestCase(TestCase):
    def setUp(self):
        self.gallerie = Gallerie.objects.create(
            titre='Nature Photography',
            gallerie='path/to/image.jpg'
        )
        self.url = reverse('gallerie_detail', kwargs={'pk': self.gallerie.pk})

    def test_gallerie_detail_view(self):
        """Test la vue détaillée d'une galerie"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nature Photography')
        self.assertContains(response, 'path/to/image.jpg')
