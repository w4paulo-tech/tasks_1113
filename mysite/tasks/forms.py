from .models import CustomUser, Uzduotis, UzduotisInstance
from django import forms as f
from django.contrib.auth.forms import UserCreationForm

class BaseUzduotisInstanceForm(f.ModelForm):
    
    class Meta:
        model = UzduotisInstance
        fields = ['status']

class StaffUzduotisInstanceForm(f.ModelForm):
    class Meta(BaseUzduotisInstanceForm.Meta):
        fields = BaseUzduotisInstanceForm.Meta.fields + ['worker', 'due_date']

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
