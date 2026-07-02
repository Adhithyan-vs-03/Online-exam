from django import forms
from .models import User
# from .models import Student
from .models import Product
from .models import UserAnswer, Question, Option,Question1
from ckeditor.widgets import CKEditorWidget


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'user_type']
        widgets = {
            'password': forms.PasswordInput(),
        }
# class StudentProfileForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = [
#             'first_name', 'last_name', 'date_of_birth', 'mobile_number',
#             'email', 'guardian_name', 'guardian_number', 'address', 
#             'pin_code', 'classX_board', 'classX_percentage', 'classX_year',
#             'classXII_board', 'classXII_percentage', 'classXII_year', 
#             'gender', 'course_applied_for'
#         ]
class PurchaseForm(forms.Form):
    product = forms.ModelChoiceField(
    queryset=Product.objects.all(),  # No stock filter
    label="Product"
)

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        min_length=13,
        widget=forms.TextInput(attrs={'placeholder': 'Card Number'}),
        label="Card Number"
    )
    cardholder_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Cardholder Name'}),
        label="Cardholder Name"
    )
    expiry_date = forms.DateField(
        widget=forms.TextInput(attrs={'placeholder': 'MM/YYYY'}),
        label="Expiry Date"
    )
    cvv = forms.CharField(
        max_length=4,
        min_length=3,
        widget=forms.PasswordInput(attrs={'placeholder': 'CVV'}),
        label="CVV"
    )

#exam

class ExamSubmissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        exam = kwargs.pop('exam')
        super().__init__(*args, **kwargs)

        for question in exam.questions.all():
            choices = [(option.id, option.text) for option in question.options.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices, widget=forms.RadioSelect, required=True
            )    

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = '__all__'
#         widgets = {
#             'text': CKEditorWidget(),
#         }
# class OptionForm(forms.ModelForm):
#     class Meta:
#         model = Option
#         fields = ['text', 'is_correct']

class QuestionForm(forms.ModelForm):
    question = forms.CharField(widget=CKEditorWidget())
    option1 = forms.CharField(max_length=25, initial="", required=False)
    option2 = forms.CharField(max_length=25, initial="", required=False)
    option3 = forms.CharField(max_length=25, initial="", required=False)
    option4 = forms.CharField(max_length=25, initial="", required=False)
    option5 = forms.CharField(max_length=25, initial="", required=False)
    option6 = forms.CharField(max_length=25, initial="", required=False)
    hint = forms.CharField(max_length=25, initial="", required=False)
    explanation = forms.CharField(max_length=25, initial="", required=False) 

    class Meta:
        model = Question1
        fields = "__all__"      



