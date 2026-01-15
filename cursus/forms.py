from django import forms
from .models import Program, Course, Post, Assignment, Submission, Session
from utilisateur.models import Utilisateur

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session', 'is_current_session', 'next_session_beginning']
        widgets = {
            'next_session_beginning': forms.DateInput(attrs={'type': 'date'}),
        }

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        label="Date limite"
    )
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'comment']

class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'feedback']
    
    grade = forms.FloatField(max_value=100, min_value=0, label="Note (/100)")
    feedback = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

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

class StudentEditForm(forms.ModelForm):
    """Formulaire pour éditer un étudiant (sans mot de passe obligatoire)"""
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'phone', 'address', 'program', 'level', 'picture']

class LecturerEditForm(forms.ModelForm):
    """Formulaire pour éditer un instructeur (sans mot de passe obligatoire)"""
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'phone', 'address', 'picture']