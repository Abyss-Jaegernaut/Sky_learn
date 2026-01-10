from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Profile, score

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'nom', 'email', 'type_utilisateur', 'is_staff')
    list_filter = ('type_utilisateur', 'is_staff', 'is_superuser')
    search_fields = ('username', 'nom', 'email')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations complémentaires', {'fields': ('nom', 'type_utilisateur', 'picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations complémentaires', {'fields': ('nom', 'type_utilisateur', 'picture')}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'site_web')
    search_fields = ('utilisateur__username', 'utilisateur__nom')

@admin.register(score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'cours', 'score', 'date_obtention')
    list_filter = ('cours',)
    search_fields = ('utilisateur__username', 'utilisateur__nom', 'cours')
