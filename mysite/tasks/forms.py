from .models import CustomUser, Uzduotis, UzduotisInstance
from django import forms as f
from django.contrib.auth.forms import UserCreationForm

class BaseUzduotisInstanceForm(f.ModelForm):
    name = f.CharField(label="Pavadinimas")
    content = f.CharField(widget=f.Textarea, label="Aprašymas")
    class Meta:
        model = UzduotisInstance
        fields = ['status']

class StaffUzduotisInstanceForm(BaseUzduotisInstanceForm):
    class Meta(BaseUzduotisInstanceForm.Meta):
        fields = BaseUzduotisInstanceForm.Meta.fields + ['worker', 'due_date']

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
