from django import forms
from django.contrib.auth import get_user_model
from .models import Student, PackagePurchase, QuestionPaper, BiologyQuestion, ChemistryQuestion, MathematicsQuestion, PhysicsQuestion
from django.utils.timezone import now, timedelta

# Get the active User model (will use your custom User)
User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    user_type = forms.ChoiceField(
        choices=[
            (1, 'Admin'),
            (2, 'Staff'), 
            (3, 'Parent'),
            (4, 'Student'),
            (5, 'MainStaff')
        ],
        required=True
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'user_type']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove user_type from Meta.fields if it doesn't exist
        if not hasattr(User, 'user_type'):
            self.fields.pop('user_type', None)
            self.Meta.fields = [f for f in self.Meta.fields if f != 'user_type']



# forms.py (if exists)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import your custom User model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'user_type')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'email', 'phone_number', 'guardian_name', 
            'guardian_number', 'address', 'package_selected'
        ]

from .models import PackagePurchase, Package

class AddPackageForm(forms.ModelForm):

    student = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Select Student"
    )

    package = forms.ModelChoiceField(
        queryset=Package.objects.all(),
        label="Select Package"
    )

    expiry_date = forms.DateTimeField(
        initial=now() + timedelta(days=30),
        label="Expiry Date"
    )

    class Meta:
        model = PackagePurchase
        fields = ['student', 'package', 'expiry_date']

class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = "__all__"
        widgets = {
            'created_by': forms.HiddenInput(),
        }

class ChemistryQuestionForm(forms.ModelForm):
    correct_options = forms.MultipleChoiceField(
        choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = ChemistryQuestion
        fields = '__all__'
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'chapter': forms.TextInput(attrs={'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'chemical_formula': forms.TextInput(attrs={'class': 'form-control'}),
            'chemical_equation': forms.TextInput(attrs={'class': 'form-control'}),
            'diagram_image': forms.FileInput(attrs={'class': 'form-control'}),
            'option1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 1'}),
            'option2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 2'}),
            'option3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 3'}),
            'option4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 4'}),
            'given_values': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'balanced_equation': forms.TextInput(attrs={'class': 'form-control'}),
            'balancing_steps': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'match_items': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class MathematicsQuestionForm(forms.ModelForm):
    class Meta:
        model = MathematicsQuestion
        fields = '__all__'
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'option1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 1'}),
            'option2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 2'}),
            'option3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 3'}),
            'option4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 4'}),
        }

# Add these if they don't exist
class PhysicsQuestionForm(forms.ModelForm):
    class Meta:
        model = PhysicsQuestion
        fields = '__all__'

class BiologyQuestionForm(forms.ModelForm):
    class Meta:
        model = BiologyQuestion
        fields = '__all__'
        
        
