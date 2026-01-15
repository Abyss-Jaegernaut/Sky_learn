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

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'first_name', 'last_name', 'email', 'phone', 'address', 'picture', 'biographie', 'site_web']

    biographie = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    site_web = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['biographie'].initial = self.instance.profile.biographie
            self.fields['site_web'].initial = self.instance.profile.site_web
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                profile = user.profile
                profile.biographie = self.cleaned_data['biographie']
                profile.site_web = self.cleaned_data['site_web']
                profile.save()
            else:
                # Handle case where profile doesn't exist (though it should usually be created via signal)
                from .models import Profile
                Profile.objects.create(
                    utilisateur=user,
                    biographie=self.cleaned_data['biographie'],
                    site_web=self.cleaned_data['site_web']
                )
        return user
