from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class UtilisateurCreationForm(UserCreationForm):
    type_utilisateur = forms.ChoiceField(
        choices=[('ETU', 'Étudiant'), ('INS', 'Instructeur')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Je suis un"
    )

    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = UserCreationForm.Meta.fields + ('email', 'nom', 'type_utilisateur')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'input-field-control'})
