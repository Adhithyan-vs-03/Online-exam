from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from ckeditor.fields import RichTextField
import re
from django.utils.html import strip_tags


# Custom User Model
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Staff'),
        (3, 'Parent'),
        (4, 'Student'),
        (5, 'MainStaff')
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)  # ✅ default

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


TYPE_CHOICES = (
    ('admin', 'Admin Added'),
    ('self', 'Self Registered'),
)

class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_profiles')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField()
    contact = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # ⭐ NEW FIELD
    created_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='admin')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user.username}"





class StudentProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    guardian_name = models.CharField(max_length=200)
    guardian_number = models.CharField(max_length=15)
    course_applied_for = models.CharField(max_length=100)
    
    # Optional: Add these fields for better management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"




# ADD THIS NEW MODEL FOR TEACHERS/STAFF
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)
    contact = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"

# Student model to store profile details
TYPE_CHOICES = [
    ('admin', 'Admin Added'),
    ('self', 'Self Registered'),
]

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=100, default='Unknown')
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_number = models.CharField(max_length=15, blank=True, null=True)
    package_selected = models.CharField(max_length=100, default='Basic Package')
    
    # ⭐ NEW: CREATED TYPE FIELD FOR STUDENTS
    created_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='admin')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name
    

class PackagePurchase(models.Model):
    BUYER_TYPES = [('student', 'Student'), ('parent', 'Parent')]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_type = models.CharField(max_length=10, choices=BUYER_TYPES)
    package_name = models.CharField(max_length=50)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    added_by_admin = models.BooleanField(default=False)  # Track if added by admin
    
    def __str__(self):
        return f"{self.buyer.username} - {self.package_name}"


class ExamPlan(models.Model):
    PLAN_TYPES = [
        ('neet', 'NEET'),
        ('jee', 'JEE'),
        ('combined', 'NEET + JEE Combined'),
    ]
    
    DURATION_CHOICES = [
        ('monthly', 'Per Month'),
        ('yearly', 'Per Year'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    
    # Features
    users = models.IntegerField(default=1)
    practice_tests = models.IntegerField(default=0)
    full_length_mocks = models.IntegerField(default=0)
    doubt_sessions = models.IntegerField(default=0)
    study_materials = models.BooleanField(default=False)
    video_lectures = models.BooleanField(default=False)
    performance_analytics = models.BooleanField(default=False)
    storage = models.CharField(max_length=50, default="1024 MB")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.plan_type} ({self.duration})"



# Renamed Exam model to ExamDetailclass StudentMarks(models.Model):
class StudentMarks(models.Model):
    student = models.ForeignKey("examapp.StudentProfile", on_delete=models.CASCADE, related_name="marks")
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name

class ExamDetail(models.Model):
    student_mark = models.ForeignKey(StudentMarks, on_delete=models.CASCADE, related_name="exam_details")
    exam_date = models.DateField()
    exam_time = models.CharField(max_length=255)
    maths_marks = models.IntegerField(default=0)
    biology_marks = models.IntegerField(default=0)
    chemistry_marks = models.IntegerField(default=0)
    physics_marks = models.IntegerField(default=0)
    
    total_marks = models.IntegerField(default=0, editable=False)
    percentage = models.FloatField(default=0, editable=False)

    def save(self, *args, **kwargs):
        self.total_marks = self.maths_marks + self.biology_marks + self.chemistry_marks + self.physics_marks
        self.percentage = (self.total_marks / 400) * 100  # Assuming each subject is out of 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_mark.name} - {self.exam_date}"

 
from django.db import models
from django.utils.html import strip_tags

from django.db import models
from django.utils import timezone



class BiologyQuestion(models.Model):
    QUESTION_TYPES = [
        ('objective', 'Objective (MCQ)'),
        ('descriptive', 'Descriptive'),
        ('match_following', 'Match the Following'),
        ('fill_in_the_blanks', 'Fill in the Blanks'),
    ]
    
    # Basic fields
    chapter = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    question = models.TextField()
    answer = models.TextField()
    
    # Biology specific fields
    formula = models.TextField(blank=True, null=True)
    diagram_reference = models.TextField(blank=True, null=True)
    diagram_image = models.ImageField(upload_to='biology/diagrams/', blank=True, null=True)
    
    # Options for objective questions
    option1 = models.TextField(blank=True, null=True)
    option2 = models.TextField(blank=True, null=True)
    option3 = models.TextField(blank=True, null=True)
    option4 = models.TextField(blank=True, null=True)
    option5 = models.TextField(blank=True, null=True)
    
    # Correct options (can store multiple for MCQ)
    correct_options = models.JSONField(default=list, blank=True, null=True)
    
    # For match_following question type
    match_items = models.TextField(blank=True, null=True)
    match_count = models.IntegerField(blank=True, null=True)
    
    # For fill_in_the_blanks question type
    blank_positions = models.CharField(max_length=100, blank=True, null=True)
    blank_count = models.IntegerField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, 
                                   null=True, blank=True, 
                                   related_name='biology_questions_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, 
                                   null=True, blank=True, 
                                   related_name='biology_questions_updated')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Biology Question"
        verbose_name_plural = "Biology Questions"
    
    def __str__(self):
        return f"Biology: {self.chapter} - {self.topic} ({self.question_type})"
    
    @property
    def has_image(self):
        return bool(self.diagram_image)
    
    @property
    def is_objective(self):
        return self.question_type == 'objective'
    
    @property
    def is_descriptive(self):
        return self.question_type == 'descriptive'
    
    @property
    def is_match_following(self):
        return self.question_type == 'match_following'
    
    @property
    def is_fill_blanks(self):
        return self.question_type == 'fill_in_the_blanks'
    
    def get_correct_options_display(self):
        """Convert correct options to letters (1->A, 2->B, etc.)"""
        if not self.correct_options:
            return ""
        
        letters = []
        for opt in self.correct_options:
            if opt == '1':
                letters.append('A')
            elif opt == '2':
                letters.append('B')
            elif opt == '3':
                letters.append('C')
            elif opt == '4':
                letters.append('D')
            elif opt == '5':
                letters.append('E')
        
        return ', '.join(letters)


class ChemistryQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('objective', 'Objective (MCQ)'),
        ('descriptive', 'Descriptive'),
        ('numerical', 'Numerical'),
        ('equation_balancing', 'Equation Balancing'),
        ('match_following', 'Match the Following'),
    ]

    chapter = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    question = models.TextField()
    answer = models.TextField()

    # For MCQ questions
    option1 = models.TextField(blank=True, null=True)
    option2 = models.TextField(blank=True, null=True)
    option3 = models.TextField(blank=True, null=True)
    option4 = models.TextField(blank=True, null=True)
    correct_options = models.CharField(max_length=50, blank=True, null=True)
    
    # Chemistry-specific fields
    final_answer = models.CharField(max_length=500, blank=True, null=True)
    numerical_solution = models.CharField(max_length=200, blank=True, null=True)
    chemical_equation = models.CharField(max_length=500, blank=True, null=True)
    chemical_formula = models.CharField(max_length=200, blank=True, null=True)
    reaction_type = models.CharField(max_length=50, blank=True, null=True)
    equation_latex = models.TextField(blank=True, null=True)
    
    # For Numerical questions
    given_values = models.CharField(max_length=500, blank=True, null=True)
    molar_mass = models.FloatField(blank=True, null=True)
    
    # For Equation Balancing
    balanced_equation = models.CharField(max_length=500, blank=True, null=True)
    balancing_steps = models.TextField(blank=True, null=True)
    answer_reaction_type = models.CharField(max_length=50, blank=True, null=True)
    
    # For Match the Following
    match_items = models.TextField(blank=True, null=True)
    match_count = models.IntegerField(default=4)
    match_answers = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    diagram_image = models.ImageField(upload_to="chemistry_questions/", null=True, blank=True)
    answer_image = models.ImageField(upload_to="chemistry_answers/", null=True, blank=True)

    def __str__(self):
        return f"{self.chapter} - {self.topic}"


class PhysicsQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('objective', 'Objective (MCQ)'),
        ('descriptive', 'Descriptive'),
        ('numerical', 'Numerical'),
        ('graph_based', 'Graph Based'),
        ('diagram_based', 'Diagram Based'),
        ('match_following', 'Match the Following'),
    ]

    chapter = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    question = models.TextField()
    answer = models.TextField()

    # For MCQ questions
    option1 = models.TextField(blank=True, null=True)
    option2 = models.TextField(blank=True, null=True)
    option3 = models.TextField(blank=True, null=True)
    option4 = models.TextField(blank=True, null=True)
    correct_options = models.CharField(max_length=50, blank=True, null=True)
    
    # Physics-specific fields
    formula = models.CharField(max_length=200, blank=True, null=True)
    units = models.CharField(max_length=100, blank=True, null=True)
    given_values = models.CharField(max_length=500, blank=True, null=True)
    
    # For Numerical questions
    final_answer = models.CharField(max_length=200, blank=True, null=True)
    numerical_solution = models.TextField(blank=True, null=True)
    
    # For Graph Based questions
    graph_type = models.CharField(max_length=50, blank=True, null=True)
    graph_xlabel = models.CharField(max_length=100, blank=True, null=True)
    graph_ylabel = models.CharField(max_length=100, blank=True, null=True)
    graph_data = models.TextField(blank=True, null=True)
    graph_interpretation = models.TextField(blank=True, null=True)
    graph_calculations = models.TextField(blank=True, null=True)
    graph_observations = models.TextField(blank=True, null=True)
    
    # For Diagram Based questions
    diagram_description = models.TextField(blank=True, null=True)
    diagram_labels = models.CharField(max_length=500, blank=True, null=True)
    diagram_analysis = models.TextField(blank=True, null=True)
    
    # For Match the Following
    match_items = models.TextField(blank=True, null=True)
    match_count = models.IntegerField(default=4)
    match_answers = models.TextField(blank=True, null=True)
    
    # Image fields
    question_graph_image = models.ImageField(upload_to='physics_graphs/question/', blank=True, null=True)
    answer_graph_image = models.ImageField(upload_to='physics_graphs/answer/', blank=True, null=True)
    diagram_image = models.ImageField(upload_to='physics_diagrams/', blank=True, null=True)
    labeled_diagram = models.ImageField(upload_to='physics_diagrams/labeled/', blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chapter} - {self.topic}"


class MathematicsQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('objective', 'Objective (MCQ)'),
        ('descriptive', 'Descriptive'),
        ('numerical', 'Numerical'),
        ('theorem', 'Theorem'),
        ('graph_based', 'Graph Based'),
    ]

    chapter = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    question = models.TextField()
    answer = models.TextField()

    # For MCQ questions
    option1 = models.TextField(blank=True, null=True)
    option2 = models.TextField(blank=True, null=True)
    option3 = models.TextField(blank=True, null=True)
    option4 = models.TextField(blank=True, null=True)
    correct_options = models.CharField(max_length=50, blank=True, null=True)
    
    # Mathematics-specific fields
    formula = models.TextField(blank=True, null=True)
    theorem_statement = models.TextField(blank=True, null=True)
    theorem_name = models.CharField(max_length=200, blank=True, null=True)
    equation_latex = models.TextField(blank=True, null=True)
    
    # For Numerical questions
    given_values = models.CharField(max_length=500, blank=True, null=True)
    final_answer = models.CharField(max_length=200, blank=True, null=True)
    step_solution = models.TextField(blank=True, null=True)
    
    # For Theorem questions
    theorem_proof = models.TextField(blank=True, null=True)
    theorem_applications = models.TextField(blank=True, null=True)
    
    # For Graph Based questions
    graph_type = models.CharField(max_length=50, blank=True, null=True)
    function_equation = models.CharField(max_length=200, blank=True, null=True)
    graph_points = models.TextField(blank=True, null=True)
    graph_analysis = models.TextField(blank=True, null=True)
    graph_keypoints = models.TextField(blank=True, null=True)
    graph_calculations = models.TextField(blank=True, null=True)
    
    # Image fields for graphs and diagrams
    graph_image = models.ImageField(upload_to='math_graphs/', blank=True, null=True)
    diagram_image = models.ImageField(upload_to='math_diagrams/', blank=True, null=True)
    theorem_diagram = models.ImageField(upload_to='math_theorem_diagrams/', blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chapter} - {self.topic}"

# Exam Schedule model (keeping this one)
class ExamSchedule(models.Model):
    exam_date = models.DateField()  # Correctly stores date in YYYY-MM-DD format
    exam_time = models.TimeField()  # Correctly stores time in HH:MM:SS format
    exam_subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.exam_subject} on {self.exam_date} at {self.exam_time}"



from datetime import datetime
 #feedback
class Feedback_review(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)  # No parentheses

    

    def __str__(self):
        return f"Feedback from {self.name or 'Anonymous'}"

    

    
from django.db import models



class Question(models.Model):
    # Basic fields
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    chapter = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    question_type = models.CharField(max_length=50)
    question = models.TextField()
    marks = models.IntegerField(default=1)
    difficulty = models.CharField(max_length=20, default='medium')
    
    # Answer field
    answer = models.TextField(blank=True, null=True)
    
    # Objective/MCQ fields
    option1 = models.TextField(blank=True, null=True)
    option2 = models.TextField(blank=True, null=True)
    option3 = models.TextField(blank=True, null=True)
    option4 = models.TextField(blank=True, null=True)
    correct_options = models.CharField(max_length=100, blank=True, null=True)
    
    # Match the Following fields
    match_items = models.TextField(blank=True, null=True)
    match_answers = models.TextField(blank=True, null=True)
    match_count = models.IntegerField(default=4)
    
    # Fill in the Blanks fields
    blank_answers = models.TextField(blank=True, null=True)
    blank_positions = models.CharField(max_length=200, blank=True, null=True)
    blank_count = models.IntegerField(default=1)
    
    # Numerical fields
    numerical_solution = models.TextField(blank=True, null=True)
    final_answer = models.CharField(max_length=200, blank=True, null=True)
    
    # Chemistry specific
    chemical_equation = models.TextField(blank=True, null=True)
    balanced_equation = models.TextField(blank=True, null=True)
    balancing_steps = models.TextField(blank=True, null=True)
    
    # Graph based fields
    graph_type = models.CharField(max_length=100, blank=True, null=True)
    graph_analysis = models.TextField(blank=True, null=True)
    question_graph_image = models.ImageField(upload_to='question_graphs/', blank=True, null=True)
    
    # Diagram based fields
    diagram_analysis = models.TextField(blank=True, null=True)
    diagram_image = models.ImageField(upload_to='question_diagrams/', blank=True, null=True)
    
    # Theorem fields
    theorem_statement = models.TextField(blank=True, null=True)
    theorem_proof = models.TextField(blank=True, null=True)
    theorem_diagram = models.ImageField(upload_to='theorem_diagrams/', blank=True, null=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject.name} - {self.chapter} - {self.question_type}"
    
    class Meta:
        ordering = ['-created_at']





import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from ckeditor.fields import RichTextField
import re
from django.utils.html import strip_tags
from django.utils import timezone  # Already there
from django.core.validators import FileExtensionValidator  # Already there
# Add this to your models.py
class GeneratedQuestionPaper(models.Model):
    PAPER_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic information
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # School/Exam information
    school_name = models.CharField(max_length=255, blank=True, null=True)
    school_address = models.TextField(blank=True, null=True)
    school_contact = models.CharField(max_length=255, blank=True, null=True)
    affiliation_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Exam details
    exam_name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=100, blank=True, null=True)
    course_name = models.CharField(max_length=100, blank=True, null=True)
    total_marks = models.IntegerField()
    time_duration = models.CharField(max_length=100)
    exam_date = models.DateField(blank=True, null=True)
    exam_time = models.IntegerField(default=180, help_text="Time in minutes")
    
    # Instructions and settings
    instructions = models.TextField(blank=True, null=True)
    logo_position = models.CharField(max_length=50, default='left')
    
    # Content
    question_data = models.JSONField()  # Store the selected questions data
    paper_html = models.TextField(blank=True, null=True)  # Store formatted HTML
    pdf_file = models.FileField(upload_to='question_papers/pdfs/', blank=True, null=True)
    logo_image = models.ImageField(upload_to='question_papers/logos/', blank=True, null=True)
    
    # Additional elements
    additional_elements = models.JSONField(blank=True, null=True)  # Watermark, signatures, etc.
    
    # Metadata
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='generated_papers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=PAPER_STATUS_CHOICES, default='draft')
    is_published = models.BooleanField(default=False)
    
    # Statistics
    total_questions = models.IntegerField(default=0)
    subjects_included = models.JSONField(blank=True, null=True)  # List of subjects
    
    # ✨ NEW FIELDS FOR EDITING ✨
    is_editable = models.BooleanField(default=True)
    edit_count = models.IntegerField(default=0)
    last_edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                       related_name='edited_papers')
    last_edited_at = models.DateTimeField(null=True, blank=True)
    original_paper_id = models.IntegerField(null=True, blank=True)  # For tracking copies
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Generated Question Paper"
        verbose_name_plural = "Generated Question Papers"
    
    def __str__(self):
        return f"{self.title} - {self.exam_name} ({self.created_at.date()})"
    
    def get_absolute_url(self):
        return f"/question-papers/{self.unique_id}/"
    
    def delete_pdf_file(self):
        """Safely delete the PDF file"""
        if self.pdf_file:
            self.pdf_file.delete(save=False)
    
    def delete_logo_image(self):
        """Safely delete the logo image"""
        if self.logo_image:
            self.logo_image.delete(save=False)
    
    # ✨ NEW METHODS FOR EDITING ✨
    def can_edit(self, user):
        """Check if user can edit this paper"""
        return self.is_editable and (self.created_by == user or user.is_staff)
    
    def create_copy(self, user):
        """Create a copy of this paper for editing"""
        copy = GeneratedQuestionPaper.objects.create(
            # Copy all fields
            title=f"Copy of {self.title}",
            description=self.description,
            school_name=self.school_name,
            school_address=self.school_address,
            school_contact=self.school_contact,
            affiliation_number=self.affiliation_number,
            exam_name=self.exam_name,
            class_name=self.class_name,
            course_name=self.course_name,
            total_marks=self.total_marks,
            time_duration=self.time_duration,
            exam_date=self.exam_date,
            exam_time=self.exam_time,
            instructions=self.instructions,
            logo_position=self.logo_position,
            question_data=self.question_data,  # Deep copy would be better
            paper_html=self.paper_html,
            additional_elements=self.additional_elements,
            created_by=user,
            status='draft',
            is_published=False,
            total_questions=self.total_questions,
            subjects_included=self.subjects_included,
            # Track original
            original_paper_id=self.id,
            is_editable=True
        )
        
        # Copy logo if exists
        if self.logo_image:
            import os
            from django.core.files.base import ContentFile
            
            # Create a new file name
            name, ext = os.path.splitext(self.logo_image.name)
            new_name = f"copy_{copy.id}{ext}"
            
            # Copy the file
            copy.logo_image.save(new_name, ContentFile(self.logo_image.read()))
        
        return copy



class TeacherPaperSettings(models.Model):
    """Store teacher's question paper settings"""
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paper_settings')
    
    # Logo and school settings
    school_name = models.CharField(max_length=255, default='Your School Name')
    school_address = models.TextField(default='City, State, PIN Code')
    school_contact = models.CharField(max_length=255, default='Phone: 1234567890 | Email: school@example.com')
    affiliation_number = models.CharField(max_length=100, default='Affiliation No: 123456')
    
    # Logo settings
    logo_image = models.ImageField(
        upload_to='teacher_logos/%Y/%m/%d/',
        blank=True,
        null=True,
        max_length=500  # Increase max_length for longer paths
    )
    logo_position = models.CharField(max_length=20, default='center', choices=[
        ('center', 'Center Only'),
        ('none', 'No Logo')
    ])
    
    # Paper defaults
    default_exam_name = models.CharField(max_length=255, default='Mid-Term Examination')
    default_total_marks = models.IntegerField(default=100)
    default_time_duration = models.CharField(max_length=100, default='3 hours')
    default_instructions = models.TextField(default='''All questions are compulsory.
Read each question carefully before answering.
Write answers in the space provided.
Use blue/black ballpoint pen only.
Calculators are not allowed unless specified.
Write your roll number on every page.''')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Teacher Paper Settings"
        verbose_name_plural = "Teacher Paper Settings"
        unique_together = ['teacher']
    
    def __str__(self):
        return f"Paper Settings for {self.teacher.username}"
    
    def delete(self, *args, **kwargs):
        """Delete the logo file when settings are deleted"""
        if self.logo_image:
            self.logo_image.delete(save=False)
        super().delete(*args, **kwargs)








from datetime import date
class MainStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    profile_photo = models.ImageField(upload_to='mainstaff_photos/', blank=True, null=True)
    joined_date = models.DateField(null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    class_name = models.CharField(max_length=200)

    def __str__(self):
        return self.class_name




class Subject(models.Model):
    class_name = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    @property
    def chapters_count(self):
        # Using property decorator
        try:
            from .models import Chapter
            return Chapter.objects.filter(subject=self).count()
        except:
            return 0

    def __str__(self):
        return self.name


from django.db import models

class ContentSource(models.Model):
    SOURCE_TYPES = [
        ('ncert', 'NCERT'),
        ('scert', 'SCERT'), 
        ('neet', 'NEET'),
        ('jee', 'JEE'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPES)
    class_name = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True, blank=True)
    original_file = models.FileField(upload_to='content_sources/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_data = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.source_type})"

    class Meta:
        db_table = 'content_source'

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=0)  # Add this if you want ordering
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SubTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class QuestionImage(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="question_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.id}"


class StaffNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title



# In examapp/models.py
class QuestionPaper(models.Model):
    # Existing fields from your error message:
    exam_name = models.CharField(max_length=200)  # Keep as CharField(200) if that's what you have
    exam_time = models.CharField(max_length=255)
    total_marks = models.IntegerField()
    
    # Additional fields from your code:
    is_published = models.BooleanField(default=False)
    exam_date_actual = models.DateField(blank=True, null=True)
    time_duration = models.CharField(max_length=100, default="3 hours")
    instructions = models.TextField(blank=True, null=True)
    
    # New timestamp fields:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        # Use the merged str method
        if self.exam_name:
            return f"{self.exam_name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        return f"Question Paper - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Optional: Add any other methods you need
    def get_total_questions(self):
        """Calculate total number of questions across all subjects"""
        total = 0
        if hasattr(self, 'mathematics_questions'):
            total += self.mathematics_questions.count()
        if hasattr(self, 'physics_questions'):
            total += self.physics_questions.count()
        if hasattr(self, 'chemistry_questions'):
            total += self.chemistry_questions.count()
        if hasattr(self, 'biology_questions'):
            total += self.biology_questions.count()
        return total
    

class AssignedExam(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.question_paper}"
    
class ExamResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_results')
    paper = models.ForeignKey(GeneratedQuestionPaper, on_delete=models.CASCADE, null=True, blank=True)
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, null=True, blank=True)
    
    # ADD THESE FIELDS if you need them:
    exam_time = models.DateTimeField(null=True, blank=True, help_text="When the exam was taken")
    status = models.CharField(max_length=20, default='completed', choices=[
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('failed', 'Failed'),
    ])
    
    # Mark fields
    total_marks = models.IntegerField()
    obtained_marks = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5)
    
    # Answer statistics
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    unattempted = models.IntegerField(default=0)
    
    # Time management
    time_taken = models.IntegerField(help_text="Time taken in minutes")
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # Store all answers
    answers = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.paper.title if self.paper else 'Paper'} - {self.grade}"

class QuestionResult(models.Model):
    exam_result = models.ForeignKey(ExamResult, on_delete=models.CASCADE, related_name='question_results')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Q{self.question.id} - {self.is_correct}"


# Add after your existing models

# Add at the top of models.py


from django.core.validators import FileExtensionValidator


class StudentExamSubmission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('evaluated', 'Evaluated'),
        ('rejected', 'Rejected'),
        ('draft', 'Draft'),
    ]
    
    # Evaluation status choices
    EVALUATION_STATUS = (
        ('pending', 'Pending Evaluation'),
        ('draft', 'Draft Evaluation'),
        ('evaluated', 'Evaluated'),
        ('published', 'Published to Student'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_submissions')
    
    # Store both types of papers
    generated_paper = models.ForeignKey('GeneratedQuestionPaper', on_delete=models.CASCADE, null=True, blank=True)
    question_paper = models.ForeignKey('QuestionPaper', on_delete=models.CASCADE, null=True, blank=True)
    
    exam_result = models.ForeignKey('ExamResult', on_delete=models.CASCADE, null=True, blank=True)
    
    student_name = models.CharField(max_length=200)
    student_email = models.EmailField()
    exam_title = models.CharField(max_length=300)
    
    # File upload with validation
    answer_file = models.FileField(
        upload_to='student_answers/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    additional_notes = models.TextField(blank=True)
    
    # Teacher evaluation
    evaluated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='evaluated_exams')
    teacher_comments = models.TextField(blank=True)
    obtained_marks = models.FloatField(default=0)
    total_marks = models.FloatField(default=100)
    percentage = models.FloatField(default=0)
    grade = models.CharField(max_length=10, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.IntegerField(default=0, help_text="Time taken in minutes")
    
    # New Evaluation fields (merged from your code)
    marking_data = models.JSONField(null=True, blank=True, help_text="Teacher's markings on answer sheet")
    marked_answer_sheet = models.FileField(upload_to='marked_answer_sheets/', null=True, blank=True)
    question_marks = models.JSONField(null=True, blank=True, help_text="Marks for each question")
    
    # New evaluation status field
    evaluation_status = models.CharField(max_length=20, choices=EVALUATION_STATUS, default='pending')
    
    # New Feedback fields
    overall_feedback = models.TextField(null=True, blank=True)
    detailed_feedback = models.JSONField(null=True, blank=True, help_text="Question-wise feedback")
    
    # New Score fields (keeping both old and new for compatibility)
    total_possible_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Student Exam Submission"
        verbose_name_plural = "Student Exam Submissions"
        indexes = [
            models.Index(fields=['status', 'submitted_at']),
            models.Index(fields=['student', 'status']),
            models.Index(fields=['evaluation_status']),
            models.Index(fields=['student', 'evaluation_status']),
        ]
    
    def __str__(self):
        return f"{self.student_name} - {self.exam_title} ({self.status})"
    
    @property
    def paper(self):
        """Get the paper object regardless of type"""
        return self.generated_paper or self.question_paper
    
    @property
    def is_pending(self):
        return self.status == 'submitted'
    
    @property
    def is_evaluated(self):
        """Check if submission is evaluated (using new evaluation_status field)"""
        return self.evaluation_status in ['evaluated', 'published']
    
    @property
    def is_published_to_student(self):
        """Check if evaluation is published to student"""
        return self.evaluation_status == 'published'
    
    @property
    def file_type(self):
        if self.answer_file:
            ext = self.answer_file.name.split('.')[-1].upper()
            if ext in ['JPG', 'JPEG', 'PNG']:
                return 'IMAGE'
            elif ext == 'PDF':
                return 'PDF'
            elif ext in ['DOC', 'DOCX']:
                return 'DOCUMENT'
        return None
    
    @property
    def file_extension(self):
        if self.answer_file:
            return self.answer_file.name.split('.')[-1].lower()
        return None
    
    def calculate_percentage(self):
        """Calculate percentage based on marks"""
        if self.total_marks > 0:
            return (self.obtained_marks / self.total_marks) * 100
        return 0
    
    def determine_grade(self, percentage=None):
        """Determine grade based on percentage"""
        if percentage is None:
            percentage = self.calculate_percentage()
        
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def save(self, *args, **kwargs):
        # Sync old and new percentage fields
        if self.total_marks > 0 and self.obtained_marks > 0:
            self.percentage = self.calculate_percentage()
            
            # Sync marks_obtained and total_possible_marks from obtained_marks and total_marks
            self.marks_obtained = self.obtained_marks
            self.total_possible_marks = self.total_marks
            
            # Auto-calculate grade if not provided
            if not self.grade:
                self.grade = self.determine_grade(self.percentage)
        
        # Sync old and new evaluation status
        if self.status == 'evaluated' and self.evaluation_status == 'pending':
            self.evaluation_status = 'evaluated'
        
        # Set evaluated_at timestamp when status changes to evaluated
        if self.status == 'evaluated' and not self.evaluated_at:
            self.evaluated_at = timezone.now()
        
        # Also set evaluated_at when evaluation_status is 'evaluated' or 'published'
        if self.evaluation_status in ['evaluated', 'published'] and not self.evaluated_at:
            self.evaluated_at = timezone.now()
        
        super().save(*args, **kwargs)

class StudentAnswer(models.Model):
    """Store individual student answers for each question"""
    submission = models.ForeignKey(
        StudentExamSubmission, 
        on_delete=models.CASCADE, 
        related_name='answers'  # Changed from 'student_answers'
    )
    
    # Question info
    question_number = models.IntegerField(default=0)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50)
    marks_allotted = models.IntegerField(default=1)
    
    # Student's answer
    student_answer = models.TextField()
    
    # Teacher evaluation
    is_evaluated = models.BooleanField(default=False)
    evaluated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='evaluated_answers'  # Add related_name
    )
    evaluated_at = models.DateTimeField(null=True, blank=True)
    
    marks_awarded = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    teacher_comments = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['question_number']
        verbose_name = "Student Answer"
        verbose_name_plural = "Student Answers"
    
    def __str__(self):
        return f"Q{self.question_number} - {self.submission.student.username}"
    

class TeacherNotification(models.Model):
    """Notifications for teachers about new submissions"""
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='teacher_notifications'
    )
    submission = models.ForeignKey(
        StudentExamSubmission, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Teacher Notification"
        verbose_name_plural = "Teacher Notifications"
    
    def __str__(self):
        return f"Notification for {self.teacher.username}"
    



class StudentNotification(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_notifications')
    submission = models.ForeignKey(StudentExamSubmission, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('exam_evaluated', 'Exam Evaluated'),
        ('new_exam', 'New Exam Available'),
        ('reminder', 'Reminder'),
        ('general', 'General'),
    ])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.student.username} - {self.notification_type}"
    
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Add these models to your models.py file

class AutoExamPaper(models.Model):
    """
    Auto-generated exam paper - connects to your existing GeneratedQuestionPaper model
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    ]
    
    # Link to your existing GeneratedQuestionPaper model
    generated_paper = models.OneToOneField(
        'GeneratedQuestionPaper', 
        on_delete=models.CASCADE, 
        related_name='auto_exam_metadata',
        null=True, 
        blank=True
    )
    
    # Teacher who created this
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='auto_exams_created',
        limit_choices_to={'user_type': 5}  # MainStaff
    )
    
    # Exam parameters
    subject = models.CharField(max_length=100)
    total_marks = models.FloatField()
    duration = models.IntegerField(help_text="Duration in minutes")
    total_questions = models.IntegerField()
    
    # Section distribution (using your existing question types)
    mcq_count = models.IntegerField(default=0)
    mcq_marks = models.FloatField(default=1)
    short_count = models.IntegerField(default=0)
    short_marks = models.FloatField(default=3)
    long_count = models.IntegerField(default=0)
    long_marks = models.FloatField(default=5)
    vlong_count = models.IntegerField(default=0)
    vlong_marks = models.FloatField(default=10)
    
    # Difficulty distribution
    difficulty_distribution = models.CharField(max_length=50, default='balanced')
    
    # Topic filters
    topics = models.TextField(blank=True, help_text="Comma-separated topics to include")
    exclude_topics = models.TextField(blank=True, help_text="Comma-separated topics to exclude")
    
    # Settings
    randomize_order = models.BooleanField(default=True)
    include_answer_key = models.BooleanField(default=True)
    avoid_recent_questions = models.BooleanField(default=False, 
        help_text="Avoid questions used in last 30 days")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Auto Exam Paper"
        verbose_name_plural = "Auto Exam Papers"
    
    def __str__(self):
        return f"{self.subject} - {self.total_marks} marks ({self.created_at.date()})"
    
    @property
    def is_published(self):
        return self.status == 'PUBLISHED'
    
    @property
    def question_count_by_type(self):
        """Get question count by type"""
        counts = self.autoexamselection_set.values('question_type').annotate(
            count=models.Count('id')
        )
        return {item['question_type']: item['count'] for item in counts}


class AutoExamSelection(models.Model):
    """
    Tracks which questions were selected for an auto-generated exam
    """
    auto_exam = models.ForeignKey(
        AutoExamPaper, 
        on_delete=models.CASCADE, 
        related_name='question_selections'
    )
    
    # Generic foreign key to handle different question types
    content_type = models.ForeignKey(
        'contenttypes.ContentType', 
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ['biologyquestion', 'chemistryquestion', 
                         'physicsquestion', 'mathematicsquestion']
        }
    )
    object_id = models.PositiveIntegerField()
    question = GenericForeignKey('content_type', 'object_id')
    
    # Question metadata at time of selection
    question_number = models.IntegerField()
    section = models.CharField(max_length=20)  # MCQ, SHORT, LONG, VLONG
    marks = models.FloatField()
    difficulty = models.CharField(max_length=10)  # EASY, MEDIUM, HARD
    
    # Link to your existing GeneratedQuestionPaper if needed
    generated_paper_question = models.ForeignKey(
        'Question',  # Your existing Question model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='auto_exam_selections'
    )
    
    class Meta:
        ordering = ['question_number']
        verbose_name = "Auto Exam Question Selection"
        verbose_name_plural = "Auto Exam Question Selections"
    
    def __str__(self):
        return f"Q{self.question_number} - {self.section}"


class AutoExamTemplate(models.Model):
    """
    Save auto exam configurations as templates for reuse
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='auto_exam_templates'
    )
    
    # Exam parameters
    subject = models.CharField(max_length=100)
    total_marks = models.FloatField()
    duration = models.IntegerField()
    total_questions = models.IntegerField()
    
    # Section distribution
    mcq_count = models.IntegerField(default=0)
    mcq_marks = models.FloatField(default=1)
    short_count = models.IntegerField(default=0)
    short_marks = models.FloatField(default=3)
    long_count = models.IntegerField(default=0)
    long_marks = models.FloatField(default=5)
    vlong_count = models.IntegerField(default=0)
    vlong_marks = models.FloatField(default=10)
    
    # Settings
    difficulty_distribution = models.CharField(max_length=50, default='balanced')
    randomize_order = models.BooleanField(default=True)
    include_answer_key = models.BooleanField(default=True)
    avoid_recent_questions = models.BooleanField(default=False)
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-usage_count', '-created_at']
        verbose_name = "Auto Exam Template"
        verbose_name_plural = "Auto Exam Templates"
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.total_marks} marks)"


class QuestionUsageLog(models.Model):
    """
    Track when questions are used in exams
    """
    # Generic foreign key for different question types
    content_type = models.ForeignKey(
        'contenttypes.ContentType', 
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    question = GenericForeignKey('content_type', 'object_id')
    
    auto_exam = models.ForeignKey(
        AutoExamPaper, 
        on_delete=models.CASCADE,
        related_name='usage_logs',
        null=True,
        blank=True
    )
    
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-used_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['used_at']),
        ]
    
    def __str__(self):
        return f"Question {self.object_id} used on {self.used_at.date()}"
from django.contrib import admin


class Package(models.Model):

    PACKAGE_TYPES = (
        ('jee', 'JEE'),
        ('neet', 'NEET'),
        ('foundation', 'Foundation'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=PACKAGE_TYPES)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)

    validity = models.IntegerField(help_text="Validity in months")

    description = models.TextField(blank=True)

    # ADD THESE FIELDS
    features = models.TextField(blank=True)
    subjects = models.TextField(blank=True)

    badge = models.CharField(max_length=100, blank=True)
    image = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    display_order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    # FEATURE LIST
    def get_features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []

    # SUBJECT LIST
    def get_subjects_list(self):
        if self.subjects:
            return [s.strip() for s in self.subjects.split(',') if s.strip()]
        return []

    def __str__(self):
        return self.name
    
class PackagePurchase(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='package_purchases')
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.package.name}"
    
    class Meta:
        ordering = ['-purchase_date']
        
