from .models import CustomUser, Uzduotis, UzduotisInstance
from django import forms as f
from django.contrib.auth.forms import UserCreationForm

class StaffUzduotisForm(f.ModelForm):
    class Meta:
        model = UzduotisInstance
        fields = ['task', 'worker', 'due_date', 'shift', 'status']
        widgets = {
            'due_date': f.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].disabled = True

class StaffUzduotisTemplateForm(f.ModelForm):
    class Meta:
        model = Uzduotis
        fields = ['name', 'content', 'shift']        

class BaseUzduotisInstanceForm(f.ModelForm):
    task_default = f.ModelChoiceField(
        queryset=Uzduotis.objects.all().order_by('name'),
        label="Užduoties šablonas",
        help_text="Pasirinkite užduoties tipą iš sąrašo.",
        required=True
    )
    class Meta:
        model = UzduotisInstance
        fields = ['task_default', 'status', 'notes']

class StaffUzduotisInstanceForm(BaseUzduotisInstanceForm):
    class Meta(BaseUzduotisInstanceForm.Meta):
        fields = BaseUzduotisInstanceForm.Meta.fields + ['worker', 'due_date']
        widgets = {'due_date': f.DateTimeInput(attrs={'type': 'datetime-local'})}

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
        widgets = {
            'shift': f.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'shift': '',
        }
