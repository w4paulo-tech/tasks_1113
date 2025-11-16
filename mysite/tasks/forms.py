from .models import CustomUser, Uzduotis, UzduotisInstance
from django import forms as f
from django.contrib.auth.forms import UserCreationForm

class BaseUzduotisInstanceForm(f.ModelForm):
    task_default = f.ModelChoiceField(
        queryset=Uzduotis.objects.all().order_by('name'),
        label="Užduoties šablonas",
        help_text="pasirinkite užduoties tipą iš sąrašo."
    )
    class Meta:
        model = UzduotisInstance
        fields = ['task_default', 'status', 'notes']

class StaffUzduotisInstanceForm(BaseUzduotisInstanceForm):
    class Meta(BaseUzduotisInstanceForm.Meta):
        fields = BaseUzduotisInstanceForm.Meta.fields + ['worker', 'due_date']
        widgets = {'due_date': f.DateInput(attrs={'type': 'date'})}

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserUpdateForm(f.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class StaffUserUpdateForm(f.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['shift']
