from django.db import models
from django.urls import reverse

class Program(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name="Titre du programme")
    summary = models.TextField(null=True, blank=True, verbose_name="Résumé")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('program_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"

class Session(models.Model):
    session = models.CharField(max_length=200, unique=True, verbose_name="Session")
    is_current_session = models.BooleanField(default=False, verbose_name="Session actuelle")
    next_session_beginning = models.DateField(null=True, blank=True, verbose_name="Début de la prochaine session")

    def __str__(self):
        return self.session

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

class Semester(models.Model):
    semester = models.CharField(max_length=10, verbose_name="Semestre")
    is_current_semester = models.BooleanField(default=False, verbose_name="Semestre actuel")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Session")

    def __str__(self):
        return f"{self.semester} ({self.session})"

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"

class Course(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Code du cours")
    credit = models.IntegerField(default=3, verbose_name="Crédits")
    description = models.TextField(verbose_name="Description")
    summary = models.TextField(max_length=200, null=True, blank=True, verbose_name="Résumé court")
    image = models.ImageField(upload_to='courses/', null=True, blank=True, verbose_name="Image de couverture")
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Prix")
    instructeur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, verbose_name="Instructeur")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Programme")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Semestre")
    
    YEAR_CHOICES = [
        ('1', '1ère Année'),
        ('2', '2ème Année'),
        ('3', '3ème Année'),
        ('4', '4ème Année'),
    ]
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, default='1', verbose_name="Année")
    is_elective = models.BooleanField(default=False, verbose_name="Optionnel")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    Level_CHOICES = [
        ('Deb', 'Débutant'),
        ('Int', 'Intermédiaire'),
        ('Avc', 'Avancé'),
    ]
    level = models.CharField(max_length=3, choices=Level_CHOICES, default='Deb', verbose_name="Niveau")

    def __str__(self):
        return f"{self.code} - {self.titre}" if self.code else self.titre

    def get_absolute_url(self):
        return reverse('course_single', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"

class Enrollment(models.Model):
    student = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='enrollments', verbose_name="Étudiant")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Cours")
    date_enrolled = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")

    def __str__(self):
        return f"{self.student.username} inscrit à {self.course.titre}"

    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
    
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name="Cours")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
    
class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE, verbose_name="Module")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    contenu = models.TextField(verbose_name="Contenu")

    def __str__(self):
        return self.titre
    
    class Meta:
        ordering = ['id']
        verbose_name = "Leçon"
        verbose_name_plural = "Leçons"

class Projet(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='projets', verbose_name="Cours")
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='projets', verbose_name="Utilisateur")
    date_rendu = models.DateTimeField(null=True, blank=True, verbose_name="Date de rendu")
    fichier = models.FileField(upload_to='projets/', null=True, blank=True, verbose_name="Fichier")
    score = models.FloatField(null=True, blank=True, verbose_name="Note")

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

class Post(models.Model):
    NEWS = 'Nouveauté'
    EVENT = 'Événement'
    POSTED_AS = [
        (NEWS, 'Nouveauté'),
        (EVENT, 'Événement'),
    ]
    titre = models.CharField(max_length=200, verbose_name="Titre", default="")
    resume = models.TextField(verbose_name="Résumé", default="")
    image = models.ImageField(upload_to='posts/', null=True, blank=True, verbose_name="Image")
    type_post = models.CharField(max_length=10, choices=POSTED_AS, default=NEWS, verbose_name="Type de post")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"

class certificat(models.Model):
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, verbose_name="Utilisateur")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Cours")
    date_obtention = models.DateTimeField(auto_now_add=True, verbose_name="Date d'obtention")

    def __str__(self):
        return f"{self.utilisateur.nom} - {self.course.titre}"
    
    class Meta:
        ordering = ['id']
        verbose_name = "Certificat"
        verbose_name_plural = "Certificats"
