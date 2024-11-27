from django.test import TestCase
from django.urls import reverse
from .models import Publication, Categorie, Commentaire
import json

class PublicationTestCase(TestCase):
    """Tests relatifs aux publications"""

    def setUp(self):
        """Préparer l'environnement de test"""
        # Création d'une catégorie pour les publications
        self.categorie = Categorie.objects.create(
            nom="Catégorie Test",
            description="Description de test"
        )
        # Création d'une publication avec une catégorie associée
        self.publication = Publication.objects.create(
            titre="Test Publication",
            description="<p>Description de test</p>",
            categorie=self.categorie,
            image="path/to/image.jpg"
        )
        # URL de la vue détail de la publication
        self.url_detail = reverse('detail', kwargs={'slug': self.publication.slug})
        # Données de test pour un commentaire
        self.data_commentaire = {
            'id': self.publication.id,
            'nom': "Test User",
            'email': "testuser@example.com",
            'commentaire': "C'est un commentaire de test"
        }

    def test_publication_creation(self):
        """Test la création d'une publication"""
        # Vérifier que la publication a bien été créée
        self.assertEqual(self.publication.titre, "Test Publication")
        self.assertEqual(self.publication.categorie.nom, "Catégorie Test")
        self.assertIsNotNone(self.publication.slug)

    def test_publication_detail_view(self):
        """Test la vue de détail d'une publication"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Publication")
        self.assertContains(response, "Description de test")

    def test_publication_slug(self):
        """Vérifier que le slug est bien généré pour la publication"""
        self.assertTrue(self.publication.slug)

class CommentaireTestCase(TestCase):
    """Tests relatifs aux commentaires"""

    def setUp(self):
        """Préparer l'environnement de test"""
        # Création d'une catégorie pour les publications
        self.categorie = Categorie.objects.create(
            nom="Catégorie Test",
            description="Description de test"
        )
        # Création d'une publication pour tester les commentaires
        self.publication = Publication.objects.create(
            titre="Test Publication",
            description="<p>Description de test</p>",
            categorie=self.categorie,
            image="path/to/image.jpg"
        )

    def test_commentaire_submission(self):
        """Test la soumission d'un commentaire"""
        # Envoi d'un POST avec les données du commentaire
        response = self.client.post(reverse('is_commentaire'), {
            'id': self.publication.id,
            'nom': "Test User",
            'email': "testuser@example.com",
            'commentaire': "C'est un commentaire de test"
        })
        # Vérification du code de réponse
        self.assertEqual(response.status_code, 200)

        # Charger la réponse JSON et vérifier les données
        response_data = json.loads(response.content)
        
        # Vérifier que le commentaire a bien été soumis
        self.assertTrue(response_data.get('success'))
        self.assertEqual(response_data.get('message'), "l'enregistrement a bien été effectué")  # Vérifier la casse

        # Vérification que le commentaire a bien été créé
        commentaire = Commentaire.objects.first()
        self.assertIsNotNone(commentaire)
        self.assertEqual(commentaire.nom, "Test User")
        self.assertEqual(commentaire.commentaire, "C'est un commentaire de test")
        self.assertEqual(commentaire.publication, self.publication)

    def test_invalid_commentaire_submission(self):
        """Test la soumission d'un commentaire invalide (par exemple, sans email)"""
        response = self.client.post(reverse('is_commentaire'), {
            'id': self.publication.id,
            'nom': "Test User",
            'commentaire': "C'est un commentaire de test"
        })
        # Vérification que le commentaire n'a pas été créé
        self.assertEqual(response.status_code, 200)

        # Charger la réponse JSON et vérifier les erreurs
        response_data = json.loads(response.content)
        
        # Vérification que la réponse indique une erreur
        self.assertFalse(response_data.get('success'))
        self.assertEqual(response_data.get('message'), "email incorrect")  # Vérifier la casse
        
        # Vérifier que aucun commentaire n'a été créé
        self.assertEqual(Commentaire.objects.count(), 0)
