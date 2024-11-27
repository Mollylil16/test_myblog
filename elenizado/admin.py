from django.contrib import admin
from .import models
from django.utils.safestring import mark_safe

# Custom admin with activate/deactivate actions
class CustomAdmin(admin.ModelAdmin):
    actions = ['activate', 'desactivate']
    list_filter = ('status',)
    list_per_page = 20
    date_hierarchy = "date_add"

    def activate(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, 'La sélection a été activée avec succès.')
    activate.short_description = "Activer les éléments sélectionnés"

    def desactivate(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, 'La sélection a été désactivée avec succès.')
    desactivate.short_description = "Désactiver les éléments sélectionnés"

# Register models with custom admin
class CategorieAdmin(CustomAdmin):
    list_display = ('nom', 'date_add', 'date_update', 'status')   
    search_fields = ('nom',)    
    ordering = ['nom']    
    fieldsets = [
        ("Informations catégorie", {"fields": ["nom", "description"]}),
        ("Statut", {"fields": ["status"]})
    ]

class PublicationAdmin(CustomAdmin):
    list_display = ('titre', 'categorie', 'date_add', 'date_update', 'status', 'image_view')   
    search_fields = ('titre',)    
    ordering = ['titre']    
    fieldsets = [
        ("Informations publication", {"fields": ["image", "titre", "description", "categorie"]}),
        ("Statut", {"fields": ["status"]})
    ]

    def image_view(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='100px' height='50px'>")
        return ""
    image_view.short_description = "Aperçu de l'image"

class CommentaireAdmin(CustomAdmin):
    list_display = ('nom', 'date_add', 'date_update', 'status')   
    search_fields = ('nom',)    
    ordering = ['nom']    
    fieldsets = [
        ("Informations commentaire", {"fields": ["nom", "commentaire", "publication"]}),
        ("Statut", {"fields": ["status"]})
    ]

class LikeAdmin(CustomAdmin):
    list_display = ('publication', 'date_add', 'date_update', 'status')   
    search_fields = ('publication',)    
    ordering = ['publication']    
    fieldsets = [
        ("Informations like", {"fields": ["publication"]}),
        ("Statut", {"fields": ["status"]})
    ]

class ReponseCommentaireAdmin(CustomAdmin):
    list_display = ('nom', 'commentaire', 'date_add', 'date_update', 'status')   
    search_fields = ('nom',)    
    ordering = ['nom']    
    fieldsets = [
        ("Informations réponse", {"fields": ["nom", "reponse", "commentaire", "email"]}),
        ("Statut", {"fields": ["status"]})
    ]

class EvenementAdmin(CustomAdmin):
    list_display = ('titre', 'date_add', 'date_update', 'status', 'image_view')   
    search_fields = ('titre',)    
    ordering = ['titre']    
    fieldsets = [
        ("Informations événement", {"fields": ["titre", "description", "image"]}),
        ("Statut", {"fields": ["status"]})
    ]

    def image_view(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='100px' height='50px'>")
        return ""
    image_view.short_description = "Aperçu de l'image"

class CoursAdmin(CustomAdmin):
    list_display = ('titre', 'niveau', 'annee', 'date_add', 'date_update', 'status')   
    search_fields = ('titre',)    
    ordering = ['titre']    
    fieldsets = [
        ("Informations cours", {"fields": ["titre", "niveau", "annee", "cours", "description"]}),
        ("Statut", {"fields": ["status"]})
    ]

class TextesAdmin(CustomAdmin):
    list_display = ('titre', 'date_add', 'date_update', 'status', 'pdf')   
    search_fields = ('titre',)    
    ordering = ['titre']    
    fieldsets = [
        ("Informations texte", {"fields": ["titre", "description", "pdf"]}),
        ("Statut", {"fields": ["status"]})
    ]

class VideoAdmin(CustomAdmin):
    list_display = ('titre', 'date_add', 'date_update', 'status', 'video')   
    search_fields = ('titre',)    
    ordering = ['titre']    
    fieldsets = [
        ("Informations vidéo", {"fields": ["video", "titre", "description"]}),
        ("Statut", {"fields": ["status"]})
    ]

# Register all models with their corresponding admin class
admin.site.register(models.Categorie, CategorieAdmin)
admin.site.register(models.Publication, PublicationAdmin)
admin.site.register(models.Commentaire, CommentaireAdmin)
admin.site.register(models.ReponseCommentaire, ReponseCommentaireAdmin)
admin.site.register(models.Like, LikeAdmin)
admin.site.register(models.Evenement, EvenementAdmin)
admin.site.register(models.Cours, CoursAdmin)
admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.Textes, TextesAdmin)
