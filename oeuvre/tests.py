from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Poesie
from elenizado.models import Evenement
from about.models import Gallerie

class PoesieModelTest(TestCase):

    def setUp(self):
        self.poeme = Poesie.objects.create(
            titre="Test Poeme",
            description="C'est un test.",
            poeme="<p>Ceci est un poème de test.</p>",
            status=True
        )

    def test_poesie_creation(self):
        poeme = Poesie.objects.get(titre="Test Poeme")
        self.assertEqual(poeme.titre, "Test Poeme")
        self.assertTrue(poeme.status)

    def test_str_method(self):
        self.assertEqual(str(self.poeme), "Test Poeme")


class PoemeViewTest(TestCase):

    def setUp(self):
        self.poeme = Poesie.objects.create(
            titre="Poème Test",
            description="Un poème d'intégration.",
            poeme="<p>Voici un poème d'intégration.</p>",
            status=True
        )
        Evenement.objects.create(nom="Event Test", date_add="2024-11-26", status=True)  # Correction ici
        Gallerie.objects.create(title="Gallerie Test", status=True)

    def test_poeme_view(self):
        response = self.client.get(reverse('poeme'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Poème Test")
        self.assertContains(response, "<p>Voici un poème d'intégration.</p>")
        self.assertTemplateUsed(response, 'pages/poesie.html')


class AdminPoemeActionsTest(TestCase):

    def setUp(self):
        self.poeme = Poesie.objects.create(
            titre="Test Poème",
            description="Test Description",
            poeme="<p>Test Poème</p>",
            status=False
        )
        self.user = self._create_admin_user()

    def _create_admin_user(self):
        return User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')

    def test_activate_action(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('admin:oeuvre_poesie_changelist'), {  # Correction ici
            '_selected_action': [str(self.poeme.id)],
            'action': 'activate'
        })
        self.poeme.refresh_from_db()
        self.assertTrue(self.poeme.status)

    def test_desactivate_action(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('admin:oeuvre_poesie_changelist'), {  # Correction ici
            '_selected_action': [str(self.poeme.id)],
            'action': 'desactivate'
        })
        self.poeme.refresh_from_db()
        self.assertFalse(self.poeme.status)
