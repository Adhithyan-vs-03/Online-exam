from django.db import models
from Online_App.models import User 
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.utils.timezone import now


#product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


#Order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=7)  # Format: MM/YYYY
    cvv = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - ${self.amount}"
 
 #exam module   
class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    # session_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

#question module
class Question(models.Model):
    SUBJECT_CHOICES = [
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('Mathematics', 'Mathematics'),
        
    ]
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    text = RichTextField()  # Allows rich text input
    correct_option = models.IntegerField(default=1)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='Physics')

    # option1 = models.CharField(max_length=255,default="")
    # option2 = models.CharField(max_length=255,default="")
    # option3 = models.CharField(max_length=25,default="")
    # option4 = models.CharField(max_length=255,default="")

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
         return self.text
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    # exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def is_correct(self):
        return self.selected_option.is_correct  

    # class Meta:
    #     # Ensure that each user can only submit one answer per question per exam session
    #     unique_together = ['user', 'question', 'exam']  

    def __str__(self):
        return f"Answer by {self.user.username} for question {self.question.id} in exam {self.exam.session_id}"
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    guardian_name = models.CharField(max_length=100)
    guardian_number = models.CharField(max_length=15)
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    
    classX_board = models.CharField(max_length=100, blank=True, null=True)
    classX_percentage = models.FloatField(blank=True, null=True)
    classX_year = models.IntegerField(blank=True, null=True)
    
    classXII_board = models.CharField(max_length=100, null=True, blank=True)
    classXII_percentage = models.FloatField(null=True, blank=True)
    classXII_year = models.CharField(max_length=10, null=True, blank=True)

    
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    course_applied_for = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

from datetime import datetime
 #feedback
class Feedback(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Feedback from {self.name or 'Anonymous'}"
       
    
#new questionmodel
class Question1(models.Model):
    qtype_id = models.IntegerField()
    subject_id = models.IntegerField(null=True, blank=True)
    topic_id = models.IntegerField(null=True, blank=True)
    stopic_id = models.IntegerField(null=True, blank=True)
    diff_id = models.IntegerField()
    passage_id = models.IntegerField(null=True, blank=True)

    question = RichTextField()
    option1 = models.TextField(null=True, blank=True)
    option2 = models.TextField(null=True, blank=True)
    option3 = models.TextField(null=True, blank=True)
    option4 = models.TextField(null=True, blank=True)
    option5 = models.TextField(null=True, blank=True)
    option6 = models.TextField(null=True, blank=True)

    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    negative_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    hint = RichTextField(null=True, blank=True)
    explanation = RichTextField(null=True, blank=True)
    answer = models.CharField(max_length=15, null=True, blank=True)
    true_false = models.CharField(max_length=5, null=True, blank=True)
    fill_blank = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=3, default="Yes")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question {self.id} - {self.question[:50]}"
     