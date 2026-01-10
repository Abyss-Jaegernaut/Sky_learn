from django import forms
from .models import Program, Course, Post
from utilisateur.models import Utilisateur

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'summary']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['titre', 'code', 'credit', 'description', 'summary', 'image', 'prix', 'instructeur', 'program', 'semester', 'year', 'level', 'is_elective']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titre', 'resume', 'image', 'type_post']

class StudentAddForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'phone', 'address', 'program', 'level', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.type_utilisateur = 'ETU'
        if commit:
            user.save()
        return user

class LecturerAddForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'phone', 'address', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.type_utilisateur = 'INS'
        user.is_staff = True
        if commit:
            user.save()
        return user
