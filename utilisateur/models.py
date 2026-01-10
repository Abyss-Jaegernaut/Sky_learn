from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    ETUDIANT = 'ETU'
    INSTRUCTEUR = 'INS'
    
    utilisateur_TYPES = [
        (ETUDIANT, 'Étudiant'),
        (INSTRUCTEUR, 'Instructeur'),
    ]

    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom complet", blank=True)
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    type_utilisateur = models.CharField(max_length=3, choices=utilisateur_TYPES, default=ETUDIANT, verbose_name="Type d'utilisateur")
    picture = models.ImageField(upload_to='profile_pics/', default='default.png', blank=True, verbose_name="Photo de profil")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name="Genre")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Téléphone")
    address = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    program = models.ForeignKey('cursus.Program', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Programme")
    
    Level_CHOICES = [
        ('100', 'Niveau 100'),
        ('200', 'Niveau 200'),
        ('300', 'Niveau 300'),
        ('400', 'Niveau 400'),
    ]
    level = models.CharField(max_length=3, choices=Level_CHOICES, default='100', verbose_name="Niveau")
    
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")

    @property
    def get_picture_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        from django.templatetags.static import static
        return static('img/default.png')

    def __str__(self):
        return self.nom or self.username

    @property
    def is_student(self):
        return self.type_utilisateur == self.ETUDIANT

    @property
    def is_lecturer(self):
        return self.type_utilisateur == self.INSTRUCTEUR

    def get_user_role(self):
        if self.is_superuser:
            return 'Administrateur'
        elif self.is_lecturer:
            return 'Instructeur'
        elif self.is_student:
            return 'Étudiant'
        return 'Utilisateur'

    class Meta:
        ordering = ['id']
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

class Profile(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    biographie = models.TextField(blank=True)
    site_web = models.URLField(blank=True)

    def __str__(self):
        return f"Profile de {self.utilisateur.nom}"
    
    class Meta:
        ordering = ['id']

class score(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    cours = models.CharField(max_length=200)
    score = models.FloatField()
    date_obtention = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.nom} - {self.cours} : {self.score}"
    
    class Meta:
        ordering = ['id']
