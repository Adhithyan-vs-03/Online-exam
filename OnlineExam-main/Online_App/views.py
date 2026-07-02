from time import timezone
from django.shortcuts import render ,redirect, get_object_or_404,HttpResponse
from .models import User
from django.contrib.auth import authenticate ,login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db import IntegrityError,transaction
from django.contrib import messages
from Online_App.models import User,Staff,Student,ExamSchedule,MainStaff,Subject
from .models import Staff, Student,ExamDetail,BiologyQuestion, ChemistryQuestion,PhysicsQuestion,MathematicsQuestion,StudentExamSubmission
from .models import ExamSchedule, PackagePurchase,StudentMarks, ExamDetail,Feedback_review,QuestionPaper,ExamResult,TeacherNotification
from examapp.models import StudentProfile,Product, Order,Payment,Exam,Question,Option,UserAnswer
from datetime import datetime
from examapp.forms import PurchaseForm,PaymentForm
from django.urls import reverse
from django.db import transaction
from .forms import AddPackageForm,QuestionPaperForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now, timedelta
from django.db.models import Q 
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

# Online_App/views.py - CORRECTED IMPORTS
from time import timezone
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError, transaction
from django.contrib import messages
from datetime import datetime

# CORRECT: Import your custom User model
from .models import User, Staff, Student, ExamSchedule, MainStaff, Subject

# ... rest of your imports
from .models import Staff, Student, ExamDetail, BiologyQuestion, ChemistryQuestion, PhysicsQuestion, MathematicsQuestion, StudentExamSubmission
from .models import ExamSchedule, PackagePurchase, StudentMarks, ExamDetail, Feedback_review, QuestionPaper, ExamResult, TeacherNotification
from examapp.models import StudentProfile, Product, Order, Payment, Exam, Question, Option, UserAnswer
from examapp.forms import PurchaseForm, PaymentForm
from django.urls import reverse
from .forms import AddPackageForm, QuestionPaperForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now, timedelta
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from Online_App.models import Student 

# ... rest of your code

def Index(request):
    return render(request, 'index.html')


from django.shortcuts import render, redirect
from .models import User 
from django.contrib import messages
from datetime import date

from .models import Staff, Student, MainStaff , StudentExamSubmission


from django.shortcuts import render, redirect
from .models import User 
from django.contrib import messages
from datetime import date

from .models import Staff, Student, MainStaff


from .models import User 
from django.contrib import messages
from datetime import date
from .models import Student, Staff, MainStaff



def Register(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        user_type = int(request.POST.get('usertype'))
        mobile = request.POST.get('mobile')

        # PASSWORD CHECK
        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('Register')

        # USERNAME CHECK
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('Register')

        # EMAIL CHECK
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('Register')

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            user_type=user_type
        )

        # ACCOUNT TYPE CHECK
        if user_type == 2:  # STAFF
            Staff.objects.create(
                user=user,
                first_name=first_name,
                email=email,
                contact=mobile,
                created_type="self"
            )

        elif user_type == 4:  # STUDENT
            Student.objects.create(
                user=user,
                name=first_name,
                email=email,
                phone_number=mobile,
                guardian_name="",
                guardian_number="",
                created_type="self"
            )

        elif user_type == 5:  # MAIN STAFF
            MainStaff.objects.create(
                user=user,
                name=first_name,
                email=email,
                joined_date=date.today()
            )

        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'register.html')



def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            elif user.user_type == 2:
                return redirect('Teacher')

            elif user.user_type == 3:
                return redirect('Parent')

            elif user.user_type == 4:
                return redirect('Student')

            elif user.user_type == 5:
                return redirect('mainstaff_dashboard')

        messages.error(request, "Invalid credentials.")
        return redirect('login')

    return render(request, 'login.html')


from .models import Subject, Chapter, Topic, SubTopic

def mainstaff_dashboard(request):

    total_subjects = Subject.objects.count()
    total_chapters = Chapter.objects.count()
    total_topics = Topic.objects.count()
    total_subtopics = SubTopic.objects.count()

    return render(request, "mainstaff/mainstaff_dashboard.html", {
        "total_subjects": total_subjects,
        "total_chapters": total_chapters,
        "total_topics": total_topics,
        "total_subtopics": total_subtopics,
    })


def mainstaff_profile(request):
    user = request.user  # Logged-in user

    return render(request, "mainstaff/mainstaff_profile.html", {"user": user})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MainStaff
from .models import User 

@login_required
def mainstaff_profile(request):
    # make sure only mainstaff can access (optional)
    # if request.user.user_type != 5: return redirect('somewhere')

    try:
        mainstaff = request.user.mainstaff
    except MainStaff.DoesNotExist:
        mainstaff = MainStaff.objects.create(user=request.user, name=request.user.get_full_name(), email=request.user.email)

    return render(request, 'mainstaff/mainstaff_profile.html', {'mainstaff': mainstaff, 'user': request.user})


def mainstaff_edit_profile(request):
    mainstaff = MainStaff.objects.get(user=request.user)

    if request.method == "POST":
        mainstaff.name = request.POST.get("name")
        mainstaff.email = request.POST.get("email")
        mainstaff.phone = request.POST.get("phone")
        mainstaff.joined_date = request.POST.get("joined_date")

        if request.FILES.get("profile_photo"):
            mainstaff.profile_photo = request.FILES.get("profile_photo")

        mainstaff.save()
        return redirect('mainstaff_profile')

    return render(request, "mainstaff/mainstaff_edit_profile.html", {"mainstaff": mainstaff})


@login_required
def mainstaff_update_photo(request):
    if request.method == 'POST':
        try:
            mainstaff = request.user.mainstaff
        except MainStaff.DoesNotExist:
            mainstaff = MainStaff.objects.create(user=request.user)

        photo = request.FILES.get('profile_photo')
        if photo:
            mainstaff.profile_photo = photo
            mainstaff.save()
            messages.success(request, "Profile photo updated.")
        else:
            messages.error(request, "No file selected.")
    return redirect('mainstaff_profile')



from .models import SchoolClass, Subject, Chapter, Topic, SubTopic

def add_class(request):
    class_list = list(range(1, 13))  # For placeholder

    # Load all data for dropdowns (IMPORTANT!)
    classes = SchoolClass.objects.all()
    subjects = Subject.objects.all()
    chapters = Chapter.objects.all()
    topics = Topic.objects.all()
    subtopics = SubTopic.objects.all()

    if request.method == "POST":
        class_value = request.POST.get("class_name")

        # If adding a class
        if class_value:
            if SchoolClass.objects.filter(class_name=class_value).exists():
                return render(request, "mainstaff/add_class.html", {
                    "class_list": class_list,
                    "classes": classes,
                    "subjects": subjects,
                    "chapters": chapters,
                    "topics": topics,
                    "subtopics": subtopics,
                    "error": f"{class_value} already exists!"
                })

            SchoolClass.objects.create(class_name=class_value)

            # Reload after saving
            classes = SchoolClass.objects.all()

            return render(request, "mainstaff/add_class.html", {
                "class_list": class_list,
                "classes": classes,
                "subjects": subjects,
                "chapters": chapters,
                "topics": topics,
                "subtopics": subtopics,
                "message": "Class added successfully!"
            })

    # GET request
    return render(request, "mainstaff/add_class.html", {
        "class_list": class_list,
        "classes": classes,
        "subjects": subjects,
        "chapters": chapters,
        "topics": topics,
        "subtopics": subtopics,
    })




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SchoolClass, Subject, Chapter, Topic, SubTopic ,Course , QuestionImage

# def manage_subjects(request):

#     # SAVE CLASS
#     if request.method == "POST" and "class_name" in request.POST:
#         class_name = request.POST.get("class_name")
#         if class_name:
#             SchoolClass.objects.create(class_name=class_name)

#     context = {
#         'classes': SchoolClass.objects.all(),
#         'subjects': Subject.objects.all(),
#         'chapters': Chapter.objects.all(),
#         'topics': Topic.objects.all(),
#         'subtopics': SubTopic.objects.all(),
#     }
#     return render(request, "mainstaff/manage_subjects.html", context)

# def manage_subjects(request):

#     # SAVE CLASS
#     if request.method == "POST" and "class_name" in request.POST:
#         class_name = request.POST.get("class_name")
#         if class_name:
#             SchoolClass.objects.create(class_name=class_name)
#         return redirect("manage_subjects")   # 🔥 important

#     context = {
#         'classes': SchoolClass.objects.all(),
#         'subjects': Subject.objects.all(),
#         'chapters': Chapter.objects.all(),
#         'topics': Topic.objects.all(),
#         'subtopics': SubTopic.objects.all(),
#     }
#     return render(request, "mainstaff/manage_subjects.html", context)


def manage_subjects(request):

    # SAVE COURSE
    if request.method == "POST" and "course_name" in request.POST:
        course_name = request.POST.get("course_name")
        if course_name:
            Course.objects.create(name=course_name)
        return redirect("manage_subjects")

    # SAVE CLASS
    if request.method == "POST" and "class_name" in request.POST:
        class_name = request.POST.get("class_name")
        course_id = request.POST.get("course_id")
        if class_name and course_id:
            SchoolClass.objects.create(class_name=class_name, course_id=course_id)
        return redirect("manage_subjects")

    context = {
        'courses': Course.objects.all(),
        'classes': SchoolClass.objects.all(),
        'subjects': Subject.objects.all(),
        'chapters': Chapter.objects.all(),
        'topics': Topic.objects.all(),
        'subtopics': SubTopic.objects.all(),
    }
    return render(request, "mainstaff/manage_subjects.html", context)


from django.shortcuts import redirect
from django.contrib import messages
from .models import QuestionImage, Subject

# def upload_question_image(request):
#     if request.method == "POST":
#         subject_id = request.POST.get("subject_id")
#         image = request.FILES.get("question_image")

#         if not image:
#             messages.error(request, "Please upload an image.")
#             return redirect("manage_subjects")

#         try:
#             subject = Subject.objects.get(id=subject_id)
#         except Subject.DoesNotExist:
#             messages.error(request, "Invalid subject.")
#             return redirect("manage_subjects")

#         QuestionImage.objects.create(subject=subject, image=image)

#         messages.success(request, "Question image uploaded successfully!")

#         return redirect("manage_subjects")

#     return redirect("manage_subjects")

def upload_question_image(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        image = request.FILES.get("question_image")
        
        print(f"DEBUG - Subject ID from form: {subject_id}")
        print(f"DEBUG - Image file name: {image.name if image else 'No image'}")
        
        if not image:
            messages.error(request, "Please upload an image.")
            return redirect("manage_subjects")

        if not subject_id:
            messages.error(request, "Please select a subject.")
            return redirect("manage_subjects")

        try:
            subject = Subject.objects.get(id=subject_id)
            print(f"DEBUG - Found subject: {subject.name} (ID: {subject.id})")
        except Subject.DoesNotExist:
            messages.error(request, f"Invalid subject ID: {subject_id}")
            return redirect("manage_subjects")
        except ValueError as e:
            messages.error(request, f"Invalid subject ID format: {subject_id}. Error: {e}")
            return redirect("manage_subjects")

        # Create and print confirmation
        question_image = QuestionImage.objects.create(subject=subject, image=image)
        print(f"DEBUG - Created QuestionImage ID: {question_image.id}")
        print(f"DEBUG - Subject ID saved: {question_image.subject.id}")
        print(f"DEBUG - Subject Name: {question_image.subject.name}")
        
        messages.success(request, f"Question image uploaded successfully for {subject.name}!")
        return redirect("manage_subjects")

    return redirect("manage_subjects")


# Online_App/views.py
from django.shortcuts import render, get_object_or_404
from .models import SchoolClass, Subject, Chapter, Topic, SubTopic

def class_list(request):
    classes = SchoolClass.objects.all().order_by('id')
    return render(request, "mainstaff/class_list.html", {"classes": classes})


def class_details(request, class_id):
    class_obj = get_object_or_404(SchoolClass, id=class_id)

    subjects = Subject.objects.filter(class_name=class_obj)
    chapters = Chapter.objects.filter(subject__class_name=class_obj)
    topics = Topic.objects.filter(chapter__subject__class_name=class_obj)
    subtopics = SubTopic.objects.filter(topic__chapter__subject__class_name=class_obj)

    return render(request, "mainstaff/class_detail.html", {
        "class_obj": class_obj,
        "subjects": subjects,
        "chapters": chapters,
        "topics": topics,
        "subtopics": subtopics,
    })




from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages

def add_subject(request):
    if request.method == "POST":
        class_id = request.POST.get("class_id")
        subject_name = request.POST.get("subject_name", "").strip()

        if not class_id:
            messages.error(request, "Please select a class.")
            return redirect(request.META.get("HTTP_REFERER"))

        classroom = get_object_or_404(SchoolClass, id=class_id)

        subject, created = Subject.objects.get_or_create(
            class_name=classroom,
            name=subject_name
        )

        if created:
            messages.success(request, f"Subject '{subject.name}' added successfully.")
        else:
            messages.info(request, f"Subject '{subject.name}' already exists.")

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect("manage_subjects")



def add_chapter(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        chapter_name = request.POST.get("chapter_name", "").strip()

        if not subject_id or not chapter_name:
            messages.error(request, "Please select a subject and enter a chapter name.")
            return redirect("manage_subjects")

        # Debug: check received data
        print("Received subject_id:", subject_id)
        print("Received chapter_name:", chapter_name)

        # Fetch the Subject object
        subject = get_object_or_404(Subject, id=subject_id)

        # Create chapter
        chapter, created = Chapter.objects.get_or_create(
            subject=subject,
            name=chapter_name
        )

        if created:
            messages.success(request, f"Chapter '{chapter.name}' added successfully.")
        else:
            messages.info(request, f"Chapter '{chapter.name}' already exists.")

        return redirect("manage_subjects")

    # If GET request, just redirect
    return redirect("manage_subjects")




def add_topic(request):
    if request.method == "POST":
        chapter_id = request.POST.get("chapter_id")
        topic_name = request.POST.get("topic_name", "").strip()

        chapter = get_object_or_404(Chapter, id=chapter_id)

        topic, created = Topic.objects.get_or_create(
            chapter=chapter,
            name=topic_name
        )

        if created:
            messages.success(request, f"Topic '{topic.name}' added.")
        else:
            messages.info(request, "Topic already exists.")

    return redirect("manage_subjects")


def add_subtopic(request):
    if request.method == "POST":
        topic_id = request.POST.get("topic_id")
        subtopic_name = request.POST.get("subtopic_name", "").strip()

        topic = get_object_or_404(Topic, id=topic_id)

        subtopic, created = SubTopic.objects.get_or_create(
            topic=topic,
            name=subtopic_name
        )

        if created:
            messages.success(request, f"Subtopic '{subtopic.name}' added.")
        else:
            messages.info(request, "Subtopic already exists.")

    return redirect("manage_subjects")

import json
import re
import PyPDF2
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import SchoolClass, Subject, Chapter, Topic, SubTopic, ContentSource
from django.conf import settings

# Load API key from settings or environment
HF_API_KEY = getattr(settings, 'HF_API_KEY', os.getenv("HF_API_KEY"))

# HuggingFace Router API endpoint
HF_ROUTER_URL = "https://router.huggingface.co/v1/completions"

def call_huggingface_simple(prompt):
    """
    Simple HuggingFace API call that should work with free tier
    """
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Try with GPT-2 which is always available and free
    data = {
        "model": "gpt2",  # Always available free model
        "prompt": prompt,
        "max_tokens": 400,
        "temperature": 0.3,
        "top_p": 0.9,
        "stream": False
    }
    
    try:
        response = requests.post(HF_ROUTER_URL, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["text"]
            else:
                return "{}"  # Return empty JSON as fallback
        else:
            # Try a different approach - use chat completion if completion fails
            return call_huggingface_chat(prompt)
            
    except Exception as e:
        print(f"API call error: {str(e)}")
        return "{}"  # Return empty JSON

def call_huggingface_chat(prompt):
    """
    Alternative using chat completion endpoint
    """
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Try chat endpoint
    chat_url = "https://router.huggingface.co/v1/chat/completions"
    
    data = {
        "model": "microsoft/DialoGPT-small",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(chat_url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
        return "{}"
    except:
        return "{}"

def extract_json_from_text(text):
    """
    Try to extract JSON from text
    """
    if not text:
        return None
    
    # Clean the text
    text = text.strip()
    
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```\s*', '', text)
    
    # Try to find JSON
    try:
        # First, try to parse the whole text as JSON
        json_data = json.loads(text)
        return json.dumps(json_data)
    except:
        pass
    
    # Try to find JSON object between { and }
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1 and end > start:
        json_str = text[start:end+1]
        try:
            json.loads(json_str)
            return json_str
        except:
            pass
    
    return None

@csrf_exempt
@login_required
def ai_process_content(request):
    """
    Process PDF and return structured data
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"})

    if not HF_API_KEY:
        return JsonResponse({
            "success": False,
            "error": "HuggingFace API key not found. Please add HF_API_KEY to your .env file"
        })

    try:
        # Get form data
        pdf_file = request.FILES.get('pdf_file')
        source_type = request.POST.get('source_type')
        class_id = request.POST.get('class_id')
        subject_id = request.POST.get('subject_id')

        if not all([pdf_file, source_type, class_id, subject_id]):
            return JsonResponse({
                "success": False,
                "error": "Missing required fields"
            })

        # Read PDF
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = ""
            for page_num, page in enumerate(pdf_reader.pages[:2]):  # Only first 2 pages
                text = page.extract_text()
                if text:
                    pdf_text += f"Page {page_num + 1}:\n{text}\n\n"
                    
            if len(pdf_text) > 1500:  # Limit for free API
                pdf_text = pdf_text[:1500]
                
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": f"Failed to read PDF: {str(e)}"
            })

        if not pdf_text.strip():
            return JsonResponse({
                "success": False,
                "error": "No text found in PDF"
            })

        # Create a VERY simple prompt
        prompt = f"""Please create a JSON structure from this educational content. Return ONLY JSON with this format:
{{
"book_title": "Book Name",
"chapters": [
{{
"chapter_number": 1,
"chapter_title": "Chapter Name",
"topics": [
{{
"topic_heading": "Topic Name",
"subtopics": ["Subtopic 1", "Subtopic 2"],
"key_concepts": ["Concept 1", "Concept 2"]
}}
]
}}
]
}}

Content: {pdf_text}

JSON:"""

        # Call API
        ai_response = call_huggingface_simple(prompt)
        
        # Try to extract JSON
        json_str = extract_json_from_text(ai_response)
        
        if json_str:
            try:
                structured_data = json.loads(json_str)
            except:
                structured_data = None
        else:
            structured_data = None
        
        # If no valid JSON, create a simple structure
        if not structured_data:
            # Extract potential chapter titles (lines that look like headings)
            lines = pdf_text.split('\n')
            possible_titles = []
            for line in lines:
                line = line.strip()
                if (len(line) > 10 and len(line) < 100 and 
                    not line.isdigit() and 
                    not line.startswith('Page')):
                    possible_titles.append(line)
            
            # Create structure
            structured_data = {
                "book_title": pdf_file.name.replace('.pdf', ''),
                "chapters": []
            }
            
            # Add up to 3 chapters
            for i, title in enumerate(possible_titles[:3]):
                structured_data["chapters"].append({
                    "chapter_number": i + 1,
                    "chapter_title": title[:100],
                    "topics": [
                        {
                            "topic_heading": f"Main Topic {i+1}",
                            "subtopics": ["Introduction", "Key Points"],
                            "key_concepts": ["Basic Concepts", "Important Terms"]
                        }
                    ]
                })
            
            # If no titles found, add at least one chapter
            if not structured_data["chapters"]:
                structured_data["chapters"].append({
                    "chapter_number": 1,
                    "chapter_title": "Introduction",
                    "topics": [
                        {
                            "topic_heading": "Main Content",
                            "subtopics": ["Overview", "Summary"],
                            "key_concepts": ["Key Ideas", "Main Points"]
                        }
                    ]
                })

        return JsonResponse({
            "success": True,
            "structured_data": structured_data,
            "book_title": structured_data.get("book_title", "Unknown"),
            "chapters_count": len(structured_data.get("chapters", []))
        })

    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            "success": False,
            "error": f"Processing error: {str(e)}"
        })

@login_required
def save_ai_content(request):
    """
    Save AI processed content to database
    """
    if request.method == "POST":
        try:
            structured_data_str = request.POST.get('structured_data')
            class_id = request.POST.get('class_id')
            subject_id = request.POST.get('subject_id')
            source_type = request.POST.get('source_type')

            if not all([structured_data_str, class_id, subject_id, source_type]):
                messages.error(request, "Missing required data.")
                return redirect('manage_subjects')

            # Parse data
            try:
                data = json.loads(structured_data_str)
            except json.JSONDecodeError:
                messages.error(request, "Invalid data format.")
                return redirect('manage_subjects')

            # Get class and subject
            try:
                classroom = SchoolClass.objects.get(id=class_id)
                subject = Subject.objects.get(id=subject_id)
            except (SchoolClass.DoesNotExist, Subject.DoesNotExist):
                messages.error(request, "Class or subject not found.")
                return redirect('manage_subjects')

            # Save chapters, topics, subtopics
            chapters_created = topics_created = subtopics_created = 0

            for chapter_data in data.get('chapters', []):
                # Create or get chapter
                chapter, created = Chapter.objects.get_or_create(
                    subject=subject,
                    name=chapter_data.get('chapter_title', 'Untitled')[:200],
                    defaults={
                        'order': chapter_data.get('chapter_number', 0)
                    }
                )
                if created:
                    chapters_created += 1

                # Create topics
                for topic_data in chapter_data.get('topics', []):
                    topic_name = topic_data.get('topic_heading', '').strip()
                    if topic_name:
                        topic, created = Topic.objects.get_or_create(
                            chapter=chapter,
                            name=topic_name[:200]
                        )
                        if created:
                            topics_created += 1

                        # Create subtopics
                        for subtopic_name in topic_data.get('subtopics', []):
                            if subtopic_name and str(subtopic_name).strip():
                                subtopic, created = SubTopic.objects.get_or_create(
                                    topic=topic,
                                    name=str(subtopic_name).strip()[:200]
                                )
                                if created:
                                    subtopics_created += 1

            # Save the source
            ContentSource.objects.create(
                name=data.get('book_title', f'AI Imported {source_type}'),
                source_type=source_type,
                class_name=classroom,
                subject=subject,
                processed_data=data
            )

            messages.success(
                request,
                f"Successfully imported {chapters_created} chapters, "
                f"{topics_created} topics, and {subtopics_created} subtopics."
            )

        except Exception as e:
            messages.error(request, f"Error saving: {str(e)}")

    return redirect('manage_subjects')



def ai_content_importer(request):
    # Get classes and subjects for the dropdowns
    classes = SchoolClass.objects.all().order_by('class_name')
    subjects = Subject.objects.all().order_by('name')
    
    context = {
        'classes': classes,
        'subjects': subjects,
    }
    
    return render(request, 'mainstaff/importer.html', context)



from .models import StaffNotification

def notifications_page(request):
    notifications = StaffNotification.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "mainstaff/notifications.html", {
        "notifications": notifications
    })


def subject_added(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    return render(request, "mainstaff/subject_added.html", {"subject": subject})



from django.shortcuts import render
from .models import Question, SchoolClass, Subject

def add_questions(request):
    classes = SchoolClass.objects.all()       # For dropdown
    subjects = Subject.objects.all()          # For dropdown
    
    if request.method == "POST":
        class_name = request.POST.get("class_name")
        subject_name = request.POST.get("subject_name")
        chapter = request.POST.get("chapter")
        topic = request.POST.get("topic")
        sub_topic = request.POST.get("sub_topic")
        marks = request.POST.get("marks")
        question_type = request.POST.get("question_type")
        question_text = request.POST.get("question_text")
        answer_text = request.POST.get("answer_text")

        Question.objects.create(
            class_name = class_name,
            subject_name = subject_name,
            chapter = chapter,
            topic = topic,
            sub_topic = sub_topic,
            marks = marks,
            question_type = question_type,
            question_text = question_text,
            answer_text = answer_text
        )

        return render(request, "mainstaff/add_questions.html", {
            "classes": classes,
            "subjects": subjects,
            "success": "Question Added Successfully!"
        })

    return render(request, "mainstaff/add_questions.html", {
        "classes": classes,
        "subjects": subjects
    })




# --------------------------------------------Admin---------------------------------------------------------------------


# Function to check if the user is a superuser
def is_superuser(user):
    return user.is_authenticated and user.is_superuser  # Ensures only superusers can access

@login_required(login_url='Login')
@user_passes_test(is_superuser, login_url='Login')
# Redirect unauthorized users
def admin_dashboard(request):
    exams = ExamSchedule.objects.all()  # Fetch exam details
    total_staff = Staff.objects.count()  # Get total number of staff
    total_student = StudentProfile.objects.count() + Student.objects.count() # Get total number of students

    context = {
        'data': {'username': request.user.username},  
        'exams': exams,  
        'total_staff': total_staff,  
        'total_student': total_student  
    }
    return render(request, 'Admin/admin-dashboard.html', context)

# Staff
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from .models import Staff

User = get_user_model()

def add_staff(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        subject = request.POST['subject']
        dob = request.POST['dob']
        contact = request.POST['contact']
        address = request.POST['address']

        # NEW: Admin enters username & password
        username = request.POST['username']
        password = request.POST['password']

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        # Create staff profile
        Staff.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            dob=dob,
            contact=contact,
            address=address,
            created_type='admin'
        )

        # SEND EMAIL WITH ENTERED CREDENTIALS
        send_mail(
            subject="Your Staff Login Credentials",
            message=f"""
Hello {first_name},

Your staff account has been created successfully.

Login Details:
------------------------
Username: {username}
Password: {password}

Please log in and update your password.

Thank you.
            """,
            from_email="youremail@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('admin_staff_list')

    staff_list = Staff.objects.all()
    return render(request, "Admin/add_staff.html", {"staff_list": staff_list})




@login_required
def admin_staff_list(request):
    query = request.GET.get('q', '')
    
    if query:
        staff_members = Staff.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(subject__icontains=query) |
            Q(contact__icontains=query)
        ).distinct()
    else:
        staff_members = Staff.objects.all()
    
    return render(request, 'Admin/admin_staff_list.html', {
        'staff_members': staff_members,
        'search_query': query
    })


@login_required
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    
    if request.method == "POST":
        # Update staff details
        staff.first_name = request.POST.get('first_name', staff.first_name)
        staff.last_name = request.POST.get('last_name', staff.last_name)
        staff.email = request.POST.get('email', staff.email)
        staff.subject = request.POST.get('subject', staff.subject)
        staff.contact = request.POST.get('contact', staff.contact)
        staff.address = request.POST.get('address', staff.address)
        staff.save()
        
        # Also update the associated user's email if changed
        if staff.user.email != staff.email:
            staff.user.email = staff.email
            staff.user.save()
        
        messages.success(request, "Staff member updated successfully!")
        return redirect('admin_staff_list')

    return render(request, 'Admin/edit_staff.html', {'staff': staff})








from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Subject, Question
import json

@login_required
def admin_dashboard(request):
    # Your existing dashboard code...
    # Add this to the context:
    subjects = Subject.objects.all().prefetch_related('class_name')
    total_questions = Question.objects.count()
    context = {
        'total_student': Student.objects.count(),
        'total_staff': Staff.objects.count(),
        'total_course': Course.objects.count(),
        'total_questions': Question.objects.count(),
        'data': request.user
    }
    return render(request, "admin/admin-dashboard.html", context)

from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import json

@login_required
def viewing_all_questions(request):
    """Render the separate page for viewing all questions"""
    subjects = Subject.objects.all().prefetch_related('class_name')
    total_questions = Question.objects.count()
    
    # Get selected subject from GET parameter or default to first subject
    selected_subject_id = request.GET.get('subject', '')
    
    context = {
        'subjects': subjects,
        'total_questions': total_questions,
        'user': request.user,
        'selected_subject_id': selected_subject_id
    }
    return render(request, "admin/viewing_all_questions.html", context)

@login_required
def get_all_questions(request):
    """API endpoint to get all questions with pagination and filtering"""
    try:
        # Get filter parameters
        subject_id = request.GET.get('subject', 'all')
        question_type = request.GET.get('type', 'all')
        difficulty = request.GET.get('difficulty', 'all')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        # Start with all questions
        questions = Question.objects.select_related('subject', 'subject__class_name').all()
        
        # Apply filters
        if subject_id and subject_id != 'all':
            questions = questions.filter(subject_id=subject_id)
        
        if question_type and question_type != 'all':
            questions = questions.filter(question_type=question_type)
        
        if difficulty and difficulty != 'all':
            questions = questions.filter(difficulty=difficulty)
        
        if search:
            questions = questions.filter(
                Q(question__icontains=search) |
                Q(chapter__icontains=search) |
                Q(topic__icontains=search) |
                Q(subject__name__icontains=search)
            )
        
        # Order by latest first
        questions = questions.order_by('-created_at')
        
        # Pagination
        paginator = Paginator(questions, per_page)
        page_obj = paginator.get_page(page)
        
        # Prepare response data
        questions_data = []
        for question in page_obj:
            questions_data.append({
                'id': question.id,
                'subject_id': question.subject.id if question.subject else None,
                'subject_name': question.subject.name if question.subject else 'No Subject',
                'chapter': question.chapter or '',
                'topic': question.topic or '',
                'question': question.question or '',
                'question_type': question.question_type or '',
                'marks': question.marks or 0,
                'difficulty': question.difficulty or 'medium',
                'option1': question.option1 or '',
                'option2': question.option2 or '',
                'option3': question.option3 or '',
                'option4': question.option4 or '',
                'correct_options': question.correct_options or '',
                'answer': question.answer or '',
                'match_items': question.match_items or '',
                'match_answers': question.match_answers or '',
                'blank_answers': question.blank_answers or '',
                'numerical_solution': question.numerical_solution or '',
                'final_answer': question.final_answer or '',
                'created_at': question.created_at.isoformat() if question.created_at else '',
                'created_by': question.created_by.username if question.created_by else 'Admin',
            })
        
        return JsonResponse({
            'success': True,
            'questions': questions_data,
            'total': paginator.count,
            'page': page,
            'per_page': per_page,
            'total_pages': paginator.num_pages
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'questions': []
        }, status=500)

@login_required
def get_question_detail(request, question_id):
    """API endpoint to get question details"""
    try:
        question = get_object_or_404(Question.objects.select_related('subject'), id=question_id)
        
        question_data = {
            'id': question.id,
            'subject_name': question.subject.name if question.subject else 'No Subject',
            'chapter': question.chapter or '',
            'topic': question.topic or '',
            'question': question.question or '',
            'question_type': question.question_type or '',
            'marks': question.marks or 0,
            'difficulty': question.difficulty or 'medium',
            'option1': question.option1 or '',
            'option2': question.option2 or '',
            'option3': question.option3 or '',
            'option4': question.option4 or '',
            'correct_options': question.correct_options or '',
            'answer': question.answer or '',
            'match_items': question.match_items or '',
            'match_answers': question.match_answers or '',
            'blank_answers': question.blank_answers or '',
            'numerical_solution': question.numerical_solution or '',
            'final_answer': question.final_answer or '',
            'created_at': question.created_at.isoformat() if question.created_at else '',
            'created_by': question.created_by.username if question.created_by else 'Admin',
        }
        
        return JsonResponse(question_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SchoolClass, Subject, Course, Chapter, Question

def question_paper_generator(request):
    # Check if editing an existing paper
    edit_paper_id = request.GET.get('edit', None)
    paper = None
    edit_mode = False
    
    if edit_paper_id:
        try:
            paper = GeneratedQuestionPaper.objects.get(id=edit_paper_id)
            edit_mode = True
        except GeneratedQuestionPaper.DoesNotExist:
            pass
    
    # Get all data
    subjects = Subject.objects.all().select_related('class_name')
    courses = Course.objects.all()
    school_classes = SchoolClass.objects.all()
    chapters = Chapter.objects.all()
    
    # Also get all questions to pass to template
    all_questions = Question.objects.all().select_related('subject')
    
    context = {
        'subjects': subjects,
        'courses': courses,
        'classes': school_classes,
        'chapters': chapters,
        'all_questions': all_questions[:50],
        'edit_mode': edit_mode,
        'paper': paper,
    }
    
    return render(request, 'Question_creation.html', context)



from django.http import JsonResponse
from .models import Question

def get_all_questions_api(request):
    """API endpoint to get all questions for AJAX"""
    try:
        questions = Question.objects.all().select_related('subject', 'subject__class_name')
        
        questions_data = []
        for question in questions:
            questions_data.append({
                'id': question.id,
                'subject_id': question.subject.id if question.subject else None,
                'subject_name': question.subject.name if question.subject else 'Unknown',
                'question': question.question,
                'type': question.question_type,
                'difficulty': question.difficulty,
                'marks': question.marks,
                'chapter': question.chapter or '',
                'topic': question.topic or '',
                'class_name': question.subject.class_name.class_name if question.subject and question.subject.class_name else 'Unknown',
                'answer': question.answer or '',
                'option1': question.option1 or '',
                'option2': question.option2 or '',
                'option3': question.option3 or '',
                'option4': question.option4 or '',
                'correct_answer': question.correct_options or '',
            })
        
        return JsonResponse({
            'success': True,
            'count': len(questions_data),
            'questions': questions_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'questions': []
        })





@csrf_exempt
def get_filtered_questions(request):
    """API endpoint to get filtered questions"""
    try:
        # Get filter parameters
        subject_id = request.GET.get('subject')
        question_type = request.GET.get('type')
        difficulty = request.GET.get('difficulty')
        marks = request.GET.get('marks')
        chapter_id = request.GET.get('chapter')
        class_id = request.GET.get('class')
        course_id = request.GET.get('course')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # Start with all questions
        questions = Question.objects.all()
        
        # Apply filters
        if subject_id:
            questions = questions.filter(subject_id=subject_id)
        if question_type:
            questions = questions.filter(question_type=question_type)
        if difficulty:
            questions = questions.filter(difficulty_level=difficulty)
        if marks:
            questions = questions.filter(marks=marks)
        if chapter_id:
            questions = questions.filter(chapter_id=chapter_id)
        if class_id:
            # Filter by class through subject
            questions = questions.filter(subject__class_name_id=class_id)
        if course_id:
            # Filter by course through class
            questions = questions.filter(subject__class_name__course_id=course_id)
        if search:
            questions = questions.filter(question_text__icontains=search)
        
        # Calculate pagination
        total_count = questions.count()
        total_pages = (total_count + page_size - 1) // page_size  # Ceiling division
        
        # Apply pagination
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_questions = questions[start_index:end_index]
        
        # Format response
        questions_data = []
        for question in paginated_questions:
            questions_data.append({
                'id': question.id,
                'subject_id': question.subject.id if question.subject else None,
                'subject_name': question.subject.name if question.subject else 'Unknown',
                'question': question.question_text,
                'type': question.question_type,
                'difficulty': question.difficulty_level,
                'marks': question.marks,
                'chapter': question.chapter.name if question.chapter else 'General',
                'topic': question.topic or 'General',
                'options': question.options.split('|') if question.options and '|' in question.options else None,
                'correct_answer': question.correct_answer,
                'class_name': question.subject.class_name.class_name if question.subject and question.subject.class_name else 'Unknown'
            })
        
        return JsonResponse({
            'success': True,
            'questions': questions_data,
            'total_pages': total_pages,
            'current_page': page,
            'total_count': total_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def get_chapters(request):
    """API endpoint to get chapters for a subject"""
    try:
        subject_id = request.GET.get('subject_id')
        
        if subject_id:
            chapters = Chapter.objects.filter(subject_id=subject_id)
        else:
            chapters = Chapter.objects.all()
        
        chapters_data = [{'id': ch.id, 'name': ch.name} for ch in chapters]
        
        return JsonResponse({
            'success': True,
            'chapters': chapters_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# @csrf_exempt
# def save_question_paper(request):
#     """API endpoint to save generated question paper"""
#     try:
#         if request.method == 'POST':
#             data = json.loads(request.body)
            
#             # Here you would save the question paper to your database
#             # For example, create a QuestionPaper model
            
#             return JsonResponse({
#                 'success': True,
#                 'message': 'Question paper saved successfully',
#                 'paper_id': 1  # Replace with actual ID
#             })
#         else:
#             return JsonResponse({
#                 'success': False,
#                 'error': 'Invalid request method'
#             })
            
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'error': str(e)
#         })

# You might also need these views
def get_questions(request):
    """Simple API to get all questions (for testing)"""
    questions = Question.objects.all()[:50]  # Limit for testing
    questions_data = []
    
    for question in questions:
        questions_data.append({
            'id': question.id,
            'subject_name': question.subject.name if question.subject else 'Unknown',
            'question': question.question_text[:100] + '...' if len(question.question_text) > 100 else question.question_text,
            'type': question.question_type,
            'difficulty': question.difficulty_level,
            'marks': question.marks,
            'chapter': question.chapter.name if question.chapter else 'General',
        })
    
    return JsonResponse({'questions': questions_data})



from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
import os

@csrf_exempt
def download_pdf(request):
    """Generate and download PDF of question paper"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            html_content = data.get('content', '')
            
            # Basic HTML template for PDF
            html_template = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: 'Times New Roman', serif; padding: 20px; }}
                    .header {{ text-align: center; margin-bottom: 30px; }}
                    .section {{ margin-bottom: 20px; }}
                    .question {{ margin-bottom: 15px; }}
                    .question-number {{ font-weight: bold; }}
                    .instructions {{ border: 1px solid #333; padding: 15px; margin-bottom: 20px; background: #f8f9fa; }}
                    .signature-section {{ margin-top: 50px; display: flex; justify-content: space-between; }}
                    .signature-box {{ width: 200px; text-align: center; }}
                    .signature-line {{ border-top: 1px solid #333; margin: 40px 0 5px; }}
                    @media print {{
                        .no-print {{ display: none; }}
                    }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Create PDF
            result = BytesIO()
            pdf = pisa.CreatePDF(BytesIO(html_template.encode('utf-8')), result)
            
            if not pdf.err:
                # Return PDF as response
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="question_paper.pdf"'
                return response
            else:
                return JsonResponse({'error': 'Error generating PDF'}, status=500)
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Alternative using ReportLab (simpler but less HTML support)
def generate_pdf_reportlab(request):
    """Generate PDF using ReportLab"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create buffer for PDF
            buffer = BytesIO()
            
            # Create PDF object
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Set starting position
            y = height - 50
            
            # Add content
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, y, data.get('school_name', 'School Name'))
            y -= 30
            
            p.setFont("Helvetica", 12)
            p.drawString(50, y, f"Exam: {data.get('title', 'Mid-Term Examination')}")
            y -= 20
            
            # Continue adding content...
            
            # Save PDF
            p.showPage()
            p.save()
            
            # Get PDF value from buffer
            pdf = buffer.getvalue()
            buffer.close()
            
            # Create HTTP response
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="question_paper.pdf"'
            
            return response
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



from django.core.files.base import ContentFile
import base64
from .models import TeacherPaperSettings
from django.core.files.storage import default_storage
import uuid

@csrf_exempt
@login_required
def save_teacher_paper_settings(request):
    """Save teacher's paper settings including logo"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get or create settings for this teacher
            settings, created = TeacherPaperSettings.objects.get_or_create(
                teacher=request.user
            )
            
            # Update school info
            settings.school_name = data.get('school_name', settings.school_name)
            settings.school_address = data.get('school_address', settings.school_address)
            settings.school_contact = data.get('school_contact', settings.school_contact)
            settings.affiliation_number = data.get('affiliation_number', settings.affiliation_number)
            
            # Update paper defaults
            settings.default_exam_name = data.get('exam_name', settings.default_exam_name)
            settings.default_total_marks = data.get('total_marks', settings.default_total_marks)
            settings.default_time_duration = data.get('time_duration', settings.default_time_duration)
            settings.default_instructions = data.get('instructions', settings.default_instructions)
            
            # Update logo position - ONLY CENTER OR NONE
            logo_position = data.get('logo_position', 'center')
            if logo_position not in ['center', 'none']:
                logo_position = 'center'  # Default to center
            settings.logo_position = logo_position
            
            # Handle logo image if provided
            logo_data = data.get('logo_data')
            if logo_data and 'data:image' in logo_data:
                try:
                    # Extract the base64 data
                    format, imgstr = logo_data.split(';base64,')
                    ext = format.split('/')[-1]
                    
                    # Generate unique filename
                    filename = f"teacher_logos/{request.user.id}/{uuid.uuid4()}.{ext}"
                    
                    # Decode and save the image
                    decoded_image = base64.b64decode(imgstr)
                    
                    # Delete old logo if exists
                    if settings.logo_image:
                        old_logo_path = settings.logo_image.path
                        if default_storage.exists(old_logo_path):
                            default_storage.delete(old_logo_path)
                    
                    # Save new logo
                    settings.logo_image.save(
                        filename,
                        ContentFile(decoded_image),
                        save=False
                    )
                except Exception as e:
                    print(f"Error saving logo: {e}")
                    # Continue without logo if there's an error
            
            settings.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Settings saved successfully!',
                'created': created,
                'has_logo': bool(settings.logo_image)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def get_teacher_paper_settings(request):
    """Get teacher's saved paper settings"""
    try:
        settings = TeacherPaperSettings.objects.get(teacher=request.user)
        
        # Get logo URL if exists
        logo_url = None
        if settings.logo_image and hasattr(settings.logo_image, 'url'):
            try:
                logo_url = request.build_absolute_uri(settings.logo_image.url)
            except:
                logo_url = None
        
        return JsonResponse({
            'success': True,
            'settings': {
                'school_name': settings.school_name,
                'school_address': settings.school_address,
                'school_contact': settings.school_contact,
                'affiliation_number': settings.affiliation_number,
                'logo_url': logo_url,
                'logo_position': settings.logo_position,
                'exam_name': settings.default_exam_name,
                'total_marks': settings.default_total_marks,
                'time_duration': settings.default_time_duration,
                'instructions': settings.default_instructions,
                'has_logo': bool(settings.logo_image)
            }
        })
        
    except TeacherPaperSettings.DoesNotExist:
        # Return default settings if not exists
        return JsonResponse({
            'success': True,
            'settings': {
                'school_name': 'Your School Name',
                'school_address': 'City, State, PIN Code',
                'school_contact': 'Phone: 1234567890 | Email: school@example.com',
                'affiliation_number': 'Affiliation No: 123456',
                'logo_url': None,
                'logo_position': 'center',  # Default to center
                'exam_name': 'Mid-Term Examination',
                'total_marks': 100,
                'time_duration': '3 hours',
                'instructions': '''All questions are compulsory.
Read each question carefully before answering.
Write answers in the space provided.
Use blue/black ballpoint pen only.
Calculators are not allowed unless specified.
Write your roll number on every page.''',
                'has_logo': False
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@login_required
def clear_teacher_logo(request):
    """Clear teacher's logo"""
    if request.method == 'POST':
        try:
            settings = TeacherPaperSettings.objects.get(teacher=request.user)
            
            # Delete the logo file
            if settings.logo_image:
                settings.logo_image.delete(save=False)
                settings.logo_image = None
                settings.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Logo cleared successfully!'
            })
            
        except TeacherPaperSettings.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Settings not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

from django.http import JsonResponse
from django.db.models import Q
from .models import Subject, Question

@login_required
def get_chapters_by_subject(request):
    """AJAX view to get chapters for a subject"""
    subject_id = request.GET.get('subject_id')
    
    if not subject_id:
        return JsonResponse({'chapters': []})
    
    try:
        subject = Subject.objects.get(id=subject_id)
        
        # Get unique chapters from Question model for this subject
        chapters = Question.objects.filter(
            subject=subject,
            chapter__isnull=False
        ).exclude(chapter='').values_list('chapter', flat=True).distinct().order_by('chapter')
        
        chapter_list = [{'id': ch, 'name': ch} for ch in chapters]
        
        return JsonResponse({'chapters': chapter_list})
    
    except Subject.DoesNotExist:
        return JsonResponse({'chapters': [], 'error': 'Subject not found'})
    except Exception as e:
        return JsonResponse({'chapters': [], 'error': str(e)})


@login_required
def get_questions_by_filters(request):
    """AJAX view to get questions based on subject and chapters"""
    subject_id = request.GET.get('subject_id')
    chapter_ids = request.GET.get('chapter_ids', '')
    
    if not subject_id or not chapter_ids:
        return JsonResponse({'questions': []})
    
    try:
        subject = Subject.objects.get(id=subject_id)
        chapter_list = chapter_ids.split(',')
        
        # Build query for chapters
        chapter_query = Q()
        for chapter in chapter_list:
            chapter_query |= Q(chapter=chapter)
        
        # Get questions
        questions = Question.objects.filter(
            subject=subject,
            
        ).values(
            'id', 'subject__name', 'chapter', 'topic', 
            'question_type', 'question', 'marks', 'difficulty',
            'option1', 'option2', 'option3', 'option4'
        )[:100]  # Limit to 100 questions
        
        questions_list = []
        for q in questions:
            questions_list.append({
                'id': q['id'],
                'subject': q['subject__name'],
                'chapter': q['chapter'],
                'topic': q['topic'],
                'question_type': q['question_type'],
                'question': q['question'][:100] + '...' if len(q['question']) > 100 else q['question'],
                'full_question': q['question'],
                'marks': float(q['marks']),
                'difficulty': q['difficulty'],
                'has_options': bool(q['option1'] or q['option2'] or q['option3'] or q['option4'])
            })
        
        return JsonResponse({'questions': questions_list})
    
    except Subject.DoesNotExist:
        return JsonResponse({'questions': [], 'error': 'Subject not found'})
    except Exception as e:
        return JsonResponse({'questions': [], 'error': str(e)})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chapter, Subject

@csrf_exempt
def get_chapters_by_subject(request):
    """API to get chapters for a specific subject"""
    try:
        subject_id = request.GET.get('subject_id')
        
        if not subject_id:
            return JsonResponse({
                'success': False,
                'error': 'Subject ID is required'
            }, status=400)
        
        # Get chapters for this subject
        chapters = Chapter.objects.filter(subject_id=subject_id).order_by('name')
        
        chapters_data = [
            {
                'id': chapter.id,
                'name': chapter.name,
                'subject_id': chapter.subject.id,
                'subject_name': chapter.subject.name
            }
            for chapter in chapters
        ]
        
        return JsonResponse({
            'success': True,
            'chapters': chapters_data,
            'count': len(chapters_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_subjects(request):
    """API to get all subjects"""
    subjects = Subject.objects.all()
    subjects_data = []
    
    for subject in subjects:
        subjects_data.append({
            'id': subject.id,
            'name': subject.name,
            'class_name': subject.class_name.class_name if subject.class_name else 'Unknown'
        })
    
    return JsonResponse({'subjects': subjects_data})


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_question_api(request, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
        question.delete()

        return JsonResponse({
            "success": True,
            "message": "Question deleted successfully"
        }, status=200)

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


@login_required
def edit_question_view(request, question_id):
    """View to edit a question"""
    question = get_object_or_404(Question, id=question_id)
    subjects = Subject.objects.all()
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update common fields
                question.chapter = request.POST.get("chapter", "").strip()
                question.topic = request.POST.get("topic", "").strip()
                question.question = request.POST.get("question", "").strip()
                question.question_type = request.POST.get("question_type", "").strip()
                question.marks = int(request.POST.get("marks", "1"))
                question.difficulty = request.POST.get("difficulty", "medium")
                
                # Handle different question types
                if question.question_type == "objective":
                    correct_options = request.POST.getlist("correct_options[]")
                    question.answer = ",".join(correct_options) if correct_options else ""
                    
                    question.option1 = request.POST.get("option1", "").strip()
                    question.option2 = request.POST.get("option2", "").strip()
                    question.option3 = request.POST.get("option3", "").strip()
                    question.option4 = request.POST.get("option4", "").strip()
                    question.correct_options = question.answer
                    
                elif question.question_type == "match_following":
                    question.match_items = request.POST.get("match_items", "").strip()
                    question.match_answers = request.POST.get("match_answers", "").strip()
                    question.match_count = int(request.POST.get("match_count", "4"))
                    question.answer = question.match_answers
                    
                elif question.question_type == "fill_in_the_blanks":
                    question.blank_answers = request.POST.get("blank_answers", "").strip()
                    question.blank_positions = request.POST.get("blank_positions", "").strip()
                    question.blank_count = int(request.POST.get("blank_count", "1"))
                    question.answer = question.blank_answers
                    
                elif question.question_type == "numerical":
                    question.numerical_solution = request.POST.get("numerical_solution", "").strip()
                    question.final_answer = request.POST.get("final_answer", "").strip()
                    question.answer = question.final_answer or question.numerical_solution
                    
                elif question.question_type in ["descriptive", "short_answer", "long_answer", "true_false"]:
                    question.answer = request.POST.get("answer", "").strip()
                
                question.save()
                
                messages.success(request, "Question updated successfully!")
                return redirect('viewing_all_questions')
                
        except Exception as e:
            messages.error(request, f"Error updating question: {str(e)}")
    
    context = {
        'question': question,
        'subjects': subjects,
    }
    return render(request, "admin/edit_question.html", context)

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    
    if request.method == "POST":
        # Delete the associated user first if needed
        user = staff.user
        staff.delete()
        user.delete()
        
        messages.success(request, "Staff member deleted successfully!")
        return redirect('admin_staff_list')
    
    # If not POST, redirect to staff list
    return redirect('staff_list')

# Student----------------------------------------------------------------------
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()

def add_student(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        guardian_name = request.POST.get('guardian_name')
        guardian_number = request.POST.get('guardian_number')
        package_selected = request.POST.get('package_selected', 'Basic Package')

        # Admin entered username & password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Prevent duplicate user
        if User.objects.filter(email=email).exists():
            messages.error(request, "Student with this email already exists.")
            return redirect('add_student')

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists.")
            return redirect('add_student')

        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=name.split()[0] if name else '',
                    password=password
                )

                # Create student profile with created_type = 'admin'
                Student.objects.create(
                    user=user,
                    name=name,
                    email=email,
                    address=address,
                    phone_number=phone_number,
                    guardian_name=guardian_name,
                    guardian_number=guardian_number,
                    package_selected=package_selected,
                    created_type="admin added"  # ⭐ ADMIN ADDED
                )

                # EMAIL TEMPLATE
                subject = "Your Student Account Login Details"
                message = f"""
Hello {name},

Your student account has been created successfully.

Login Details:
Username: {username}
Password: {password}

You can now login to the student portal.

Regards,
Admin Team
"""

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                

                messages.success(request, "Student added successfully & login details sent to email!")
                return redirect('student_list')

        except Exception as e:
            messages.error(request, f"Error adding student: {str(e)}")
            return redirect('student_list')

    return render(request, 'Admin/Student/add_student.html')




@login_required
def student_list(request):
    query = request.GET.get('q', '')

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(package_selected__icontains=query) |
            Q(guardian_name__icontains=query)
        )

    context = {
        'students': students,
        'search_query': query
    }

    return render(request, 'Admin/Student/student_list.html', context)


@login_required
def view_student(request, student_type, student_id):
    if student_type == 'admin':
        student = get_object_or_404(Student, id=student_id)
        # template = 'Admin/Student/viewstudent.html'
    else:
        student = get_object_or_404(StudentProfile, id=student_id)
        # template = 'Admin/Student/viewstudent.html'

    return render(request, 'Admin/Student/viewstudent.html', {'student': student})

def delete_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f"Student {student.first_name} {student.last_name} deleted successfully.")
        return redirect('student_list')
    return redirect('student_list')




# Exam Creation--------------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from .models import ExamSchedule

def exam_schedule_view(request):
    # Get all exams ordered by date and time
    exams = ExamSchedule.objects.all().order_by('exam_date', 'exam_time')
    
    # Get current date for comparison
    current_date = timezone.now().date()
    
    # Format dates and times for better display
    for exam in exams:
        exam.formatted_date = exam.exam_date.strftime('%b %d, %Y')  # Format: Jan 01, 2023
        exam.formatted_time = exam.exam_time.strftime('%I:%M %p')   # Format: 02:30 PM
    
    context = {
        'exams': exams,
        'current_date': current_date,
        'current_date_formatted': current_date.strftime('%B %d, %Y')  # Format: January 01, 2023
    }

    return render(request, 'Admin/Examschedule.html', context)

@require_POST
def delete_exam(request, exam_id):
    exam = get_object_or_404(ExamSchedule, id=exam_id)
    exam.delete()
    return redirect('exam_schedule')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import ExamPlan
from .models import (
    Package,
    PackagePurchase,
    QuestionPaper,
    GeneratedQuestionPaper,
    ExamResult,
    StudentNotification,
    StudentExamSubmission
)


def plan_list(request):
    plans = ExamPlan.objects.filter(is_active=True)
    neet_plans = plans.filter(plan_type='neet')
    jee_plans = plans.filter(plan_type='jee')
    combined_plans = plans.filter(plan_type='combined')
    
    context = {
        'neet_plans': neet_plans,
        'jee_plans': jee_plans,
        'combined_plans': combined_plans,
    }
    return render(request, 'Admin/Plans/Plan_list.html', context)

def create_plan(request):
    if request.method == 'POST':
        plan = ExamPlan()
        plan.name = request.POST.get('name')
        plan.plan_type = request.POST.get('plan_type')
        plan.price = request.POST.get('price')
        plan.duration = request.POST.get('duration')
        plan.users = request.POST.get('users', 1)
        plan.practice_tests = request.POST.get('practice_tests', 0)
        plan.full_length_mocks = request.POST.get('full_length_mocks', 0)
        plan.doubt_sessions = request.POST.get('doubt_sessions', 0)
        plan.study_materials = 'study_materials' in request.POST
        plan.video_lectures = 'video_lectures' in request.POST
        plan.performance_analytics = 'performance_analytics' in request.POST
        plan.storage = request.POST.get('storage', '1024 MB')
        plan.save()

        messages.success(request, 'Plan created successfully!')
        return redirect('plan_list')

    return render(request, 'Admin/Plans/create_plan.html')

def edit_plan(request, plan_id):
    plan = get_object_or_404(ExamPlan, id=plan_id)
    
    if request.method == 'POST':
        plan.name = request.POST.get('name')
        plan.plan_type = request.POST.get('plan_type')
        plan.price = request.POST.get('price')
        plan.duration = request.POST.get('duration')
        plan.users = request.POST.get('users', 1)
        plan.practice_tests = request.POST.get('practice_tests', 0)
        plan.full_length_mocks = request.POST.get('full_length_mocks', 0)
        plan.doubt_sessions = request.POST.get('doubt_sessions', 0)
        plan.study_materials = 'study_materials' in request.POST
        plan.video_lectures = 'video_lectures' in request.POST
        plan.performance_analytics = 'performance_analytics' in request.POST
        plan.storage = request.POST.get('storage', '1024 MB')
        plan.save()
        
        messages.success(request, 'Plan updated successfully!')
        return redirect('plan_list')
    
    return render(request, 'Admin/Plans/edit_plan.html', {'plan': plan})

def delete_plan(request, plan_id):
    plan = get_object_or_404(ExamPlan, id=plan_id)
    
    if request.method == 'POST':
        # Soft delete by setting is_active to False
        plan.is_active = False
        plan.save()
        messages.success(request, 'Plan deleted successfully!')
        return redirect('plan_list')
    
    # For GET requests, show confirmation page
    return render(request, 'Admin/Plans/delete_plan.html', {'plan': plan})



def student_profile(request):
    if request.method == "POST":
        try:
            # Get form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            date_of_birth = request.POST.get('date_of_birth')
            mobile_number = request.POST.get('mobile_number')
            email = request.POST.get('email')
            guardian_name = request.POST.get('guardian_name')
            guardian_number = request.POST.get('guardian_number')
            address = request.POST.get('address')
            pin_code = request.POST.get('pin_code')
            gender = request.POST.get('gender')
            course_applied_for = request.POST.get('course_applied_for')
            
            # Academic details
            classX_board = request.POST.get('classX_board', '')
            classX_percentage = request.POST.get('classX_percentage', None)
            classX_year = request.POST.get('classX_year', None)
            
            classXII_board = request.POST.get('classXII_board', '')
            classXII_percentage = request.POST.get('classXII_percentage', None)
            classXII_year = request.POST.get('classXII_year', None)
            
            # Create or get user
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            
            if not created:
                messages.error(request, 'A student with this email already exists!')
                return redirect('add_student')
            
            # Create student profile
            StudentProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                mobile_number=mobile_number,
                email=email,
                guardian_name=guardian_name,
                guardian_number=guardian_number,
                address=address,
                pin_code=pin_code,
                gender=gender,
                course_applied_for=course_applied_for,
                classX_board=classX_board,
                classX_percentage=classX_percentage,
                classX_year=classX_year,
                classXII_board=classXII_board,
                classXII_percentage=classXII_percentage,
                classXII_year=classXII_year
            )
            
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
            
        except Exception as e:
            messages.error(request, f'Error adding student: {str(e)}')
    
    student_list = StudentProfile.objects.all().order_by('-created_at')
    return render(request, "Admin/add_student.html", {"student_list": student_list})


# Online_App/views.py

@login_required
def Student1(request):
    """Student dashboard with packages and notifications"""

    # ===== STUDENT PROFILE =====
    student_profile = None
    if hasattr(request.user, 'student'):
        student_profile = request.user.student
    elif hasattr(request.user, 'studentprofile'):
        student_profile = request.user.studentprofile

    # ===== GET ACTIVE PACKAGES =====
    packages = Package.objects.filter(
        is_active=True
    ).order_by('display_order')

    # ===== GET PURCHASED PACKAGES =====
    purchased_packages = PackagePurchase.objects.filter(
        student=request.user,
        is_active=True,
        expiry_date__gte=timezone.now()  # avoid expired packages
    )

    purchased_package_ids = [
        purchase.package.id for purchase in purchased_packages
    ]

    # ===== GET NOTIFICATIONS =====
    recent_notifications = StudentNotification.objects.filter(
        student=request.user
    ).order_by('-created_at')[:10]

    unread_notifications_count = StudentNotification.objects.filter(
        student=request.user,
        is_read=False
    ).count()

    # ===== GET TODAY EXAMS =====
    today = timezone.now().date()

    published_papers = GeneratedQuestionPaper.objects.filter(
        is_published=True,
        status='published',
        created_at__date=today
    )

    completed_exam_ids_today = ExamResult.objects.filter(
        student=request.user,
        submitted_at__date=today,
        paper__isnull=False
    ).values_list('paper_id', flat=True)

    available_papers = published_papers.exclude(
        id__in=completed_exam_ids_today
    )

    # ===== PROCESS PAPERS =====
    valid_papers = []

    for paper in available_papers:

        if paper.question_data and isinstance(paper.question_data, list):
            total_questions = len(paper.question_data)

        elif paper.question_data and isinstance(paper.question_data, dict):
            questions = paper.question_data.get('selected_questions', [])
            total_questions = len(questions)

        else:
            total_questions = 0

        if total_questions > 0:
            valid_papers.append({
                'paper': paper,
                'total_questions': total_questions,
                'total_marks': paper.total_marks or 100,
                'exam_time': paper.exam_time or 180,
            })

    # ===== GET EVALUATED SUBMISSIONS =====
    evaluated_submissions = StudentExamSubmission.objects.filter(
        student=request.user,
        status='evaluated'
    ).select_related(
        'evaluated_by'
    ).order_by('-evaluated_at')[:5]

    # ===== DEBUG (OPTIONAL) =====
    print("===== STUDENT DASHBOARD DEBUG =====")
    print("Packages:", packages.count())
    print("Purchased IDs:", purchased_package_ids)
    print("Notifications:", recent_notifications.count())
    print("Available Exams:", len(valid_papers))
    print("===================================")

    # ===== CONTEXT =====
    context = {
        'data': {
            'username': request.user.username,
            'student_profile': student_profile,
        },

        'packages': packages,
        'purchased_package_ids': purchased_package_ids,

        'question_paper': QuestionPaper.objects.last()
        if QuestionPaper.objects.exists() else None,

        'recent_notifications': recent_notifications,
        'unread_notifications_count': unread_notifications_count,

        'exams_data': valid_papers,
        'today': today,

        'total_today': published_papers.count(),
        'completed_today': len(completed_exam_ids_today),
        'remaining_today': available_papers.count(),

        'evaluated_submissions': evaluated_submissions,
    }

    return render(request, 'student.html', context)

# Online_App/views.py
@login_required
@user_passes_test(lambda u: u.user_type == 4)  # Only students
def student_view_evaluated_exam(request, submission_id):
    """Student view of a specific evaluated exam"""
    # Get the submission
    submission = get_object_or_404(
        StudentExamSubmission,
        id=submission_id,
        student=request.user,
        status='evaluated'  # Only show evaluated submissions
    )
    
    # Mark the notification as read
    try:
        from .models import StudentNotification
        StudentNotification.objects.filter(
            student=request.user,
            submission=submission,
            is_read=False
        ).update(is_read=True)
    except:
        pass
    
    # Get the paper
    paper = submission.paper
    
    # Parse marking data if exists
    marking_data = submission.marking_data or {}
    question_marks = submission.question_marks or {}
    
    # Calculate statistics
    total_questions = len(question_marks) if isinstance(question_marks, dict) else 0
    
    context = {
        'submission': submission,
        'paper': paper,
        'teacher': submission.evaluated_by,
        'marking_data': marking_data,
        'question_marks': question_marks,
        'total_questions': total_questions,
        'title': f'Evaluation - {submission.exam_title}'
    }
    
    return render(request, 'student_view_evaluation.html', context)

from django.utils import timezone
from datetime import datetime

@login_required
def student_available_exams(request):
    """Show only TODAY'S exams that student hasn't taken yet"""
    
    # Get today's date (only date part, not time)
    today = timezone.now().date()
    
    print(f"DEBUG: Today's date is: {today}")
    print(f"DEBUG: Student: {request.user.username}")
    
    # Get ONLY published papers created TODAY
    published_papers = GeneratedQuestionPaper.objects.filter(
        is_published=True,
        status='published',
        created_at__date=today
    )
    
    print(f"DEBUG: Found {published_papers.count()} exams created today ({today})")
    for paper in published_papers:
        print(f"  - Paper ID: {paper.id}, Name: {paper.exam_name}")
    
    # Get exams this student has already taken TODAY only
    # Use 'paper' field (not 'question_paper') since it's the GeneratedQuestionPaper
    completed_exam_ids_today = ExamResult.objects.filter(
        student=request.user,
        submitted_at__date=today,
        paper__isnull=False  # Only include exams with a paper (GeneratedQuestionPaper)
    ).values_list('paper_id', flat=True)  # CHANGED: Use 'paper_id' not 'question_paper_id'
    
    print(f"DEBUG: Student has completed {len(completed_exam_ids_today)} exams TODAY")
    print(f"DEBUG: Completed paper IDs: {list(completed_exam_ids_today)}")
    
    # Filter out only TODAY'S completed exams
    available_papers = published_papers.exclude(id__in=completed_exam_ids_today)
    
    print(f"DEBUG: {available_papers.count()} exams available today for this student")
    for paper in available_papers:
        print(f"  - Available Paper ID: {paper.id}, Name: {paper.exam_name}")
    
    # Process papers to check if they have questions
    valid_papers = []
    for paper in available_papers:
        # Check if paper has question_data
        if paper.question_data and isinstance(paper.question_data, list):
            total_questions = len(paper.question_data)
        elif paper.question_data and isinstance(paper.question_data, dict):
            questions = paper.question_data.get('selected_questions', [])
            total_questions = len(questions) if isinstance(questions, list) else 0
        else:
            total_questions = 0
        
        if total_questions > 0:
            valid_papers.append({
                'paper': paper,
                'total_questions': total_questions,
                'total_marks': paper.total_marks or 100,
                'exam_time': paper.exam_time or 180,
                # Add subject flags for template
                'has_math': any(q.get('subject') == 'Math' for q in (paper.question_data if isinstance(paper.question_data, list) else paper.question_data.get('selected_questions', []))),
                'has_physics': any(q.get('subject') == 'Physics' for q in (paper.question_data if isinstance(paper.question_data, list) else paper.question_data.get('selected_questions', []))),
                'has_chemistry': any(q.get('subject') == 'Chemistry' for q in (paper.question_data if isinstance(paper.question_data, list) else paper.question_data.get('selected_questions', []))),
                'has_biology': any(q.get('subject') == 'Biology' for q in (paper.question_data if isinstance(paper.question_data, list) else paper.question_data.get('selected_questions', []))),
            })
            print(f"✓ Available today: Paper ID {paper.id}: {paper.exam_name}")
    
    print(f"DEBUG: Total valid papers for today: {len(valid_papers)}")
    
    # Calculate progress stats
    total_today = published_papers.count()
    completed_today = len(completed_exam_ids_today)
    remaining_today = available_papers.count()
    
    print(f"DEBUG: Progress - Total: {total_today}, Completed: {completed_today}, Remaining: {remaining_today}")
    
    context = {
        'exams_data': valid_papers,
        'username': request.user.username,
        'today': today,
        'total_today': total_today,
        'completed_today': completed_today,
        'remaining_today': remaining_today,
    }
    return render(request, 'available_exams.html', context)

# @login_required
def student_start_exam(request, paper_id):
    """Student starts an exam"""
    paper = get_object_or_404(QuestionPaper, id=paper_id)
    
    # Check if student has already taken this exam
    if ExamResult.objects.filter(student=request.user, question_paper=paper).exists():
        messages.error(request, "You have already taken this exam.")
        return redirect('student_available_exams')
    
    # Check if paper has questions
    total_questions = (
        paper.mathematics_questions.count() +
        paper.physics_questions.count() +
        paper.chemistry_questions.count() +
        paper.biology_questions.count()
    )
    
    if total_questions == 0:
        messages.error(request, "This exam paper has no questions.")
        return redirect('student_available_exams')
    
    # Store exam info in session
    request.session['current_exam_id'] = paper_id
    request.session['exam_start_time'] = str(timezone.now())
    request.session['exam_answers'] = {}
    
    # Get exam duration from paper or use default
    exam_duration = 180  # Default 3 hours in minutes
    if hasattr(paper, 'exam_time') and paper.exam_time:
        exam_duration = paper.exam_time
    request.session['exam_duration'] = exam_duration
    
    # Store paper title
    paper_title = f"Question Paper {paper.id}"
    if hasattr(paper, 'exam_name') and paper.exam_name:
        paper_title = paper.exam_name
    request.session['paper_title'] = paper_title
    
    context = {
        'paper': paper,
        'total_questions': total_questions,
        'exam_time': exam_duration,
        'username': request.user.username,
        'paper_title': paper_title
    }
    
    return render(request, 'student/start_exam.html', context)

def get_options_dict(question):
    """Extract options from question object"""
    options = {}
    if question.option1:
        options['A'] = question.option1
    if question.option2:
        options['B'] = question.option2
    if question.option3:
        options['C'] = question.option3
    if question.option4:
        options['D'] = question.option4
    if hasattr(question, 'option5') and question.option5:
        options['E'] = question.option5
    return options

def get_correct_answer(question):
    """Extract correct answer from question object"""
    if question.question_type == 'objective':
        if hasattr(question, 'correct_option') and question.correct_option:
            return question.correct_option
        elif hasattr(question, 'correct_options') and question.correct_options:
            return question.correct_options
    else:
        return question.answer if hasattr(question, 'answer') else ''

@login_required
def student_take_exam(request, question_index):
    """Display individual exam question"""
    if 'current_exam_id' not in request.session:
        return redirect('student_available_exams')
    
    paper_id = request.session['current_exam_id']
    paper = get_object_or_404(QuestionPaper, id=paper_id)
    
    # Get questions from session
    all_questions = request.session.get('exam_questions', [])
    
    if question_index >= len(all_questions):
        # All questions answered, redirect to submit
        return redirect('student_submit_exam')
    
    current_question = all_questions[question_index]
    
    # Check if already answered
    exam_answers = request.session.get('exam_answers', {})
    previous_answer = exam_answers.get(current_question['id'], '')
    
    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip()
        
        # Save answer in session
        exam_answers = request.session.get('exam_answers', {})
        exam_answers[current_question['id']] = answer
        request.session['exam_answers'] = exam_answers
        
        # Update answered count
        answered_count = len(exam_answers)
        request.session['answered_questions'] = answered_count
        
        # Move to next question or submit
        if question_index + 1 < len(all_questions):
            request.session['current_question_index'] = question_index + 1
            return redirect('student_take_exam', question_index=question_index + 1)
        else:
            return redirect('student_submit_exam')
    
    # Calculate remaining time
    start_time_str = request.session.get('exam_start_time')
    remaining_minutes = paper.exam_time if paper.exam_time else 180
    
    if start_time_str:
        try:
            start_time = timezone.datetime.fromisoformat(start_time_str)
            elapsed = timezone.now() - start_time
            elapsed_minutes = elapsed.total_seconds() / 60
            remaining_minutes = max(0, (paper.exam_time if paper.exam_time else 180) - elapsed_minutes)
        except:
            pass
    
    context = {
        'paper': paper,
        'question': current_question,
        'current_index': question_index + 1,
        'total_questions': len(all_questions),
        'previous_answer': previous_answer,
        'remaining_minutes': int(remaining_minutes),
        'answered_questions': request.session.get('answered_questions', 0),
        'question_number': question_index + 1,
        'username': request.user.username
    }
    
    return render(request, 'student/take_exam.html', context)

@login_required
def student_submit_exam(request):
    """Submit the completed exam"""
    if 'current_exam_id' not in request.session:
        return redirect('student_available_exams')
    
    paper_id = request.session['current_exam_id']
    paper = get_object_or_404(QuestionPaper, id=paper_id)
    
    # Calculate score
    all_questions = request.session.get('exam_questions', [])
    exam_answers = request.session.get('exam_answers', {})
    
    total_marks = 0
    obtained_marks = 0
    correct_answers = 0
    incorrect_answers = 0
    
    for question in all_questions:
        total_marks += question.get('marks', 4)
        user_answer = exam_answers.get(question['id'], '').strip()
        correct_answer = question.get('correct_answer', '')
        
        if question['type'] == 'objective':
            # For MCQ questions
            if user_answer and user_answer == str(correct_answer):
                obtained_marks += question.get('marks', 4)
                correct_answers += 1
            elif user_answer:  # Answered but wrong
                incorrect_answers += 1
        else:
            # For descriptive/numerical questions
            if user_answer:  # For now, give marks if answered (can implement more complex checking)
                obtained_marks += question.get('marks', 4) // 2  # Half marks for attempting
    
    # Calculate time taken
    start_time_str = request.session.get('exam_start_time')
    time_taken = 0
    if start_time_str:
        try:
            start_time = timezone.datetime.fromisoformat(start_time_str)
            time_taken = (timezone.now() - start_time).total_seconds() / 60  # in minutes
        except:
            pass
    
    # Save exam result
    exam_result = ExamResult.objects.create(
        student=request.user,
        question_paper=paper,
        total_marks=total_marks,
        obtained_marks=obtained_marks,
        exam_time=int(time_taken),
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
        answers=json.dumps(exam_answers)
    )
    
    # Clear session data
    session_keys = ['current_exam_id', 'exam_start_time', 'exam_questions', 
                    'exam_answers', 'current_question_index', 'answered_questions']
    for key in session_keys:
        if key in request.session:
            del request.session[key]
    
    context = {
        'result': exam_result,
        'paper': paper,
        'total_questions': len(all_questions),
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'percentage': (obtained_marks / total_marks * 100) if total_marks > 0 else 0,
        'time_taken': f"{int(time_taken)} minutes",
        'username': request.user.username
    }
    
    return render(request, 'student/exam_result.html', context)

# @login_required
# def student_exam_results(request):
#     """View all exam results for the student"""
#     results = ExamResult.objects.filter(student=request.user).order_by('-submitted_at')
    
#     context = {
#         'results': results,
#         'username': request.user.username
#     }
    
#     return render(request, 'student/exam_results.html', context)

@login_required
def student_view_result_detail(request, result_id):
    """View detailed result of a specific exam"""
    result = get_object_or_404(ExamResult, id=result_id, student=request.user)
    
    # Parse answers if they exist
    answers = {}
    if result.answers:
        try:
            answers = json.loads(result.answers)
        except:
            pass
    
    context = {
        'result': result,
        'answers': answers,
        'percentage': (result.obtained_marks / result.total_marks * 100) if result.total_marks > 0 else 0,
        'username': request.user.username
    }
    
    return render(request, 'student/view_result_detail.html', context)


@login_required
def Profile(request):
    return render(request, 'Profile.html')

@login_required
def Parent(request):
    exams = ExamSchedule.objects.all()  # Fetch all exams
    context = {
        'data': {'username': request.user.username},
        'exams': exams  # Pass exams to parent.html
    }
    return render(request, 'parent.html', context)

def Data(request):
    return render(request, 'Data-entry.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date, timedelta
from .models import (
    Staff, Student, ExamSchedule, StudentExamSubmission, 
    TeacherNotification, GeneratedQuestionPaper, QuestionPaper,
    ExamResult
)

@login_required
def Teacher(request):
    print("DEBUG: Teacher view called - UPDATED VERSION")
    print(f"DEBUG: User: {request.user.username}")
    
    # Get the staff object for the logged-in teacher
    try:
        staff = Staff.objects.get(user=request.user)
        print(f"DEBUG: Staff found: {staff}")
    except Staff.DoesNotExist:
        staff = None
        print("DEBUG: No staff object found, creating one...")
        # Create staff profile if doesn't exist
        staff = Staff.objects.create(
            user=request.user,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email,
            created_type='self'
        )
    
    # Get exam schedules
    exams = ExamSchedule.objects.all()
    print(f"DEBUG: Exams count: {exams.count()}")
    
    # ==================== DYNAMIC STATISTICS ====================
    today = date.today()
    
    # 1. Total Students (count all students) - FIXED
    try:
        total_students = Student.objects.count()
        print(f"DEBUG: Total students: {total_students}")
        
        # Check if there are any students
        if total_students == 0:
            print("DEBUG: No students found in database")
            all_students = Student.objects.all()
            for student in all_students[:5]:
                print(f"DEBUG: Student: {student.name} ({student.email})")
    except Exception as e:
        print(f"DEBUG: Error counting students: {e}")
        import traceback
        traceback.print_exc()
        total_students = 0
    
    # Calculate growth percentage
    try:
        growth_percentage = calculate_student_growth()
    except Exception as e:
        print(f"DEBUG: Error calculating growth: {e}")
        import traceback
        traceback.print_exc()
        growth_percentage = 0
    print(f"DEBUG: Growth percentage: {growth_percentage}")
    
    # 2. Upcoming Exams (exams scheduled for today or future)
    upcoming_exams = ExamSchedule.objects.filter(exam_date__gte=today).count()
    print(f"DEBUG: Upcoming exams: {upcoming_exams}")
    
    # Get next exam date
    next_exam = ExamSchedule.objects.filter(exam_date__gte=today).order_by('exam_date', 'exam_time').first()
    if next_exam:
        if next_exam.exam_date == today:
            next_exam_text = "Today"
        elif (next_exam.exam_date - today).days == 1:
            next_exam_text = "Tomorrow"
        else:
            next_exam_text = f"In {(next_exam.exam_date - today).days} days"
    else:
        next_exam_text = "No upcoming exams"
    print(f"DEBUG: Next exam text: {next_exam_text}")
    
    # 3. Pending Submissions (submissions waiting for teacher evaluation)
    pending_submissions_count = StudentExamSubmission.objects.filter(
        status='submitted'
    ).count()
    print(f"DEBUG: Pending submissions: {pending_submissions_count}")
    
    # 4. Unread Messages/Notifications for teacher
    unread_messages_count = TeacherNotification.objects.filter(
        teacher=request.user,
        is_read=False
    ).count()
    print(f"DEBUG: Unread messages: {unread_messages_count}")
    
    # Count urgent notifications (last 24 hours)
    yesterday = timezone.now() - timedelta(days=1)
    urgent_notifications = TeacherNotification.objects.filter(
        teacher=request.user,
        created_at__gte=yesterday,
        is_read=False
    ).count()
    print(f"DEBUG: Urgent notifications: {urgent_notifications}")
    
    # Get recent activity - FIXED
    try:
        recent_activities = get_recent_activities(request.user)
    except Exception as e:
        print(f"DEBUG: Error getting recent activities: {e}")
        recent_activities = []
    print(f"DEBUG: Recent activities count: {len(recent_activities)}")
    
    # Count generated papers by this teacher
    generated_papers_count = GeneratedQuestionPaper.objects.filter(
        created_by=request.user
    ).count()
    print(f"DEBUG: Generated papers count: {generated_papers_count}")
    
    # DEBUG: Print all context values
    print("=" * 50)
    print("DEBUG CONTEXT VALUES:")
    print(f"total_students: {total_students}")
    print(f"growth_percentage: {growth_percentage}")
    print(f"upcoming_exams: {upcoming_exams}")
    print(f"pending_submissions_count: {pending_submissions_count}")
    print(f"unread_messages_count: {unread_messages_count}")
    print(f"urgent_notifications: {urgent_notifications}")
    print(f"generated_papers_count: {generated_papers_count}")
    print(f"recent_activities: {recent_activities}")
    print("=" * 50)
    
    context = {
        'data': {'username': request.user.username},
        'staff': staff,
        'exams': exams,
        'today': today,
        
        # Statistics for dashboard
        'total_students': total_students,
        'growth_percentage': growth_percentage,
        'upcoming_exams': upcoming_exams,
        'next_exam_text': next_exam_text,
        'pending_submissions_count': pending_submissions_count,
        'unread_messages_count': unread_messages_count,
        'urgent_notifications': urgent_notifications,
        'recent_activities': recent_activities,
        'generated_papers_count': generated_papers_count,
    }
    
    print(f"DEBUG: Context keys being sent: {list(context.keys())}")
    return render(request, 'Teacher.html', context)



def calculate_student_growth():
    """Calculate student growth percentage from last month"""
    from django.utils import timezone
    from datetime import datetime, timedelta
    
    today = timezone.now().date()
    
    # Get current month start
    current_month_start = today.replace(day=1)
    
    # Students created this month
    try:
        current_month_students = Student.objects.filter(
            created_at__gte=current_month_start
        ).count()
        print(f"DEBUG: Current month students: {current_month_students}")
    except Exception as e:
        print(f"DEBUG: Error filtering current month students: {e}")
        current_month_students = Student.objects.count()  # Fallback to total count
    
    # Calculate last month start
    if current_month_start.month == 1:
        last_month_start = current_month_start.replace(
            year=current_month_start.year - 1, 
            month=12
        )
    else:
        last_month_start = current_month_start.replace(
            month=current_month_start.month - 1
        )
    
    # Students created last month
    try:
        last_month_students = Student.objects.filter(
            created_at__gte=last_month_start,
            created_at__lt=current_month_start
        ).count()
        print(f"DEBUG: Last month students: {last_month_students}")
    except Exception as e:
        print(f"DEBUG: Error filtering last month students: {e}")
        last_month_students = 0
    
    # Calculate percentage growth
    if last_month_students > 0:
        growth_percentage = ((current_month_students - last_month_students) / last_month_students) * 100
    else:
        # If no students last month, but we have students this month
        if current_month_students > 0:
            growth_percentage = 100.0  # 100% growth from 0
        else:
            growth_percentage = 0.0
    
    print(f"DEBUG: Calculated growth: {growth_percentage}%")
    return round(growth_percentage, 1)

def get_recent_activities(user):
    """Get recent activities for teacher dashboard"""
    from django.utils import timezone
    
    recent_activities = []
    
    # Recent submissions (last 5)
    recent_submissions = StudentExamSubmission.objects.filter(
        status='submitted'
    ).select_related('student').order_by('-submitted_at')[:5]
    
    for submission in recent_submissions:
        time_ago = timezone.now() - submission.submitted_at
        if time_ago.days > 0:
            time_text = f"{time_ago.days} days ago"
        elif time_ago.seconds // 3600 > 0:
            time_text = f"{time_ago.seconds // 3600} hours ago"
        else:
            time_text = f"{time_ago.seconds // 60} minutes ago"
        
        recent_activities.append({
            'type': 'submission',
            'title': f'New exam submission from {submission.student_name}',
            'description': f'{submission.exam_title} submitted for evaluation',
            'time': time_text,
            'icon': 'fa-file-upload',
            'color': 'blue'
        })
    
    # Recent notifications
    recent_notifications = TeacherNotification.objects.filter(
        teacher=user
    ).order_by('-created_at')[:3]
    
    for notification in recent_notifications:
        time_ago = timezone.now() - notification.created_at
        if time_ago.days > 0:
            time_text = f"{time_ago.days} days ago"
        elif time_ago.seconds // 3600 > 0:
            time_text = f"{time_ago.seconds // 3600} hours ago"
        else:
            time_text = f"{time_ago.seconds // 60} minutes ago"
        
        recent_activities.append({
            'type': 'notification',
            'title': 'Notification',
            'description': notification.message[:50] + '...' if len(notification.message) > 50 else notification.message,
            'time': time_text,
            'icon': 'fa-comment-alt',
            'color': 'green'
        })
    
    # If no activities, add a default one
    if not recent_activities:
        recent_activities.append({
            'type': 'info',
            'title': 'No recent activity',
            'description': 'Check back later for updates',
            'time': '',
            'icon': 'fa-inbox',
            'color': 'gray'
        })
    
    return recent_activities



from datetime import datetime
from .models import StaffProfile

@login_required
def teacher_profile(request):
    staff = StaffProfile.objects.filter(user=request.user).last()

    if request.method == 'POST':

        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        dob_str = request.POST.get('dob', '')  
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        subject = request.POST.get('subject')
        address = request.POST.get('address')

        # Parse DOB
        parsed_dob = None
        if dob_str:
            try:
                parsed_dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return redirect('teacher_profile')

        try:
            # If profile exists → update it
            if staff:
                staff.first_name = first_name
                staff.last_name = last_name
                staff.dob = parsed_dob
                staff.email = email
                staff.contact = contact
                staff.subject = subject
                staff.address = address
                staff.save()

            else:
                # Create new profile
                staff = StaffProfile.objects.create(
                    user=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    dob=parsed_dob,
                    email=email,
                    contact=contact,
                    subject=subject,
                    address=address
                )

            # Sync email with User model
            request.user.email = email
            request.user.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('teacher_profile')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'Teacher.html', {'staff': staff})



def student_marks(request):
    students = StudentMarks.objects.all().prefetch_related("exam_details")

    student_data = []
    for student in students:
        exams = student.exam_details.all()
        for exam in exams:
            student_data.append({
                "name": student.name,
                "email": student.email,
                "contact_number": student.contact_number,
                "maths_marks": exam.maths_marks,
                "biology_marks": exam.biology_marks,
                "chemistry_marks": exam.chemistry_marks,
                "physics_marks": exam.physics_marks,
                "total_marks": exam.total_marks,
                "percentage": exam.percentage,
            })

    return render(request, 'marks.html', {'students': student_data})


# View to handle combined exam and question paper creation
def create_exam_and_question_paper(request):
    if request.method == 'POST':
        # Handle the form submission for creating the exam and question paper
        
        # Get form data from the POST request
        exam_time = request.POST.get('exam_time')
        subject = request.POST.get('subject')
        chapter = request.POST.get('chapter')
        topic = request.POST.get('topic')
        total_marks = request.POST.get('total_marks')

        # Save the exam details to the database (ExamDetail model)
        exam = ExamDetail.objects.create(
            exam_time=exam_time,
            subject=subject,
            chapter=chapter,
            topic=topic,
            total_marks=total_marks,
            duration_minutes=request.POST.get('exam_duration')  # Assuming you have this in your form
        )

        # Handle the question paper upload
        uploaded_file = request.FILES.get('question_file')

        if uploaded_file:
            # Save the question paper to the database (QuestionPaper model)
            QuestionPaper.objects.create(
                subject=subject,
                chapter=chapter,
                topic=topic,
                question_file=uploaded_file
            )

        # Redirect to a success page or back to the create exam page
        return redirect('Create-exam')  # You can also redirect to another page like 'exam_success'

    # For GET request, return the create exam form
    return render(request, 'create_exam.html')  # Full page load for normal requests (create_exam.html form page)

def parent_result(request):
    student_data = None
    
    if request.method == "POST":
        # Get student name and email from the form submission
        student_name = request.POST.get('student_name')
        student_email = request.POST.get('student_email')

        # Simulate fetching student data based on name and email (Replace this with actual DB lookup)
        if student_name == "John Doe" and student_email == "john@example.com":
            student_data = {
                'name': 'John Doe',
                'course': 'JEE',  # This can be dynamic based on actual student data
                'physics_marks': 85,
                'chemistry_marks': 78,
                'biology_marks': 90,
                'mathematics_marks': 92,
            }

            # Calculate total marks and percentage
            total_marks = sum([student_data['physics_marks'], student_data['chemistry_marks'], student_data['biology_marks'], student_data['mathematics_marks']])
            percentage = (total_marks / 400) * 100  # Assuming total marks is 400 for 4 subjects

            # Add calculated fields to student data
            student_data['total_marks'] = total_marks
            student_data['percentage'] = round(percentage, 2)

    return render(request, 'parent-result.html', {'student': student_data})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Course, SchoolClass, Subject, Chapter, Topic, SubTopic
from django.views.decorators.http import require_POST

# ============ EDIT VIEWS ============

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course_name = request.POST.get('course_name', '').strip()
        if course_name:
            course.name = course_name
            course.save()
            messages.success(request, f'Course "{course_name}" updated successfully!')
        else:
            messages.error(request, 'Course name cannot be empty!')
    return redirect('manage_subjects')



def edit_class(request, class_id):
    classroom = get_object_or_404(SchoolClass, id=class_id)
    if request.method == 'POST':
        class_name = request.POST.get('class_name', '').strip()
        course_id = request.POST.get('course_id')
        
        if class_name and course_id:
            try:
                course = Course.objects.get(id=course_id)
                classroom.class_name = class_name
                classroom.course = course
                classroom.save()
                messages.success(request, f'Class "{class_name}" updated successfully!')
            except Course.DoesNotExist:
                messages.error(request, 'Invalid course selected!')
        else:
            messages.error(request, 'All fields are required!')
    return redirect('manage_subjects')



def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name', '').strip()
        class_id = request.POST.get('class_id')
        
        if subject_name and class_id:
            try:
                classroom = SchoolClass.objects.get(id=class_id)
                subject.name = subject_name
                subject.class_name = classroom
                subject.save()
                messages.success(request, f'Subject "{subject_name}" updated successfully!')
            except SchoolClass.DoesNotExist:
                messages.error(request, 'Invalid class selected!')
        else:
            messages.error(request, 'All fields are required!')
    return redirect('manage_subjects')



def edit_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.method == 'POST':
        chapter_name = request.POST.get('chapter_name', '').strip()
        subject_id = request.POST.get('subject_id')
        
        if chapter_name and subject_id:
            try:
                subject = Subject.objects.get(id=subject_id)
                chapter.name = chapter_name
                chapter.subject = subject
                chapter.save()
                messages.success(request, f'Chapter "{chapter_name}" updated successfully!')
            except Subject.DoesNotExist:
                messages.error(request, 'Invalid subject selected!')
        else:
            messages.error(request, 'All fields are required!')
    return redirect('manage_subjects')



def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        topic_name = request.POST.get('topic_name', '').strip()
        chapter_id = request.POST.get('chapter_id')
        
        if topic_name and chapter_id:
            try:
                chapter = Chapter.objects.get(id=chapter_id)
                topic.name = topic_name
                topic.chapter = chapter
                topic.save()
                messages.success(request, f'Topic "{topic_name}" updated successfully!')
            except Chapter.DoesNotExist:
                messages.error(request, 'Invalid chapter selected!')
        else:
            messages.error(request, 'All fields are required!')
    return redirect('manage_subjects')


def edit_subtopic(request, subtopic_id):
    subtopic = get_object_or_404(SubTopic, id=subtopic_id)
    if request.method == 'POST':
        subtopic_name = request.POST.get('subtopic_name', '').strip()
        topic_id = request.POST.get('topic_id')
        
        if subtopic_name and topic_id:
            try:
                topic = Topic.objects.get(id=topic_id)
                subtopic.name = subtopic_name
                subtopic.topic = topic
                subtopic.save()
                messages.success(request, f'Subtopic "{subtopic_name}" updated successfully!')
            except Topic.DoesNotExist:
                messages.error(request, 'Invalid topic selected!')
        else:
            messages.error(request, 'All fields are required!')
    return redirect('manage_subjects')






from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject, Question  # Assuming you have a base question model

@login_required
def addd_biology_question(request):
    # Get all subjects from database
    subjects = Subject.objects.all().prefetch_related('class_name')
    
    # Add chapters count to each subject
    for subject in subjects:
        subject.question_types = 'objective,descriptive,match_following,fill_in_the_blanks,numerical,true_false,short_answer,long_answer'
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        
        if not subject_id:
            messages.error(request, "Subject ID missing!")
            return redirect("addd_biology_question")

        try:
            with transaction.atomic():
                # Common fields for all questions
                chapter = request.POST.get("chapter", "").strip()
                topic = request.POST.get("topic", "").strip()
                question = request.POST.get("question", "").strip()
                question_type = request.POST.get("question_type", "").strip()
                marks = request.POST.get("marks", "1")
                difficulty = request.POST.get("difficulty", "medium")

                # Validate required fields
                if not all([chapter, topic, question_type, question, marks]):
                    messages.error(request, "Please fill all required fields")
                    return render(request, "mainstaff/add_question.html", {
                        "subjects": subjects
                    })

                # Get the subject object
                try:
                    subject_obj = Subject.objects.get(id=subject_id)
                except Subject.DoesNotExist:
                    messages.error(request, "Selected subject does not exist!")
                    return redirect("addd_biology_question")

                # Determine which model to use based on subject type or use a generic model
                # Assuming you have a generic Question model that handles all subjects
                from .models import Question  # Import your main Question model
                
                # Create base question object
                question_obj = Question(
                    subject=subject_obj,
                    chapter=chapter,
                    topic=topic,
                    question_type=question_type,
                    question=question,
                    marks=int(marks),
                    difficulty=difficulty,
                    created_by=request.user
                )
                
                # Handle different question types
                if question_type == "objective":
                    correct_options = request.POST.getlist("correct_options[]")
                    answer = ",".join(correct_options) if correct_options else ""
                    
                    question_obj.option1 = request.POST.get("option1", "").strip()
                    question_obj.option2 = request.POST.get("option2", "").strip()
                    question_obj.option3 = request.POST.get("option3", "").strip()
                    question_obj.option4 = request.POST.get("option4", "").strip()
                    question_obj.correct_options = answer
                    question_obj.answer = answer
                    
                elif question_type == "match_following":
                    match_items = request.POST.get("match_items", "").strip()
                    match_answers = request.POST.get("match_answers", "").strip()
                    match_count = request.POST.get("match_count", "4")
                    
                    question_obj.match_items = match_items
                    question_obj.match_answers = match_answers
                    question_obj.match_count = int(match_count) if match_count else 4
                    question_obj.answer = match_answers
                    
                elif question_type == "fill_in_the_blanks":
                    blank_answers = request.POST.get("blank_answers", "").strip()
                    blank_positions = request.POST.get("blank_positions", "").strip()
                    blank_count = request.POST.get("blank_count", "1")
                    
                    question_obj.blank_positions = blank_positions
                    question_obj.blank_count = int(blank_count) if blank_count else 1
                    question_obj.answer = blank_answers
                    
                elif question_type == "numerical":
                    numerical_solution = request.POST.get("numerical_solution", "").strip()
                    final_answer = request.POST.get("final_answer", "").strip()
                    
                    question_obj.numerical_solution = numerical_solution
                    question_obj.final_answer = final_answer
                    question_obj.answer = final_answer or numerical_solution
                    
                elif question_type == "true_false":
                    answer = request.POST.get("answer", "").strip()
                    question_obj.answer = answer
                    
                elif question_type in ["descriptive", "short_answer", "long_answer"]:
                    answer = request.POST.get("answer", "").strip()
                    question_obj.answer = answer
                    
                elif question_type == "equation_balancing":
                    chemical_equation = request.POST.get("chemical_equation", "").strip()
                    balanced_equation = request.POST.get("balanced_equation", "").strip()
                    balancing_steps = request.POST.get("balancing_steps", "").strip()
                    
                    question_obj.chemical_equation = chemical_equation
                    question_obj.balanced_equation = balanced_equation
                    question_obj.balancing_steps = balancing_steps
                    question_obj.answer = balanced_equation
                    
                elif question_type == "graph_based":
                    graph_type = request.POST.get("graph_type", "").strip()
                    graph_analysis = request.POST.get("graph_analysis", "").strip()
                    question_graph_image = request.FILES.get('question_graph_image')
                    
                    question_obj.graph_type = graph_type
                    question_obj.graph_analysis = graph_analysis
                    question_obj.question_graph_image = question_graph_image
                    question_obj.answer = graph_analysis
                    
                elif question_type == "diagram_based":
                    diagram_analysis = request.POST.get("diagram_analysis", "").strip()
                    diagram_image = request.FILES.get('diagram_image')
                    
                    question_obj.diagram_analysis = diagram_analysis
                    question_obj.diagram_image = diagram_image
                    question_obj.answer = diagram_analysis
                    
                elif question_type == "theorem":
                    theorem_statement = request.POST.get("theorem_statement", "").strip()
                    theorem_proof = request.POST.get("theorem_proof", "").strip()
                    theorem_diagram = request.FILES.get('theorem_diagram')
                    
                    question_obj.theorem_statement = theorem_statement
                    question_obj.theorem_proof = theorem_proof
                    question_obj.theorem_diagram = theorem_diagram
                    question_obj.answer = theorem_proof
                    
                else:
                    # For any other custom question type
                    answer = request.POST.get("answer", "").strip()
                    question_obj.answer = answer
                
                # Save the question
                question_obj.save()
                
                messages.success(request, f"Question added successfully to {subject_obj.name}! ID: {question_obj.id}")
                return redirect("addd_biology_question")

        except Exception as e:
            messages.error(request, f"Error saving question: {str(e)}")
            import traceback
            traceback.print_exc()

    # GET request - show form with subjects
    return render(request, "mainstaff/addd_biology_question.html", {
        "subjects": subjects
    })


@login_required
def view_all_questions(request):
    # View all questions from all subjects
    from .models import Question
    
    # Get filter parameters
    subject_filter = request.GET.get('subject', '')
    class_filter = request.GET.get('class', '')
    question_type_filter = request.GET.get('type', '')
    
    # Start with all questions
    questions = Question.objects.all().select_related('subject', 'subject__class_name')
    
    # Apply filters if provided
    if subject_filter:
        questions = questions.filter(subject__id=subject_filter)
    if class_filter:
        questions = questions.filter(subject__class_name__id=class_filter)
    if question_type_filter:
        questions = questions.filter(question_type=question_type_filter)
    
    # Get all subjects and classes for filter dropdowns
    all_subjects = Subject.objects.all()
    all_classes = SchoolClass.objects.all()  # Assuming you have a Class model
    
    context = {
        'questions': questions,
        'all_subjects': all_subjects,
        'all_classes': all_classes,
        'subject_filter': subject_filter,
        'class_filter': class_filter,
        'question_type_filter': question_type_filter,
    }
    
    return render(request, "mainstaff/view_all_question.html", context)


# views.py
from django.shortcuts import render
from .models import BiologyQuestion, ChemistryQuestion, PhysicsQuestion, MathematicsQuestion

@login_required
def view_biology_questions(request):
    """View all biology questions"""
    questions = BiologyQuestion.objects.all().order_by('-id')
    
    # Get unique chapters and topics for filters
    chapters = BiologyQuestion.objects.values_list('chapter', flat=True).distinct()
    topics = BiologyQuestion.objects.values_list('topic', flat=True).distinct()
    
    # Count by question type
    objective_count = questions.filter(question_type='objective').count()
    descriptive_count = questions.filter(question_type='descriptive').count()
    match_count = questions.filter(question_type='match_following').count()
    fill_count = questions.filter(question_type='fill_in_the_blanks').count()
    
    context = {
        'biology_questions': questions,
        'chapters': chapters,
        'topics': topics,
        'objective_count': objective_count,
        'descriptive_count': descriptive_count,
        'match_count': match_count,
        'fill_count': fill_count,
    }
    return render(request, 'mainstaff/view_biology.html', context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@login_required
def view_chemistry_questions(request):
    """View all chemistry questions with filtering and pagination"""
    # Get all questions ordered by latest first
    questions = ChemistryQuestion.objects.all().order_by('-id')
    
    # Get filter parameters from GET request
    chapter_filter = request.GET.get('chapter', '')
    topic_filter = request.GET.get('topic', '')
    type_filter = request.GET.get('type', '')
    search_query = request.GET.get('search', '')
    
    # Apply filters if provided
    if chapter_filter:
        questions = questions.filter(chapter=chapter_filter)
    
    if topic_filter:
        questions = questions.filter(topic=topic_filter)
    
    if type_filter:
        questions = questions.filter(question_type=type_filter)
    
    if search_query:
        questions = questions.filter(
            Q(chapter__icontains=search_query) |
            Q(topic__icontains=search_query) |
            Q(question__icontains=search_query) |
            Q(answer__icontains=search_query) |
            Q(option1__icontains=search_query) |
            Q(option2__icontains=search_query) |
            Q(option3__icontains=search_query) |
            Q(option4__icontains=search_query)
        )
    
    # Get unique chapters and topics for dropdowns (from filtered results)
    chapters = questions.values_list('chapter', flat=True).distinct().order_by('chapter')
    topics = questions.values_list('topic', flat=True).distinct().order_by('topic')
    
    # Calculate counts AFTER applying filters
    total_count = questions.count()
    objective_count = questions.filter(question_type='objective').count()
    descriptive_count = questions.filter(question_type='descriptive').count()
    numerical_count = questions.filter(question_type='numerical').count()
    equation_count = questions.filter(question_type='equation_balancing').count()
    match_following_count = questions.filter(question_type='match_following').count()
    
    # Pagination - Show 20 questions per page
    paginator = Paginator(questions, 20)
    page = request.GET.get('page', 1)
    
    try:
        paginated_questions = paginator.page(page)
    except PageNotAnInteger:
        paginated_questions = paginator.page(1)
    except EmptyPage:
        paginated_questions = paginator.page(paginator.num_pages)
    
    context = {
        'chemistry_questions': paginated_questions,
        'chapters': chapters,
        'topics': topics,
        'objective_count': objective_count,
        'descriptive_count': descriptive_count,
        'numerical_count': numerical_count,
        'equation_count': equation_count,
        'match_following_count': match_following_count,
        'total_questions': total_count,
        'active_questions_count': total_count,  # Assuming all are active
        
        # Pass filter values back to template to show current filters
        'current_chapter': chapter_filter,
        'current_topic': topic_filter,
        'current_type': type_filter,
        'search_query': search_query,
    }
    
    return render(request, 'mainstaff/view_chemistry.html', context)

@login_required
def view_physics_questions(request):
    """View all physics questions"""
    questions = PhysicsQuestion.objects.all().order_by('-id')
    
    chapters = PhysicsQuestion.objects.values_list('chapter', flat=True).distinct()
    topics = PhysicsQuestion.objects.values_list('topic', flat=True).distinct()
    
    objective_count = questions.filter(question_type='objective').count()
    descriptive_count = questions.filter(question_type='descriptive').count()
    numerical_count = questions.filter(question_type='numerical').count()
    graph_based_count = questions.filter(question_type='graph_based').count()
    diagram_based_count = questions.filter(question_type='diagram_based').count()
    match_count = questions.filter(question_type='match_following').count()
    
    context = {
        'physics_questions': questions,
        'chapters': chapters,
        'topics': topics,
        'objective_count': objective_count,
        'descriptive_count': descriptive_count,
        'numerical_count': numerical_count,
        'graph_based_count': graph_based_count,
        'diagram_based_count': diagram_based_count,
        'match_count': match_count,
    }
    return render(request, 'mainstaff/view_physics.html', context)

@login_required
def view_mathematics_questions(request):
    """View all mathematics questions"""
    questions = MathematicsQuestion.objects.all().order_by('-id')
    
    chapters = MathematicsQuestion.objects.values_list('chapter', flat=True).distinct()
    topics = MathematicsQuestion.objects.values_list('topic', flat=True).distinct()
    
    objective_count = questions.filter(question_type='objective').count()
    descriptive_count = questions.filter(question_type='descriptive').count()
    numerical_count = questions.filter(question_type='numerical').count()
    theorem_count = questions.filter(question_type='theorem').count()
    graph_based_count = questions.filter(question_type='graph_based').count()
    
    context = {
        'mathematics_questions': questions,
        'chapters': chapters,
        'topics': topics,
        'objective_count': objective_count,
        'descriptive_count': descriptive_count,
        'numerical_count': numerical_count,
        'theorem_count': theorem_count,
        'graph_based_count': graph_based_count,
    }
    return render(request, 'mainstaff/view_mathematics.html', context)

# ==================== DETAIL VIEWS ====================

@login_required
def view_biology_question_detail(request, question_id):
    """View details of a specific biology question"""
    question = get_object_or_404(BiologyQuestion, id=question_id)
    return render(request, 'question_detail.html', {
        'question': question,
        'subject': 'biology',
        'subject_name': 'Biology',
        'subject_color': '#1d976c'
    })

@login_required
def view_chemistry_question_detail(request, question_id):
    """View details of a specific chemistry question"""
    question = get_object_or_404(ChemistryQuestion, id=question_id)
    return render(request, 'question_detail.html', {
        'question': question,
        'subject': 'chemistry',
        'subject_name': 'Chemistry',
        'subject_color': '#6a11cb'
    })

@login_required
def view_physics_question_detail(request, question_id):
    """View details of a specific physics question"""
    question = get_object_or_404(PhysicsQuestion, id=question_id)
    return render(request, 'question_detail.html', {
        'question': question,
        'subject': 'physics',
        'subject_name': 'Physics',
        'subject_color': '#ff6b6b'
    })

@login_required
def view_mathematics_question_detail(request, question_id):
    """View details of a specific mathematics question"""
    question = get_object_or_404(MathematicsQuestion, id=question_id)
    return render(request, 'question_detail.html', {
        'question': question,
        'subject': 'mathematics',
        'subject_name': 'Mathematics',
        'subject_color': '#4facfe'
    })

# ==================== EDIT VIEWS ====================
from .forms import ChemistryQuestionForm
@login_required
def edit_chemistry_question(request, question_id):
    question = get_object_or_404(ChemistryQuestion, id=question_id)
    
    # Get correct options as list
    correct_options = []
    if question.correct_options:
        correct_options = question.correct_options.split(',')
    
    if request.method == 'POST':
        try:
            # Update question fields directly from POST data
            question.chapter = request.POST.get('chapter', '')
            question.topic = request.POST.get('topic', '')
            question.question_type = request.POST.get('question_type', '')
            
            # FIXED: Changed 'question_text' to 'question' to match the template
            question.question = request.POST.get('question', '')  # Changed this line
            
            question.answer = request.POST.get('answer', '')
            question.chemical_formula = request.POST.get('chemical_formula', '')
            question.equation = request.POST.get('equation', '')
            question.given_values = request.POST.get('given_values', '')
            question.solution_steps = request.POST.get('solution_steps', '')
            question.apparatus = request.POST.get('apparatus', '')
            question.procedure = request.POST.get('procedure', '')
            
            # Handle type-specific fields
            question_type = request.POST.get('question_type', '')
            
            if question_type == 'objective':
                question.option1 = request.POST.get('option1', '')
                question.option2 = request.POST.get('option2', '')
                question.option3 = request.POST.get('option3', '')
                question.option4 = request.POST.get('option4', '')
                
                # Handle correct options from checkboxes
                correct_opts = request.POST.getlist('correct_options[]', [])
                valid_options = [opt for opt in correct_opts if opt in ['1', '2', '3', '4']]
                question.correct_options = ','.join(valid_options)
            else:
                # Clear options for non-objective questions
                question.option1 = ''
                question.option2 = ''
                question.option3 = ''
                question.option4 = ''
                question.correct_options = ''
            
            # Handle numerical type specific fields
            if question_type == 'numerical':
                question.numerical_solution = request.POST.get('numerical_solution', '')
                question.final_answer = request.POST.get('final_answer', '')
            
            # Handle equation balancing type specific fields
            if question_type == 'equation_balancing':
                question.balanced_equation = request.POST.get('balanced_equation', '')
                question.answer_reaction_type = request.POST.get('answer_reaction_type', '')
                question.balancing_steps = request.POST.get('balancing_steps', '')
            
            # Handle match following type specific fields
            if question_type == 'match_following':
                question.match_items = request.POST.get('match_items', '')
                question.match_answers = request.POST.get('match_answers', '')
                question.match_count = request.POST.get('match_count', 4)
            
            # Handle file upload
            if 'diagram_image' in request.FILES:
                question.diagram_image = request.FILES['diagram_image']
            
            # Auto-update the updated_at timestamp
            question.updated_at = timezone.now()
            
            # Save the question
            question.save()
            
            messages.success(request, 'Chemistry question updated successfully!')
            return redirect('add_chemistry_question')  # Or redirect to view_chemistry_questions
            
        except Exception as e:
            print(f"Error updating question: {e}")
            messages.error(request, f'Error updating question: {str(e)}')
    
    # For GET request, prepare context with question data
    context = {
        'question': question,
        'correct_options': correct_options,
        'subject': 'chemistry',
        'subject_name': 'Chemistry',
        'subject_color': '#f39c12'
    }
    
    return render(request, 'admin/edit_chemestry_question.html', context)



@login_required
def edit_physics_question(request, question_id):
    """Edit a physics question"""
    question = get_object_or_404(PhysicsQuestion, id=question_id)
    
    # Parse correct options for initial display
    if question.correct_options:
        # Convert string like "['1', '3']" to list ['1', '3']
        try:
            import ast
            correct_options = ast.literal_eval(question.correct_options)
        except:
            # If parsing fails, try to extract numbers
            import re
            correct_options = re.findall(r'\d', question.correct_options)
    else:
        correct_options = []
    
    if request.method == 'POST':
        # Get all form data
        chapter = request.POST.get('chapter', '').strip()
        topic = request.POST.get('topic', '').strip()
        question_text = request.POST.get('question', '').strip()
        question_type = request.POST.get('question_type', '').strip()
        answer = request.POST.get('answer', '').strip()
        
        # Update basic fields
        question.chapter = chapter
        question.topic = topic
        question.question = question_text
        question.question_type = question_type
        question.answer = answer
        
        # Handle question type specific fields
        if question_type == 'objective':
            question.option1 = request.POST.get('option1', '').strip()
            question.option2 = request.POST.get('option2', '').strip()
            question.option3 = request.POST.get('option3', '').strip()
            question.option4 = request.POST.get('option4', '').strip()
            
            # Get correct options as list
            correct_options = request.POST.getlist('correct_options[]')
            question.correct_options = str(correct_options)
            
        elif question_type == 'numerical':
            question.formula = request.POST.get('formula', '').strip()
            question.units = request.POST.get('units', '').strip()
            question.given_values = request.POST.get('given_values', '').strip()
            question.solution_steps = request.POST.get('solution_steps', '').strip()
            question.numerical_solution = request.POST.get('numerical_solution', '').strip()
            question.final_answer = request.POST.get('final_answer', '').strip()
            
        elif question_type == 'graph_based':
            question.graph_type = request.POST.get('graph_type', '').strip()
            question.graph_xlabel = request.POST.get('graph_xlabel', '').strip()
            question.graph_ylabel = request.POST.get('graph_ylabel', '').strip()
            question.graph_data = request.POST.get('graph_data', '').strip()
            question.graph_interpretation = request.POST.get('graph_interpretation', '').strip()
            question.graph_calculations = request.POST.get('graph_calculations', '').strip()
            question.graph_observations = request.POST.get('graph_observations', '').strip()
            
            # Handle file uploads
            if 'question_graph_image' in request.FILES:
                question.question_graph_image = request.FILES['question_graph_image']
            if 'answer_graph_image' in request.FILES:
                question.answer_graph_image = request.FILES['answer_graph_image']
                
        elif question_type == 'diagram_based':
            question.diagram_description = request.POST.get('diagram_description', '').strip()
            question.diagram_labels = request.POST.get('diagram_labels', '').strip()
            question.diagram_analysis = request.POST.get('diagram_analysis', '').strip()
            
            # Handle file uploads
            if 'diagram_image' in request.FILES:
                question.diagram_image = request.FILES['diagram_image']
            if 'labeled_diagram' in request.FILES:
                question.labeled_diagram = request.FILES['labeled_diagram']
                
        elif question_type == 'match_following':
            question.match_items = request.POST.get('match_items', '').strip()
            question.match_count = request.POST.get('match_count', 4)
            question.match_answers = request.POST.get('match_answers', '').strip()
        
        try:
            question.save()
            messages.success(request, 'Physics question updated successfully!')
            return redirect('add_physics_question')
        except Exception as e:
            messages.error(request, f'Error updating question: {str(e)}')
    
    # For GET request, render template with existing data
    # Extract all unique chapters and topics for filters
    all_questions = PhysicsQuestion.objects.all()
    chapters = sorted(set(q.chapter for q in all_questions if q.chapter))
    topics = sorted(set(q.topic for q in all_questions if q.topic))
    
    # Count question types for stats
    objective_count = all_questions.filter(question_type='objective').count()
    descriptive_count = all_questions.filter(question_type='descriptive').count()
    numerical_count = all_questions.filter(question_type='numerical').count()
    graph_based_count = all_questions.filter(question_type='graph_based').count()
    diagram_based_count = all_questions.filter(question_type='diagram_based').count()
    match_following_count = all_questions.filter(question_type='match_following').count()
    
    return render(request, 'admin/edit_physics_question.html', {
        'question': question,
        'correct_options': correct_options,
        'chapters': chapters,
        'topics': topics,
        'objective_count': objective_count,
        'descriptive_count': descriptive_count,
        'numerical_count': numerical_count,
        'graph_based_count': graph_based_count,
        'diagram_based_count': diagram_based_count,
        'match_following_count': match_following_count,
        'total_questions': all_questions.count()
    })



@login_required
def delete_physics_question(request, question_id):
    question = get_object_or_404(PhysicsQuestion, id=question_id)
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Physics question deleted successfully!')
        return redirect('add_physics_question')
    
    messages.error(request, 'Invalid request method.')
    return redirect('view_physics_questions')


from .forms import MathematicsQuestionForm

@login_required
def edit_mathematics_question(request, question_id):
    """Edit a mathematics question"""
    question = get_object_or_404(MathematicsQuestion, id=question_id)

    if request.method == 'POST':
        print("\n=== EDIT MATHEMATICS QUESTION ===")
        print("POST Data received:")
        for key, value in request.POST.items():
            print(f"  {key}: {value}")
        
        print("\nFILES received:")
        for key in request.FILES:
            print(f"  {key}: {request.FILES[key].name}")
        
        # Get all form data
        chapter = request.POST.get('chapter', '').strip()
        topic = request.POST.get('topic', '').strip()
        question_text = request.POST.get('question', '').strip()
        question_type = request.POST.get('question_type', '').strip()
        
        # Validate required fields
        if not chapter or not topic or not question_text or not question_type:
            messages.error(request, 'Please fill all required fields')
            return render(request, 'admin/edit_mathematics_question.html', {
                'question': question,
                'subject': 'mathematics',
                'subject_name': 'Mathematics',
                'subject_color': '#4facfe'
            })
        
        # Update basic fields
        question.chapter = chapter
        question.topic = topic
        question.question = question_text
        question.question_type = question_type
        
        # Handle question type specific fields
        if question_type == 'objective':
            question.option1 = request.POST.get('option1', '').strip()
            question.option2 = request.POST.get('option2', '').strip()
            question.option3 = request.POST.get('option3', '').strip()
            question.option4 = request.POST.get('option4', '').strip()
            
            # Handle correct options
            correct_options = request.POST.getlist('correct_options')
            print(f"Correct options: {correct_options}")
            question.correct_options = ','.join(correct_options) if correct_options else ''
            
            # Clear other fields
            fields_to_clear = [
                'answer', 'formula', 'equation_latex', 'given_values', 
                'step_solution', 'final_answer', 'theorem_statement', 
                'theorem_proof', 'theorem_applications', 'graph_type',
                'function_equation', 'graph_points', 'graph_analysis',
                'graph_keypoints', 'graph_calculations'
            ]
            for field in fields_to_clear:
                setattr(question, field, '')
                
        elif question_type == 'numerical':
            question.formula = request.POST.get('formula', '').strip()
            question.equation_latex = request.POST.get('equation_latex', '').strip()
            question.given_values = request.POST.get('given_values', '').strip()
            question.step_solution = request.POST.get('step_solution', '').strip()
            question.final_answer = request.POST.get('final_answer', '').strip()
            
            # Clear other fields
            fields_to_clear = [
                'option1', 'option2', 'option3', 'option4', 'correct_options',
                'answer', 'theorem_statement', 'theorem_proof', 
                'theorem_applications', 'graph_type', 'function_equation', 
                'graph_points', 'graph_analysis', 'graph_keypoints', 
                'graph_calculations'
            ]
            for field in fields_to_clear:
                setattr(question, field, '')
                
        elif question_type == 'theorem':
            question.theorem_statement = request.POST.get('theorem_statement', '').strip()
            question.theorem_proof = request.POST.get('theorem_proof', '').strip()
            question.theorem_applications = request.POST.get('theorem_applications', '').strip()
            
            # Clear other fields
            fields_to_clear = [
                'option1', 'option2', 'option3', 'option4', 'correct_options',
                'answer', 'formula', 'equation_latex', 'given_values',
                'step_solution', 'final_answer', 'graph_type',
                'function_equation', 'graph_points', 'graph_analysis',
                'graph_keypoints', 'graph_calculations'
            ]
            for field in fields_to_clear:
                setattr(question, field, '')
                
        elif question_type == 'graph_based':
            question.graph_type = request.POST.get('graph_type', '').strip()
            question.function_equation = request.POST.get('function_equation', '').strip()
            question.graph_points = request.POST.get('graph_points', '').strip()
            question.graph_analysis = request.POST.get('graph_analysis', '').strip()
            question.graph_keypoints = request.POST.get('graph_keypoints', '').strip()
            question.graph_calculations = request.POST.get('graph_calculations', '').strip()
            
            # Clear other fields
            fields_to_clear = [
                'option1', 'option2', 'option3', 'option4', 'correct_options',
                'answer', 'formula', 'equation_latex', 'given_values',
                'step_solution', 'final_answer', 'theorem_statement',
                'theorem_proof', 'theorem_applications'
            ]
            for field in fields_to_clear:
                setattr(question, field, '')
                
        else:  # descriptive
            question.answer = request.POST.get('answer', '').strip()
            
            # Clear other fields
            fields_to_clear = [
                'option1', 'option2', 'option3', 'option4', 'correct_options',
                'formula', 'equation_latex', 'given_values', 'step_solution',
                'final_answer', 'theorem_statement', 'theorem_proof',
                'theorem_applications', 'graph_type', 'function_equation',
                'graph_points', 'graph_analysis', 'graph_keypoints',
                'graph_calculations'
            ]
            for field in fields_to_clear:
                setattr(question, field, '')
        
        # Handle file uploads
        try:
            # Handle theorem diagram
            if 'theorem_diagram' in request.FILES:
                theorem_file = request.FILES['theorem_diagram']
                # Validate file size (5MB limit)
                if theorem_file.size > 5 * 1024 * 1024:
                    messages.error(request, 'Theorem diagram file is too large (max 5MB)')
                    return render(request, 'admin/edit_mathematics_question.html', {
                        'question': question,
                        'subject': 'mathematics',
                        'subject_name': 'Mathematics',
                        'subject_color': '#4facfe'
                    })
                
                # Delete old file if exists
                if question.theorem_diagram:
                    question.theorem_diagram.delete(save=False)
                
                question.theorem_diagram = theorem_file
                print(f"Theorem diagram uploaded: {theorem_file.name}")
                
            elif 'clear_theorem_diagram' in request.POST:
                # Clear the image
                if question.theorem_diagram:
                    question.theorem_diagram.delete(save=False)
                    question.theorem_diagram = None
                    print("Theorem diagram cleared")
            
            # Handle graph image
            if 'graph_image' in request.FILES:
                graph_file = request.FILES['graph_image']
                # Validate file size (5MB limit)
                if graph_file.size > 5 * 1024 * 1024:
                    messages.error(request, 'Graph image file is too large (max 5MB)')
                    return render(request, 'admin/edit_mathematics_question.html', {
                        'question': question,
                        'subject': 'mathematics',
                        'subject_name': 'Mathematics',
                        'subject_color': '#4facfe'
                    })
                
                # Delete old file if exists
                if question.graph_image:
                    question.graph_image.delete(save=False)
                
                question.graph_image = graph_file
                print(f"Graph image uploaded: {graph_file.name}")
                
            elif 'clear_graph_image' in request.POST:
                # Clear the image
                if question.graph_image:
                    question.graph_image.delete(save=False)
                    question.graph_image = None
                    print("Graph image cleared")
                    
        except Exception as e:
            print(f"File upload error: {e}")
            messages.error(request, f'Error uploading file: {str(e)}')
        
        # Save the question
        try:
            question.save()
            print("Question saved successfully!")
            messages.success(request, 'Mathematics question updated successfully!')
            return redirect('add_mathematics_question')
        except Exception as e:
            print(f"Save error: {e}")
            messages.error(request, f'Error updating question: {str(e)}')
    
    # For GET request, just pass the question
    return render(request, 'admin/edit_mathematics_question.html', {
        'question': question,
        'subject': 'mathematics',
        'subject_name': 'Mathematics',
        'subject_color': '#4facfe'
    })


@login_required
def delete_mathematics_question(request, question_id):
    question = get_object_or_404(MathematicsQuestion, id=question_id)
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Mathematics question deleted successfully!')
        return redirect('add_mathematics_question')
    
    messages.error(request, 'Invalid request method.')
    return redirect('view_mathematics_questions')


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def delete_chemistry_question(request, question_id):
    """Delete a chemistry question"""
    question = get_object_or_404(ChemistryQuestion, id=question_id)
    
    if request.method == 'POST':
        # Get question text for message
        question_text = question.question[:50]
        
        # Delete the question
        question.delete()
        
        messages.success(request, f'Chemistry question "{question_text}..." deleted successfully!')
        return redirect('add_chemistry_question')
    
    # If not POST, redirect back to questions list
    return redirect('view_chemistry_questions')




@login_required
def view_biology_question_detail(request, question_id):
    """View to display details of a single Biology question."""
    try:
        question = get_object_or_404(BiologyQuestion, id=question_id)
        
        # Parse match items if exists
        match_items_list = []
        if question.match_items:
            for line in question.match_items.split('\n'):
                if line.strip():  # Skip empty lines
                    if '-' in line:
                        left, right = line.split('-', 1)
                        match_items_list.append({
                            'left': left.strip(),
                            'right': right.strip()
                        })
        
        # Parse correct options
        correct_options_list = []
        if question.correct_options:
            # If stored as string like "1,3"
            if isinstance(question.correct_options, str):
                correct_options_list = question.correct_options.split(',')
            else:
                correct_options_list = question.correct_options
        
        context = {
            'question': question,
            'match_items_list': match_items_list,
            'correct_options_list': correct_options_list,
            'option_letters': ['A', 'B', 'C', 'D', 'E'],
            'has_options': any([question.option1, question.option2, question.option3, question.option4])
        }
        
        return render(request, 'Admin/view_biology_question_detail.html', context)
        
    except BiologyQuestion.DoesNotExist:
        messages.error(request, "Question not found!")
        return redirect('addd_biology_question')

@login_required
def edit_biology_question(request, question_id):
    """View to edit a Biology question."""
    question = get_object_or_404(BiologyQuestion, id=question_id)
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                question.chapter = request.POST.get("chapter", "").strip()
                question.topic = request.POST.get("topic", "").strip()
                question.question_type = request.POST.get("question_type", "").strip()
                question.question = request.POST.get("question", "").strip()
                
                # Update based on question type
                if question.question_type == "objective":
                    correct_options = request.POST.getlist("correct_options[]")
                    question.answer = ",".join(correct_options) if correct_options else ""
                    question.correct_options = question.answer
                    question.option1 = request.POST.get("option1", "").strip()
                    question.option2 = request.POST.get("option2", "").strip()
                    question.option3 = request.POST.get("option3", "").strip()
                    question.option4 = request.POST.get("option4", "").strip()
                    
                elif question.question_type == "match_following":
                    question.answer = request.POST.get("answer", "").strip()
                    question.match_items = request.POST.get("match_items", "").strip()
                    question.match_count = int(request.POST.get("match_count", 0))
                    
                elif question.question_type == "fill_in_the_blanks":
                    question.answer = request.POST.get("answer", "").strip()
                    question.blank_positions = request.POST.get("blank_positions", "").strip()
                    question.blank_count = int(request.POST.get("blank_count", 1))
                    
                else:  # descriptive
                    question.answer = request.POST.get("answer", "").strip()
                
                question.updated_at = timezone.now()
                question.save()
                
                messages.success(request, f"Biology question '{question.id}' updated successfully!")
                return redirect("addd_biology_question")
                
        except Exception as e:
            messages.error(request, f"Error updating question: {str(e)}")
    
    # GET request → show edit form
    context = {
        "question": question,
        "correct_options": question.correct_options.split(',') if question.correct_options else [],
    }
    return render(request, "Admin/edit_biology_question.html", context)

@login_required
def delete_biology_question(request, question_id):
    """View to delete a Biology question."""
    if request.method == "POST":
        try:
            question = get_object_or_404(BiologyQuestion, id=question_id)
            question_id = question.id
            question.delete()
            messages.success(request, f"Biology question '{question_id}' deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting question: {str(e)}")
    
    return redirect("addd_biology_question")

@login_required
def admin_biology_dashboard(request):
    """Admin dashboard for Biology questions."""
    biology_questions = BiologyQuestion.objects.all().order_by('-created_at')
    
    # Get statistics
    total_count = biology_questions.count()
    objective_count = biology_questions.filter(question_type="objective").count()
    descriptive_count = biology_questions.filter(question_type="descriptive").count()
    match_count = biology_questions.filter(question_type="match_following").count()
    fill_count = biology_questions.filter(question_type="fill_in_the_blanks").count()
    
    # Get unique chapters and topics for filters
    chapters = biology_questions.order_by('chapter').values_list('chapter', flat=True).distinct()
    topics = biology_questions.order_by('topic').values_list('topic', flat=True).distinct()
    
    context = {
        "biology_questions": biology_questions,
        "total_count": total_count,
        "objective_count": objective_count,
        "descriptive_count": descriptive_count,
        "match_count": match_count,
        "fill_count": fill_count,
        "chapters": chapters,
        "topics": topics,
    }
    
    return render(request, "Admin/admin_biology_dashboard.html", context)

# ============ Views for other subjects ============

@login_required
def admin_chemistry_dashboard(request):
    """Admin dashboard for Chemistry questions."""
    chemistry_questions = ChemistryQuestion.objects.all().order_by('-created_at')
    
    context = {
        "chemistry_questions": chemistry_questions,
    }
    return render(request, "Admin/admin_chemistry_dashboard.html", context)

@login_required
def admin_physics_dashboard(request):
    """Admin dashboard for Physics questions."""
    physics_questions = PhysicsQuestion.objects.all().order_by('-created_at')
    
    context = {
        "physics_questions": physics_questions,
    }
    return render(request, "Admin/admin_physics_dashboard.html", context)

@login_required
def admin_mathematics_dashboard(request):
    """Admin dashboard for Mathematics questions."""
    mathematics_questions = MathematicsQuestion.objects.all().order_by('-created_at')
    
    context = {
        "mathematics_questions": mathematics_questions,
    }
    return render(request, "Admin/admin_mathematics_dashboard.html", context)




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import BiologyQuestion
from django.utils import timezone

@login_required
def add_biology_question(request):
    """View to add and list Biology questions."""
    
    # Fetch ALL biology questions ordered by latest first
    biology_questions = BiologyQuestion.objects.all().order_by('-created_at')
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                chapter = request.POST.get("chapter", "").strip()
                topic = request.POST.get("topic", "").strip()
                question_type = request.POST.get("question_type", "").strip()
                question = request.POST.get("question", "").strip()
                answer = request.POST.get("answer", "").strip()
                
                # Validate required fields
                if not all([chapter, topic, question_type, question]):
                    messages.error(request, "Please fill all required fields (Chapter, Topic, Question Type, Question)")
                    return render(request, "add_biology_question.html", {
                        "biology_questions": biology_questions
                    })
                
                # Biology specific fields
                formula = request.POST.get("formula", "").strip()
                diagram_reference = request.POST.get("diagram_reference", "").strip()
                
                # Handle file upload (diagram_image)
                diagram_image = request.FILES.get('diagram_image')
                
                # Handle options for objective questions
                option1 = request.POST.get("option1", "").strip()
                option2 = request.POST.get("option2", "").strip()
                option3 = request.POST.get("option3", "").strip()
                option4 = request.POST.get("option4", "").strip()
                option5 = request.POST.get("option5", "").strip()
                
                # Handle correct options (can be multiple for MCQ)
                correct_options = request.POST.getlist("correct_options[]")
                
                # 🔴 MERGED FIX (ONLY THIS PART ADDED)
                if question_type == "objective":
                    option_map = {
                        '1': 'A',
                        '2': 'B',
                        '3': 'C',
                        '4': 'D',
                        '5': 'E',
                    }
                    answer = ", ".join(
                        option_map[o] for o in correct_options if o in option_map
                    )
                
                # For match_following question type
                match_items = request.POST.get("match_items", "").strip()
                match_count = request.POST.get("match_count", "").strip()
                
                # For fill_in_the_blanks question type
                blank_positions = request.POST.get("blank_positions", "").strip()
                blank_count = request.POST.get("blank_count", "").strip()
                
                # Create question object
                new_question = BiologyQuestion.objects.create(
                    chapter=chapter,
                    topic=topic,
                    question_type=question_type,
                    question=question,
                    answer=answer,
                    formula=formula,
                    diagram_reference=diagram_reference,
                    diagram_image=diagram_image,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    option5=option5,
                    correct_options=correct_options,
                    match_items=match_items,
                    match_count=match_count,
                    blank_positions=blank_positions,
                    blank_count=blank_count,
                    created_by=request.user
                )
                
                messages.success(request, f"Biology question '{new_question.id}' added successfully!")
                return redirect("add_biology_question")
                
        except Exception as e:
            messages.error(request, f"Error adding question: {str(e)}")
            return render(request, "add_biology_question.html", {
                "biology_questions": biology_questions,
                "form_data": request.POST
            })
    
    # GET request → show all questions
    context = {
        "biology_questions": biology_questions,
        "objective_count": biology_questions.filter(question_type="objective").count(),
        "descriptive_count": biology_questions.filter(question_type="descriptive").count(),
        "match_count": biology_questions.filter(question_type="match_following").count(),
        "fill_count": biology_questions.filter(question_type="fill_in_the_blanks").count(),
        "chapters": biology_questions.order_by('chapter').values_list('chapter', flat=True).distinct(),
        "topics": biology_questions.order_by('topic').values_list('topic', flat=True).distinct(),
    }
    return render(request, "add_biology_question.html", context)


@login_required
def view_biology_question_detail(request, question_id):
    """View to display details of a single Biology question."""
    try:
        question = get_object_or_404(BiologyQuestion, id=question_id)
        
        # Parse match items if exists
        match_items_list = []
        if question.match_items:
            for line in question.match_items.split('\n'):
                if '-' in line:
                    left, right = line.split('-', 1)
                    match_items_list.append({
                        'left': left.strip(),
                        'right': right.strip()
                    })
        
        # Parse correct options
        correct_options_list = []
        if question.correct_options:
            correct_options_list = question.correct_options
        
        context = {
            'question': question,
            'match_items_list': match_items_list,
            'correct_options_list': correct_options_list,
            'option_letters': ['A', 'B', 'C', 'D', 'E'],
            'has_options': any([question.option1, question.option2, question.option3, question.option4, question.option5])
        }
        
        return render(request, 'Admin/view_biology_question_detail.html', context)
        
    except BiologyQuestion.DoesNotExist:
        messages.error(request, "Question not found!")
        return redirect('add_biology_question')

@login_required
def edit_biology_question(request, question_id):
    """View to edit a Biology question."""
    question = get_object_or_404(BiologyQuestion, id=question_id)
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                question.chapter = request.POST.get("chapter", "").strip()
                question.topic = request.POST.get("topic", "").strip()
                question.question_type = request.POST.get("question_type", "").strip()
                question.question = request.POST.get("question", "").strip()
                question.answer = request.POST.get("answer", "").strip()
                
                # Biology specific fields
                question.formula = request.POST.get("formula", "").strip()
                question.diagram_reference = request.POST.get("diagram_reference", "").strip()
                
                # Handle file upload (diagram_image)
                if 'diagram_image' in request.FILES:
                    question.diagram_image = request.FILES['diagram_image']
                
                # Handle options for objective questions
                question.option1 = request.POST.get("option1", "").strip()
                question.option2 = request.POST.get("option2", "").strip()
                question.option3 = request.POST.get("option3", "").strip()
                question.option4 = request.POST.get("option4", "").strip()
                question.option5 = request.POST.get("option5", "").strip()
                
                # Handle correct options
                question.correct_options = request.POST.getlist("correct_options[]")
                
                # For match_following question type
                question.match_items = request.POST.get("match_items", "").strip()
                question.match_count = request.POST.get("match_count", "").strip()
                
                # For fill_in_the_blanks question type
                question.blank_positions = request.POST.get("blank_positions", "").strip()
                question.blank_count = request.POST.get("blank_count", "").strip()
                
                question.updated_at = timezone.now()
                question.updated_by = request.user
                question.save()
                
                messages.success(request, f"Biology question '{question.id}' updated successfully!")
                return redirect("add_biology_question")
                
        except Exception as e:
            messages.error(request, f"Error updating question: {str(e)}")
    
    # GET request → show edit form
    context = {
        "question": question,
        "correct_options": question.correct_options or [],
    }
    return render(request, "Admin/edit_biology_question.html", context)

@login_required
def delete_biology_question(request, question_id):
    """View to delete a Biology question."""
    if request.method == "POST":
        try:
            question = get_object_or_404(BiologyQuestion, id=question_id)
            question_id = question.id
            question.delete()
            messages.success(request, f"Biology question '{question_id}' deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting question: {str(e)}")
    
    return redirect("add_biology_question")

@login_required
def admin_biology_dashboard(request):
    """Admin dashboard for Biology questions."""
    biology_questions = BiologyQuestion.objects.all().order_by('-created_at')
    
    # Get statistics
    total_count = biology_questions.count()
    objective_count = biology_questions.filter(question_type="objective").count()
    descriptive_count = biology_questions.filter(question_type="descriptive").count()
    match_count = biology_questions.filter(question_type="match_following").count()
    fill_count = biology_questions.filter(question_type="fill_in_the_blanks").count()
    
    # Get unique chapters and topics for filters
    chapters = biology_questions.order_by('chapter').values_list('chapter', flat=True).distinct()
    topics = biology_questions.order_by('topic').values_list('topic', flat=True).distinct()
    
    context = {
        "biology_questions": biology_questions,
        "total_count": total_count,
        "objective_count": objective_count,
        "descriptive_count": descriptive_count,
        "match_count": match_count,
        "fill_count": fill_count,
        "chapters": chapters,
        "topics": topics,
    }
    
    return render(request, "Admin/admin_biology_dashboard.html", context)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ChemistryQuestion
from django.contrib.auth.decorators import login_required

@login_required
def add_chemistry_question(request):

    chemistry_questions = ChemistryQuestion.objects.all()

    if request.method == "POST":

        chapter = request.POST.get("chapter")
        topic = request.POST.get("topic")
        question_type = request.POST.get("question_type")
        question = request.POST.get("question")
        answer = request.POST.get("answer")

        # Chemistry-specific fields
        chemical_equation = request.POST.get("chemical_equation")
        chemical_formula = request.POST.get("chemical_formula")
        reaction_type = request.POST.get("reaction_type")
        equation_latex = request.POST.get("equation_latex")

        # File fields
        question_image = request.FILES.get("diagram_image")
        answer_image = request.FILES.get("answer_image")

        # Objective options
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")
        option5 = request.POST.get("option5")
        correct_option = request.POST.get("correct_option")

        try:
            ChemistryQuestion.objects.create(
                chapter=chapter,
                topic=topic,
                question_type=question_type,
                question=question,
                answer=answer,

                # chemistry fields
                chemical_equation=chemical_equation,
                chemical_formula=chemical_formula,
                reaction_type=reaction_type,
                equation_latex=equation_latex,

                # Images
                diagram_image=question_image,
                answer_image=answer_image,

                # For Objective Type Questions
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                option5=option5,
                correct_option=correct_option,
            )

            messages.success(request, "Chemistry question added successfully!")
            return redirect("add_chemistry_question")

        except Exception as e:
            messages.error(request, f"Error adding question: {str(e)}")

    return render(request, "add_chemistry_question.html", {
        "chemistry_questions": chemistry_questions
    })



@login_required
def view_chemistry_question_detail(request, question_id):
    """View to show full details of a single Chemistry question"""
    
    # Get the specific question
    question = get_object_or_404(ChemistryQuestion, id=question_id)
    
    return render(request, 'Admin/chemistry_question_detail.html', {
        'question': question
    })

@login_required
def add_physics_question(request):
    """View to add and list Physics questions."""
    
    # Fetch ALL physics questions
    physics_questions = PhysicsQuestion.objects.all()
    
    if request.method == "POST":
        chapter = request.POST.get("chapter")
        topic = request.POST.get("topic")
        sub_topic = request.POST.get("sub_topic")
        marks = request.POST.get("marks", 0)
        
        question_type = request.POST.get("question_type")
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        
        # Objective question options
        option1 = request.POST.get("option1", "")
        option2 = request.POST.get("option2", "")
        option3 = request.POST.get("option3", "")
        option4 = request.POST.get("option4", "")
        option5 = request.POST.get("option5", "")
        correct_option = request.POST.get("correct_option", None)
        
        try:
            # Create question object
            PhysicsQuestion.objects.create(
                chapter=chapter,
                topic=topic,
                sub_topic=sub_topic,
                marks=marks,
                question_type=question_type,
                question=question,
                answer=answer,
                
                # Only save objective fields if type = objective
                option1=option1 if question_type == "objective" else None,
                option2=option2 if question_type == "objective" else None,
                option3=option3 if question_type == "objective" else None,
                option4=option4 if question_type == "objective" else None,
                option5=option5 if question_type == "objective" else None,
                correct_option=int(correct_option) if correct_option and question_type == "objective" else None,
            )
            
            messages.success(request, "Physics question added successfully!")
            return redirect("add_physics_question")
            
        except Exception as e:
            messages.error(request, f"Error adding question: {str(e)}")
    
    # GET request → show all questions
    return render(request, "add_physics_question.html", {
        "physics_questions": physics_questions
    })

@login_required
def view_physics_question_detail(request, question_id):
    """View to display details of a single Physics question."""
    try:
        question = PhysicsQuestion.objects.get(id=question_id)
        return render(request, 'Admin/view_physics_question_detail.html', {
            'question': question
        })
    except PhysicsQuestion.DoesNotExist:
        messages.error(request, "Question not found!")
        return redirect('add_physics_question')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MathematicsQuestion


@login_required
def add_mathematics_question(request):
    """View to add and list Mathematics questions (same structure as Chemistry)."""

    # Fetch ALL math questions
    math_questions = MathematicsQuestion.objects.all()

    if request.method == "POST":
        chapter = request.POST.get("chapter")
        topic = request.POST.get("topic")
        # Remove these if you don't need them:
        # sub_topic = request.POST.get("sub_topic")
        # marks = request.POST.get("marks", 0)

        formula = request.POST.get("formula", "")
        characters = request.POST.get("characters", "")

        question_type = request.POST.get("question_type")
        question = request.POST.get("question")
        answer = request.POST.get("answer")

        # Objective question options
        option1 = request.POST.get("option1", "")
        option2 = request.POST.get("option2", "")
        option3 = request.POST.get("option3", "")
        option4 = request.POST.get("option4", "")
        option5 = request.POST.get("option5", "")
        correct_option = request.POST.get("correct_option", None)

        try:
            # Create question object
            MathematicsQuestion.objects.create(
                chapter=chapter,
                topic=topic,
                formula=formula,
                characters=characters,
                question_type=question_type,
                question=question,
                answer=answer,

                # Only save objective fields if type = objective
                option1=option1 if question_type == "objective" else None,
                option2=option2 if question_type == "objective" else None,
                option3=option3 if question_type == "objective" else None,
                option4=option4 if question_type == "objective" else None,
                option5=option5 if question_type == "objective" else None,
                correct_option=int(correct_option) if correct_option and question_type == "objective" else None,
            )

            messages.success(request, "Mathematics question added successfully!")
            return redirect("add_mathematics_question")

        except Exception as e:
            messages.error(request, f"Error adding question: {str(e)}")

    # GET request → show all questions
    return render(request, "add_mathematics_question.html", {
        # CHANGE THIS: Use consistent variable name
        "mathematics_questions": math_questions  # Changed from "math_questions"
    })


@login_required
def view_mathematics_question_detail(request, question_id):
    """View to display details of a single Mathematics question."""
    try:
        question = MathematicsQuestion.objects.get(id=question_id)
        return render(request, 'Admin/view_mathematics_question_detail.html', {
            'question': question
        })
    except MathematicsQuestion.DoesNotExist:
        messages.error(request, "Question not found!")
        return redirect('add_mathematics_question')



# Add these imports at the top
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.conf import settings
from .models import GeneratedQuestionPaper
from .utils.pdf_generator import QuestionPaperPDFGenerator

# In views.py - Add this view
@csrf_exempt
@login_required
def save_question_paper(request):
    """Save generated question paper to database"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create the paper
            paper = GeneratedQuestionPaper.objects.create(
                title=data.get('title', 'Generated Question Paper'),
                description=data.get('description', ''),
                
                # School info
                school_name=data.get('school_name', ''),
                school_address=data.get('school_address', ''),
                school_contact=data.get('school_contact', ''),
                affiliation_number=data.get('affiliation_number', ''),
                
                # Exam details
                exam_name=data.get('exam_name', 'Exam'),
                class_name=data.get('class_name', ''),
                course_name=data.get('course_name', ''),
                total_marks=data.get('total_marks', 100),
                time_duration=data.get('time_duration', '3 hours'),
                exam_date=data.get('exam_date'),
                
                # Instructions
                instructions=data.get('instructions', ''),
                logo_position=data.get('logo_position', 'left'),
                
                # Content
                question_data=data.get('selected_questions', []),
                paper_html=data.get('paper_html', ''),
                
                # Additional elements
                additional_elements=data.get('additional_elements', []),
                
                # Statistics
                total_questions=data.get('total_questions', 0),
                subjects_included=data.get('subjects_included', []),
                
                # CRITICAL: Publishing flags
                is_published=data.get('is_published', False),
                status=data.get('status', 'draft'),
                
                # Metadata
                created_by=request.user
            )
            
            # If published, also set exam_time for student exams
            if paper.is_published and paper.time_duration:
                # Extract minutes from time_duration string
                import re
                time_match = re.search(r'(\d+)\s*hours?', paper.time_duration)
                if time_match:
                    hours = int(time_match.group(1))
                    paper.exam_time = hours * 60  # Convert to minutes
                else:
                    paper.exam_time = 180  # Default 3 hours
                paper.save()
            
            return JsonResponse({
                'success': True,
                'paper_id': paper.id,
                'title': paper.title,
                'is_published': paper.is_published,
                'message': 'Paper saved successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def generate_and_download_pdf(request):
    """Generate and download PDF directly"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    try:
        data = json.loads(request.body)
        
        # Prepare paper data
        paper_data = prepare_paper_data(data)
        
        # Generate PDF
        pdf_bytes = QuestionPaperPDFGenerator.generate_pdf(paper_data)
        
        if not pdf_bytes:
            return JsonResponse({'success': False, 'error': 'Failed to generate PDF'})
        
        # Create HTTP response with PDF
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        filename = f"{paper_data['exam_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(pdf_bytes)
        
        return response
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def download_saved_paper(request, unique_id):
    """Download a previously saved question paper"""
    try:
        paper = GeneratedQuestionPaper.objects.get(unique_id=unique_id)
        
        if paper.pdf_file and paper.pdf_file.storage.exists(paper.pdf_file.name):
            # Serve the existing PDF
            response = HttpResponse(paper.pdf_file.read(), content_type='application/pdf')
            filename = f"{paper.exam_name.replace(' ', '_')}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            # Regenerate PDF if not exists
            pdf_bytes = QuestionPaperPDFGenerator.generate_pdf(paper.question_data)
            
            if pdf_bytes:
                response = HttpResponse(pdf_bytes, content_type='application/pdf')
                filename = f"{paper.exam_name.replace(' ', '_')}.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                response['Content-Length'] = len(pdf_bytes)
                return response
            else:
                return JsonResponse({'success': False, 'error': 'Failed to generate PDF'})
                
    except GeneratedQuestionPaper.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Paper not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def preview_paper(request, unique_id):
    """Preview a saved question paper"""
    try:
        paper = GeneratedQuestionPaper.objects.get(unique_id=unique_id)
        
        context = {
            'paper': paper,
            'question_data': paper.question_data,
            'can_edit': paper.created_by == request.user or request.user.is_staff,
        }
        
        return render(request, 'preview_question_paper.html', context)
        
    except GeneratedQuestionPaper.DoesNotExist:
        messages.error(request, "Question paper not found.")
        return redirect('question_paper_generator')

@login_required
def list_generated_papers(request):
    """List all generated question papers"""
    papers = GeneratedQuestionPaper.objects.filter(created_by=request.user).order_by('-created_at')
    
    return render(request, 'list_generated_papers.html', {
        'papers': papers,
        'title': 'My Generated Question Papers'
    })

# Utility functions
def prepare_paper_data(data):
    """Prepare paper data for PDF generation"""
    # This function extracts and formats data from the frontend
    paper_data = {
        'school_name': data.get('schoolName', 'Your School Name'),
        'school_address': data.get('schoolAddress', 'City, State, PIN Code'),
        'school_contact': data.get('schoolContact', 'Phone: 1234567890 | Email: school@example.com'),
        'affiliation_number': data.get('affiliationNo', ''),
        
        'exam_name': data.get('examName', 'Mid-Term Examination'),
        'class_name': data.get('classFilter', ''),
        'course_name': data.get('courseFilter', ''),
        'total_marks': int(data.get('totalMarks', 100)),
        'time_duration': data.get('timeDuration', '3 hours'),
        'exam_date': data.get('examDate', ''),
        'exam_date_formatted': format_exam_date(data.get('examDate')),
        
        'instructions': data.get('instructions', ''),
        'logo_position': data.get('logoPosition', 'left'),
        
        'sections': [],
        'watermark': None,
        'signatures': [],
        'show_footer': True,
    }
    
    # Process sections
    sections_data = {
        'mcq': {'title': 'Section A: Objective Questions', 'instructions': 'Choose the correct option.'},
        'short': {'title': 'Section B: Subjective Questions', 'instructions': 'Answer the following questions briefly.'},
        'long': {'title': 'Section C: Applied Questions', 'instructions': 'Answer the following questions in detail.'},
    }
    
    for section_key, section_info in sections_data.items():
        section_questions = get_questions_from_section(data, section_key)
        if section_questions:
            paper_data['sections'].append({
                'title': section_info['title'],
                'instructions': section_info['instructions'],
                'questions': section_questions
            })
    
    # Process additional elements
    additional_elements = []
    for element in data.get('additionalElements', []):
        if element.get('type') == 'watermark':
            paper_data['watermark'] = element.get('config', {})
        elif element.get('type') == 'signature':
            paper_data['signatures'] = element.get('config', {}).get('signatures', [])
        elif element.get('type') == 'footer':
            paper_data['show_footer'] = True
        else:
            additional_elements.append(element)
    
    paper_data['additional_elements'] = additional_elements
    
    return paper_data

def get_questions_from_section(data, section_key):
    """Extract questions from a specific section"""
    questions = []
    section_data = data.get(f'{section_key}Questions', [])
    
    for question_id in section_data:
        # Find the question in allQuestions
        question = find_question_by_id(data.get('allQuestions', []), question_id)
        if question:
            # Format the question for display
            formatted_question = {
                'id': question.get('id'),
                'question_text': question.get('question', ''),
                'marks': question.get('marks', 1),
                'type': question.get('type'),
                'options': format_options(question),
                'subject': question.get('subject_name', ''),
                'chapter': question.get('chapter', ''),
            }
            questions.append(formatted_question)
    
    return questions

def find_question_by_id(all_questions, question_id):
    """Find a question by ID in the list"""
    for question in all_questions:
        if str(question.get('id')) == str(question_id):
            return question
    return None

def format_options(question):
    """Format MCQ options for display"""
    if question.get('type') != 'objective':
        return None
    
    options = []
    option_letters = ['A', 'B', 'C', 'D', 'E']
    
    for i in range(1, 6):
        option_text = question.get(f'option{i}', '')
        if option_text:
            options.append({
                'letter': option_letters[i-1],
                'text': option_text
            })
    
    return options if options else None

def format_exam_date(date_str):
    """Format exam date for display"""
    if not date_str:
        return ''
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d %B %Y')
    except:
        return date_str

def generate_paper_html(paper_data):
    """Generate HTML representation of the paper"""
    from django.template.loader import render_to_string
    
    return render_to_string('pdf/question_paper_template.html', {
        'paper': paper_data,
        'logo_path': None,  # Will be handled separately
    })



def exam_schedule(request, template_name):
    exams = ExamSchedule.objects.all()  # Fetch all exam schedules
    return render(request, template_name, {'exams': exams})  # Pass exams to the template


def add_exam_schedule(request):
    exams = ExamSchedule.objects.all()  # Fetch all exams
    return render(request, 'Teacher.html', {'exams': exams})  # Render in teacher dashboard

def save_exam_details(request):
    if request.method == "POST":
        exam_date_str = request.POST.get('exam_date')
        exam_time_str = request.POST.get('exam_time')
        exam_subject = request.POST.get('exam_subject')

        if exam_date_str and exam_time_str and exam_subject:
            try:
                exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
                exam_time = datetime.strptime(exam_time_str, "%H:%M").time()

                # Save exam schedule to database
                ExamSchedule.objects.create(
                    exam_date=exam_date,
                    exam_time=exam_time,
                    exam_subject=exam_subject
                )

                messages.success(request, 'Exam added successfully!')

            except ValueError as e:
                messages.error(request, f"Invalid date/time format. Error: {e}")

    return redirect('exam_schedule')

def get_exam_details(request):
    exams = ExamSchedule.objects.all()  # Fetch all exams from the database
    return render(request, 'Parent.html', {'exams': exams})  # Pass exams to the template

def get_admin_exam_details(request):
    exams = ExamSchedule.objects.all()  # Fetch all exams
    return render(request, 'admin-dashboard.html', {'exams': exams})  # Pass exams to the template

def payment_list(request):
    return render(request, 'payment_list.html')  # Ensure you have a correct template

@staff_member_required
def pack(request):
    purchases = PackagePurchase.objects.all()
    form = AddPackageForm()

    if request.method == "POST":
        form = AddPackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.added_by_admin = True  # Mark that admin added this package
            package.purchase_date = now()
            package.save()
            return redirect('admin_pack')

    return render(request, "pack.html", {"purchases": purchases, "form": form})

@staff_member_required
def remove_purchase(request, purchase_id):
    purchase = get_object_or_404(PackagePurchase, id=purchase_id)
    purchase.delete()
    return redirect('pack.html')

#feedback schedule
def submit_feedback(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")

        Feedback_review.objects.create(name=name, email=email, message=message)
        return HttpResponse("<script>window.alert('thankyou for the feedback.');window.location.href='/student/';</script>")

    return render(request, "feedback.html")

def feedback_list(request):
    feedbacks = Feedback_review.objects.all()
    return render(request, 'admin_feedback.html', {'feedback_list': feedbacks})

def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback_review, id=feedback_id)
    feedback.delete()
    return redirect('feedback_list')  # Ensure this name matches your URL pattern

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StudentProfile

@login_required
def student_profile(request):
    """Handle student profile creation and update"""
    
    # Try to get existing student profile
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        is_edit = True
    except StudentProfile.DoesNotExist:
        student_profile = None
        is_edit = False
    
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        date_of_birth = request.POST.get("date_of_birth")
        mobile_number = request.POST.get("mobile_number", "").strip()
        email = request.POST.get("email", "").strip()
        guardian_name = request.POST.get("guardian_name", "").strip()
        guardian_number = request.POST.get("guardian_number", "").strip()
        address = request.POST.get("address", "").strip()
        pin_code = request.POST.get("pin_code", "").strip()
        gender = request.POST.get("gender")
        course_applied_for = request.POST.get("course_applied_for")

        # Academic details
        classX_board = request.POST.get("classX_board", "").strip()
        classX_percentage = request.POST.get("classX_percentage")
        classX_year = request.POST.get("classX_year")
        
        classXII_board = request.POST.get("classXII_board", "").strip()
        classXII_percentage = request.POST.get("classXII_percentage")
        classXII_year = request.POST.get("classXII_year")

        # Validate required fields
        if not all([first_name, last_name, date_of_birth, mobile_number, email, 
                   guardian_name, guardian_number, address, pin_code, gender, course_applied_for]):
            messages.error(request, "Please fill all required fields.")
            return render(request, "student.html", {
                "data": {"username": request.user.username},
                "student_profile": student_profile,
                "is_edit": is_edit,
                "form_data": request.POST
            })

        # Check if email is already used by another user (if changed)
        if email != request.user.email:
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, "Email already exists. Please use another email.")
                return render(request, "student.html", {
                    "data": {"username": request.user.username},
                    "student_profile": student_profile,
                    "is_edit": is_edit,
                    "form_data": request.POST
                })
            # Update user email if changed
            request.user.email = email
            request.user.save()

        try:
            # Update existing profile or create new one
            if student_profile:
                # Update existing profile
                student_profile.first_name = first_name
                student_profile.last_name = last_name
                student_profile.date_of_birth = date_of_birth
                student_profile.mobile_number = mobile_number
                student_profile.email = email
                student_profile.guardian_name = guardian_name
                student_profile.guardian_number = guardian_number
                student_profile.address = address
                student_profile.pin_code = pin_code
                student_profile.gender = gender
                student_profile.course_applied_for = course_applied_for
                student_profile.classX_board = classX_board
                student_profile.classX_percentage = classX_percentage
                student_profile.classX_year = classX_year
                student_profile.classXII_board = classXII_board
                student_profile.classXII_percentage = classXII_percentage
                student_profile.classXII_year = classXII_year
                
                student_profile.save()
                messages.success(request, "Profile updated successfully!")
            else:
                # Create new profile
                student_profile = StudentProfile.objects.create(
                    user=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth,
                    mobile_number=mobile_number,
                    email=email,
                    guardian_name=guardian_name,
                    guardian_number=guardian_number,
                    address=address,
                    pin_code=pin_code,
                    gender=gender,
                    course_applied_for=course_applied_for,
                    classX_board=classX_board,
                    classX_percentage=classX_percentage,
                    classX_year=classX_year,
                    classXII_board=classXII_board,
                    classXII_percentage=classXII_percentage,
                    classXII_year=classXII_year,
                )
                messages.success(request, "Profile created successfully!")
            
            # Also update user's first_name and last_name
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()

            return redirect('Student1')

        except Exception as e:
            messages.error(request, f"Error saving profile: {str(e)}")
            return render(request, "student.html", {
                "data": {"username": request.user.username},
                "student_profile": student_profile,
                "is_edit": is_edit,
                "form_data": request.POST
            })

    # GET request - show form with existing data
    context = {
        "data": {"username": request.user.username},
        "student_profile": student_profile,
        "is_edit": is_edit,
    }
    
    return render(request, "student.html", context)


def question_list(request):
    questions = QuestionPaper.objects.all()
    return render(request, "question_list.html", {"questions": questions})



def feedback_staff(request):
    feedbacks = Feedback_review.objects.all().order_by('-created_at')  # Latest feedback first
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})


def search_students(request):
    query = request.GET.get('q', '').strip()
    print(f"Search Query: {query}")

    # Search results
    students = []
    if query:
        students = StudentProfile.objects.filter(
            first_name__icontains=query
        ) | StudentProfile.objects.filter(
            last_name__icontains=query
        )
        print(f"Students Found: {students}")

    # Always get all students for the full list
    all_students = StudentProfile.objects.all().order_by("first_name")

    print(f"All Students Count: {all_students.count()}")
    print(f"Search Results Count: {students.count() if query else 0}")

    return render(request, 'search_students.html', {
        'students': students,  # Pass the QuerySet directly, not custom dict
        'query': query,
        'student_list': all_students
    })


def pass_fail_chart(request):
    # Sample data (fetch from database in real implementation)
    total_students = 200
    pass_percentage = 75
    fail_percentage = 100 - pass_percentage

    context = {
        'total_students': total_students,
        'pass_percentage': pass_percentage,
        'fail_percentage': fail_percentage
    }
    
    return render(request, 'pass_fail_chart.html', context)

from django.shortcuts import render
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Question, Subject, SchoolClass

def view_all_question(request):
    # Get filter parameters
    class_filter = request.GET.get('class', '')
    subject_filter = request.GET.get('subject', '')
    question_type_filter = request.GET.get('type', '')
    difficulty_filter = request.GET.get('difficulty', '')
    
    # Start with all questions - OPTIMIZE QUERYSET
    # Remove prefetch_related('tags') if you don't have tags field
    questions = Question.objects.all().select_related('subject', 'created_by')
    
    # Apply filters
    if class_filter:
        questions = questions.filter(subject__class_name_id=class_filter)
    
    if subject_filter:
        questions = questions.filter(subject_id=subject_filter)
    
    if question_type_filter:
        questions = questions.filter(question_type=question_type_filter)
    
    if difficulty_filter:
        questions = questions.filter(difficulty=difficulty_filter)
    
    # Get statistics counts (filtered if applicable)
    # FIX: Use correct question_type values from your model
    mcq_count = questions.filter(question_type='objective').count()
    descriptive_count = questions.filter(question_type='descriptive').count()
    match_count = questions.filter(question_type='match_following').count()
    fill_count = questions.filter(question_type='fill_in_the_blanks').count()
    numerical_count = questions.filter(question_type='numerical').count()
    true_false_count = questions.filter(question_type='true_false').count()
    short_answer_count = questions.filter(question_type='short_answer').count()
    long_answer_count = questions.filter(question_type='long_answer').count()
    diagram_count = questions.filter(question_type='diagram_based').count()
    graph_count = questions.filter(question_type='graph_based').count()
    
    # Get all classes and subjects for filter dropdowns
    all_classes = SchoolClass.objects.all()
    all_subjects = Subject.objects.all()
    
    # If class filter is applied, filter subjects by class
    if class_filter:
        all_subjects = all_subjects.filter(class_name_id=class_filter)
    
    # Pagination
    paginator = Paginator(questions, 12)  # Show 12 questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'questions': page_obj,
        'all_classes': all_classes,
        'all_subjects': all_subjects,
        'class_filter': class_filter,
        'subject_filter': subject_filter,
        'question_type_filter': question_type_filter,
        'difficulty_filter': difficulty_filter,
        'mcq_count': mcq_count,
        'descriptive_count': descriptive_count,
        'match_count': match_count,
        'fill_count': fill_count,
        'numerical_count': numerical_count,
        'true_false_count': true_false_count,
        'short_answer_count': short_answer_count,
        'long_answer_count': long_answer_count,
        'diagram_count': diagram_count,
        'graph_count': graph_count,
        'total_count': paginator.count,
    }
    
    return render(request, 'mainstaff/view_all_question.html', context)


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Question, Subject


@login_required
def view_question_detail(request, question_id):
    """View question details page"""
    question = get_object_or_404(Question, id=question_id)
    context = {
        'question': question,
        'title': f'Question #{question.id} - Details'
    }
    return render(request, 'mainstaff/Question Details.html', context)

@login_required
def edit_question(request, question_id):
    """Edit question page without Django forms"""
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        try:
            # Get all form data
            subject_id = request.POST.get('subject')
            question_type = request.POST.get('question_type')
            chapter = request.POST.get('chapter', '').strip()
            topic = request.POST.get('topic', '').strip()
            difficulty = request.POST.get('difficulty')
            marks = request.POST.get('marks', 1)
            question_text = request.POST.get('question')
            answer = request.POST.get('answer', '').strip()
            explanation = request.POST.get('explanation', '').strip()
            reference = request.POST.get('reference', '').strip()
            
            # Get subject
            subject = Subject.objects.get(id=subject_id)
            
            # Update question fields
            question.subject = subject
            question.question_type = question_type
            question.chapter = chapter
            question.topic = topic
            question.difficulty = difficulty
            question.marks = int(marks) if marks else 1
            question.question = question_text
            question.answer = answer
            question.explanation = explanation
            question.reference = reference
            
            # Handle question type specific fields
            if question_type == 'objective':
                question.option1 = request.POST.get('option1', '').strip()
                question.option2 = request.POST.get('option2', '').strip()
                question.option3 = request.POST.get('option3', '').strip()
                question.option4 = request.POST.get('option4', '').strip()
                question.correct_options = request.POST.getlist('correct_options')
            
            elif question_type == 'true_false':
                question.answer = request.POST.get('answer', 'true').strip()
            
            elif question_type == 'fill_in_the_blanks':
                question.blank_answers = request.POST.get('blank_answers', '').strip()
            
            elif question_type == 'match_following':
                question.match_answers = request.POST.get('match_answers', '').strip()
            
            elif question_type == 'numerical':
                question.final_answer = request.POST.get('final_answer', '').strip()
            
            # Handle ALL image file uploads
            if 'image' in request.FILES:
                question.image = request.FILES['image']
            
            if 'diagram' in request.FILES:
                question.diagram = request.FILES['diagram']
            
            # NEW: Handle additional image fields
            if 'question_graph_image' in request.FILES:
                question.question_graph_image = request.FILES['question_graph_image']
            
            if 'diagram_image' in request.FILES:
                question.diagram_image = request.FILES['diagram_image']
            
            if 'theorem_diagram' in request.FILES:
                question.theorem_diagram = request.FILES['theorem_diagram']
            
            # NEW: Handle image removal if checkbox is present (optional feature)
            # You can add this if you want to allow deleting images
            if 'remove_question_graph_image' in request.POST:
                question.question_graph_image.delete(save=False)
                question.question_graph_image = None
            
            if 'remove_diagram_image' in request.POST:
                question.diagram_image.delete(save=False)
                question.diagram_image = None
            
            if 'remove_theorem_diagram' in request.POST:
                question.theorem_diagram.delete(save=False)
                question.theorem_diagram = None
            
            if 'remove_image' in request.POST:
                question.image.delete(save=False)
                question.image = None
            
            if 'remove_diagram' in request.POST:
                question.diagram.delete(save=False)
                question.diagram = None
            
            # Save the question
            question.save()
            
            messages.success(request, f'Question #{question.id} has been updated successfully!')
            return redirect('view_question_detail', question_id=question.id)
            
        except Subject.DoesNotExist:
            messages.error(request, 'Selected subject does not exist.')
        except Exception as e:
            messages.error(request, f'Error updating question: {str(e)}')
            # For debugging, you can print the error
            print(f"Error: {str(e)}")
    
    # Get all subjects for the dropdown
    subjects = Subject.objects.all().select_related('class_name')
    
    context = {
        'question': question,
        'subjects': subjects,
        'title': f'Edit Question #{question.id}'
    }
    return render(request, 'mainstaff/Edit Question.html', context)




@login_required
def delete_question(request, question_id):
    """Delete question"""
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        question_id = question.id
        question.delete()
        messages.success(request, f'Question #{question_id} has been deleted successfully!')
        return redirect('view_all_question')
    
    # If not POST, show confirmation page
    context = {
        'question': question,
        'title': f'Delete Question #{question.id}'
    }
    return render(request, 'question_bank/delete_confirm.html', context)

# Add this API view for AJAX calls (for your existing modal)
from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
def get_question_detail_api(request, question_id):
    """API endpoint for question details (used in modal)"""
    question = get_object_or_404(Question, id=question_id)
    
    # Generate type badge
    type_badge = get_type_badge(question.question_type)
    
    # Generate difficulty badge
    difficulty_badge = get_difficulty_badge(question.difficulty)
    
    # Generate MCQ options HTML if applicable
    mcq_options = ''
    if question.question_type == 'objective':
        mcq_options = render_to_string('question_bank/partials/mcq_options.html', {
            'question': question
        })
    
    data = {
        'id': question.id,
        'subject': question.subject.name,
        'class': question.subject.class_name.class_name,
        'chapter': question.chapter or 'Not specified',
        'topic': question.topic or 'Not specified',
        'question': question.question,
        'answer': question.answer or 'No answer provided',
        'marks': question.marks,
        'created_at': question.created_at.strftime('%B %d, %Y'),
        'type_badge': type_badge,
        'difficulty_badge': difficulty_badge,
        'mcq_options': mcq_options
    }
    
    return JsonResponse(data)

def get_type_badge(question_type):
    """Helper function to generate type badge HTML"""
    badges = {
        'objective': '<span class="type-badge type-mcq"><i class="fas fa-list-ul me-1"></i>MCQ</span>',
        'descriptive': '<span class="type-badge type-descriptive"><i class="fas fa-align-left me-1"></i>Descriptive</span>',
        'match_following': '<span class="type-badge type-match"><i class="fas fa-link me-1"></i>Match</span>',
        'fill_in_the_blanks': '<span class="type-badge type-fill"><i class="fas fa-edit me-1"></i>Fill</span>',
        'numerical': '<span class="type-badge type-num"><i class="fas fa-calculator me-1"></i>Num</span>',
        'true_false': '<span class="type-badge type-tf"><i class="fas fa-check-double me-1"></i>T/F</span>',
        'short_answer': '<span class="type-badge type-short"><i class="fas fa-pen-alt me-1"></i>Short</span>',
        'long_answer': '<span class="type-badge type-long"><i class="fas fa-file-alt me-1"></i>Long</span>',
        'diagram_based': '<span class="type-badge type-diag"><i class="fas fa-draw-polygon me-1"></i>Diag</span>',
    }
    return badges.get(question_type, f'<span class="type-badge type-default">{question_type}</span>')

def get_difficulty_badge(difficulty):
    """Helper function to generate difficulty badge HTML"""
    badges = {
        'easy': '<span class="difficulty-badge difficulty-easy"><i class="fas fa-thermometer-empty me-1"></i>Easy</span>',
        'medium': '<span class="difficulty-badge difficulty-medium"><i class="fas fa-thermometer-half me-1"></i>Medium</span>',
        'hard': '<span class="difficulty-badge difficulty-hard"><i class="fas fa-thermometer-full me-1"></i>Hard</span>',
    }
    return badges.get(difficulty, f'<span class="difficulty-badge">{difficulty}</span>')




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def auto_generate_paper(request):
    """Simple view that just shows the auto-generator"""
    context = {
        'current_date': datetime.now().strftime("%Y-%m-%d")
    }
    return render(request, 'teacher/auto_generate_paper.html', context)

@login_required
def save_generated_paper(request):
    """Save auto-generated paper to database"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        # Create question paper
        from .models import QuestionPaper
        paper = QuestionPaper.objects.create(
            title=data.get('title'),
            exam_time=data.get('time'),
            total_marks=data.get('marks'),
            created_by=request.user
        )
        
        # Return success
        return JsonResponse({'success': True, 'paper_id': paper.id})
    
    return JsonResponse({'success': False})


@login_required
def get_questions_ajax(request):
    """AJAX endpoint to get filtered questions"""
    subject = request.GET.get('subject')
    question_type = request.GET.get('type', 'all')
    
    # Map subject to model
    model_map = {
        'mathematics': MathematicsQuestion,
        'physics': PhysicsQuestion,
        'chemistry': ChemistryQuestion,
        'biology': BiologyQuestion
    }
    
    if subject not in model_map:
        return JsonResponse({'questions': []})
    
    Model = model_map[subject]
    queryset = Model.objects.all()
    
    if question_type != 'all':
        queryset = queryset.filter(question_type=question_type)
    
    questions = []
    for q in queryset[:50]:
        questions.append({
            'id': q.id,
            'text': q.question[:200] + '...' if len(q.question) > 200 else q.question,
            'type': q.question_type,
            'chapter': q.chapter[:50] if q.chapter else 'General',
            'marks': 4  # Default marks
        })
    
    return JsonResponse({'questions': questions})


@login_required
def get_questions_api(request):
    """API endpoint to get questions for AJAX"""
    subject = request.GET.get('subject', '')
    question_type = request.GET.get('type', 'all')
    
    questions = []
    
    # Get questions based on subject
    if subject == 'mathematics':
        queryset = MathematicsQuestion.objects.all()
    elif subject == 'physics':
        queryset = PhysicsQuestion.objects.all()
    elif subject == 'chemistry':
        queryset = ChemistryQuestion.objects.all()
    elif subject == 'biology':
        queryset = BiologyQuestion.objects.all()
    else:
        return JsonResponse({'questions': []})
    
    # Filter by type if not 'all'
    if question_type != 'all':
        queryset = queryset.filter(question_type=question_type)
    
    # Limit to 50 questions for performance
    queryset = queryset[:50]
    
    # Format questions for JSON response
    for q in queryset:
        questions.append({
            'id': q.id,
            'text': q.question[:150] + '...' if len(q.question) > 150 else q.question,
            'type': q.get_question_type_display() if hasattr(q, 'get_question_type_display') else q.question_type,
            'chapter': q.chapter[:50] if q.chapter else 'No chapter',
            'marks': 4,  # Default marks for JEE/NEET
            'has_image': bool(q.diagram_image) if hasattr(q, 'diagram_image') else False,
        })
    
    return JsonResponse({'questions': questions})


@login_required
def view_question_paper(request, paper_id):
    """View a created question paper"""
    question_paper = get_object_or_404(QuestionPaper, id=paper_id, created_by=request.user)
    
    context = {
        'paper': question_paper,
        'math_questions': question_paper.mathematics_questions.all(),
        'physics_questions': question_paper.physics_questions.all(),
        'chemistry_questions': question_paper.chemistry_questions.all(),
        'biology_questions': question_paper.biology_questions.all(),
    }
    
    return render(request, 'teacher/view_question_paper.html', context)


@login_required
def teacher_question_papers(request):
    """List all question papers created by teacher"""
    papers = QuestionPaper.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'papers': papers,
    }
    
    return render(request, 'teacher/question_papers.html', context)


@login_required
def view_question_paper(request, paper_id):
    """View a specific question paper"""
    question_paper = get_object_or_404(QuestionPaper, id=paper_id)
    
    # Check if user has permission (teacher or student)
    if not question_paper.is_published and request.user != question_paper.created_by:
        messages.error(request, "This question paper is not published yet.")
        return redirect("teacher_dashboard")
    
    context = {
        "paper": question_paper,
        "is_teacher": request.user == question_paper.created_by or request.user.is_staff
    }
    return render(request, "question_paper/view.html", context)

@login_required
def student_question_papers(request):
    """View for students to see available question papers"""
    # Get published papers and papers assigned to the student
    published_papers = QuestionPaper.objects.filter(
        is_published=True,
        exam_date_actual__gte=timezone.now().date()  # Future or today's papers
    ).order_by('exam_date_actual', 'exam_start_time')
    
    context = {
        "question_papers": published_papers,
        "now": timezone.now()
    }
    return render(request, "student/question_papers.html", context)

# In views.py - Add these views
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from django.utils import timezone

# views.py - In your student_start_exam view
@login_required
def start_exam(request, paper_id):
    """Student starts an exam"""
    try:
        # Get paper and verify access
        paper = get_object_or_404(GeneratedQuestionPaper, id=paper_id)
        
        # Get teacher settings for this paper
        from .models import TeacherPaperSettings
        
        teacher_settings = None
        if paper.created_by:
            try:
                teacher_settings = TeacherPaperSettings.objects.get(teacher=paper.created_by)
            except TeacherPaperSettings.DoesNotExist:
                teacher_settings = TeacherPaperSettings.objects.create(
                    teacher=paper.created_by,
                    school_name='Your School Name',
                    school_address='City, State, PIN Code',
                    school_contact='Phone: 1234567890 | Email: school@example.com',
                    affiliation_number='Affiliation No: 123456',
                    logo_position='center',
                    default_exam_name='Mid-Term Examination',
                    default_total_marks=100,
                    default_time_duration='3 hours'
                )
        
        # Parse question data
        all_questions = []
        if paper.question_data:
            try:
                # Handle different question data formats
                if isinstance(paper.question_data, dict):
                    questions = paper.question_data.get('selected_questions', [])
                    if isinstance(questions, list):
                        all_questions = questions
                    elif isinstance(questions, dict):
                        all_questions = list(questions.values())
                elif isinstance(paper.question_data, list):
                    all_questions = paper.question_data
            except Exception as e:
                print(f"Error parsing question data: {e}")
                all_questions = []
        
        # Get teacher logo URL if exists
        logo_url = None
        if teacher_settings and teacher_settings.logo_image:
            try:
                logo_url = teacher_settings.logo_image.url
            except:
                logo_url = None
        
        # Store in session
        request.session['current_exam_id'] = paper_id
        request.session['exam_start_time'] = timezone.now().isoformat()
        request.session['exam_questions'] = all_questions
        request.session['exam_answers'] = {}
        request.session['current_question_index'] = 0
        
        # Set exam duration
        exam_duration = paper.exam_time or 180  # Default 3 hours in minutes
        request.session['exam_duration_minutes'] = exam_duration
        
        # Calculate exam time in seconds
        exam_time_seconds = exam_duration * 60
        
        context = {
            'paper': paper,
            'teacher_settings': teacher_settings,
            'all_questions': all_questions,
            'total_questions': len(all_questions),
            'exam_time_seconds': exam_time_seconds,
            'student': request.user,
        }
        
        return render(request, 'student_start_exam.html', context)
        
    except Exception as e:
        print(f"Error starting exam: {e}")
        messages.error(request, "Error loading exam. Please try again.")
        return redirect('student_available_exams')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
import json
import os

@login_required
@user_passes_test(lambda u: u.user_type == 2)  # Only teachers
def teacher_pending_evaluations(request):
    """Show all exam submissions pending correction"""
    try:
        # FIXED: Only use StudentExamSubmission which has 'status' field
        pending_submissions = StudentExamSubmission.objects.filter(
            status='submitted'
        ).select_related('student', 'generated_paper', 'question_paper').order_by('-submitted_at')
        
        # FIXED: Don't filter ExamResult by status if field doesn't exist
        # Just get recent exam results without status filter
        exam_results = ExamResult.objects.all().select_related('student', 'paper', 'question_paper').order_by('-submitted_at')[:10]
        
        context = {
            'pending_submissions': pending_submissions,
            'exam_results': exam_results,
            'pending_submissions_count': pending_submissions.count(),
            'title': '📝 Correction Exam'
        }
        
        return render(request, 'pending_evaluations.html', context)
        
    except Exception as e:
        print(f"Error in teacher_pending_evaluations: {str(e)}")
        messages.error(request, f"Error loading evaluations: {str(e)}")
        return redirect('Teacher')


@login_required
@user_passes_test(lambda u: u.user_type == 2)  # Only teachers
def teacher_evaluate_exam(request, submission_id):
    """Teacher evaluates exam - can see answer key from database"""
    try:
        # Get submission
        submission = get_object_or_404(
            StudentExamSubmission.objects.select_related(
                'student', 'generated_paper', 'question_paper'
            ),
            id=submission_id
        )
        
        # Get the paper
        paper = submission.paper
        
        # Check if we have existing evaluation data
        existing_question_marks = submission.question_marks or {}
        
        # Get all questions with their CORRECT ANSWERS from database
        questions_with_answers = []
        
        if paper and paper.question_data:
            try:
                # Parse question data
                if isinstance(paper.question_data, dict):
                    raw_questions = paper.question_data.get('selected_questions', [])
                elif isinstance(paper.question_data, list):
                    raw_questions = paper.question_data
                else:
                    raw_questions = []
                
                # Get student's answers from submission
                student_answers = {}
                if submission.answers:
                    try:
                        student_answers = json.loads(submission.answers)
                    except:
                        pass
                
                # Process each question
                for i, q_data in enumerate(raw_questions):
                    question_id = q_data.get('id')
                    
                    # 1. TRY TO GET QUESTION FROM DATABASE (with answer key)
                    correct_answer_from_db = ""
                    question_text = ""
                    question_type = ""
                    
                    if question_id:
                        try:
                            db_question = Question.objects.get(id=question_id)
                            # Get the correct answer from database
                            if db_question.question_type == 'objective':
                                # For MCQ, get correct options
                                correct_options = db_question.correct_options or ""
                                # Convert "1,3" to "A, C"
                                option_map = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'}
                                options_list = [opt.strip() for opt in correct_options.split(',') if opt.strip()]
                                correct_answer_from_db = ", ".join(
                                    option_map.get(opt, opt) for opt in options_list
                                )
                            else:
                                # For other types, get the answer field
                                correct_answer_from_db = db_question.answer or ""
                            
                            question_text = db_question.question
                            question_type = db_question.question_type
                            
                        except Question.DoesNotExist:
                            # If not in database, use data from paper
                            db_question = None
                    
                    # 2. If not in database, use data from paper
                    if not correct_answer_from_db:
                        correct_answer_from_db = q_data.get('correct_answer') or q_data.get('answer') or ""
                    
                    if not question_text:
                        question_text = q_data.get('question') or q_data.get('question_text') or f'Question {i+1}'
                    
                    if not question_type:
                        question_type = q_data.get('type') or q_data.get('question_type') or 'descriptive'
                    
                    # 3. Prepare options for MCQ questions
                    options = []
                    if question_type == 'objective':
                        option_letters = ['A', 'B', 'C', 'D']
                        for j in range(1, 5):
                            option_text = q_data.get(f'option{j}') or ""
                            if option_text:
                                options.append({
                                    'letter': option_letters[j-1],
                                    'text': option_text,
                                    'is_correct': False  # Will be set below
                                })
                        
                        # Mark correct options
                        if correct_answer_from_db:
                            correct_letters = [letter.strip() for letter in correct_answer_from_db.split(',')]
                            for option in options:
                                if option['letter'] in correct_letters:
                                    option['is_correct'] = True
                    
                    # 4. Get student's answer for this question
                    student_answer = student_answers.get(str(question_id or i+1), '')
                    
                    # 5. Get existing evaluation if any
                    existing_eval = existing_question_marks.get(str(question_id or i+1), {})
                    
                    # 6. Create question object with ANSWER KEY
                    question_obj = {
                        'id': question_id or i+1,
                        'number': i+1,
                        'question': question_text,
                        'type': question_type,
                        'marks': q_data.get('marks', 1),
                        'subject': q_data.get('subject_name') or q_data.get('subject') or 'General',
                        
                        # Student's attempt
                        'student_answer': student_answer,
                        
                        # ANSWER KEY (what data entry entered)
                        'correct_answer': correct_answer_from_db,
                        
                        # Options for MCQ
                        'options': options,
                        'has_options': len(options) > 0,
                        
                        # Existing evaluation
                        'evaluated_marks': existing_eval.get('marks', 0),
                        'evaluated_feedback': existing_eval.get('feedback', ''),
                        
                        # For display
                        'is_correct': False,  # Will be calculated
                        'score_color': 'gray',
                    }
                    
                    # Check if student's answer is correct
                    if student_answer and correct_answer_from_db:
                        if question_type == 'objective':
                            # For MCQ, check if student selected correct options
                            student_selected = [s.strip().upper() for s in student_answer.split(',')]
                            correct_options = [c.strip().upper() for c in correct_answer_from_db.split(',')]
                            question_obj['is_correct'] = set(student_selected) == set(correct_options)
                        else:
                            # For descriptive, simple comparison
                            question_obj['is_correct'] = student_answer.strip().lower() == correct_answer_from_db.strip().lower()
                    
                    # Set score color
                    if question_obj['is_correct']:
                        question_obj['score_color'] = 'green'
                    elif student_answer:
                        question_obj['score_color'] = 'yellow'
                    else:
                        question_obj['score_color'] = 'red'
                    
                    questions_with_answers.append(question_obj)
                
            except Exception as e:
                print(f"Error processing questions: {str(e)}")
                questions_with_answers = []
        
        # Handle POST request (teacher submits evaluation)
        if request.method == 'POST':
            try:
                # Collect question-wise marks
                question_marks = {}
                total_obtained = 0
                
                for question in questions_with_answers:
                    q_id = str(question['id'])
                    marks_key = f'marks_{q_id}'
                    feedback_key = f'feedback_{q_id}'
                    
                    marks_obtained = float(request.POST.get(marks_key, 0))
                    feedback = request.POST.get(feedback_key, '')
                    
                    # Validate marks don't exceed maximum
                    max_marks = question['marks']
                    if marks_obtained > max_marks:
                        marks_obtained = max_marks
                    
                    question_marks[q_id] = {
                        'question': question['question'][:100],
                        'marks': marks_obtained,
                        'max_marks': max_marks,
                        'feedback': feedback,
                        'correct_answer': question['correct_answer'],  # Store answer key
                        'student_answer': question['student_answer'],
                    }
                    
                    total_obtained += marks_obtained
                
                # Get other form data
                additional_marks = float(request.POST.get('additional_marks', 0))
                total_marks = float(request.POST.get('total_marks', 100))
                teacher_comments = request.POST.get('teacher_comments', '')
                marking_data = request.POST.get('marking_data', '{}')
                
                # Calculate final marks
                final_obtained = total_obtained + additional_marks
                percentage = (final_obtained / total_marks * 100) if total_marks > 0 else 0
                
                # Determine grade
                grade = request.POST.get('grade', '')
                if not grade:
                    if percentage >= 90: grade = 'A+'
                    elif percentage >= 80: grade = 'A'
                    elif percentage >= 70: grade = 'B+'
                    elif percentage >= 60: grade = 'B'
                    elif percentage >= 50: grade = 'C'
                    elif percentage >= 40: grade = 'D'
                    else: grade = 'F'
                
                # Update submission
                submission.total_marks = total_marks
                submission.obtained_marks = final_obtained
                submission.teacher_comments = teacher_comments
                submission.percentage = percentage
                submission.grade = grade
                submission.question_marks = question_marks
                submission.marking_data = json.loads(marking_data) if marking_data else {}
                submission.status = 'evaluated'
                submission.evaluated_by = request.user
                submission.evaluated_at = timezone.now()
                
                # Handle marked sheet upload
                marked_sheet = request.FILES.get('marked_sheet')
                if marked_sheet:
                    submission.marked_answer_sheet = marked_sheet
                
                submission.save()
                
                # Update ExamResult if exists
                if submission.exam_result:
                    submission.exam_result.obtained_marks = final_obtained
                    submission.exam_result.total_marks = total_marks
                    submission.exam_result.percentage = percentage
                    submission.exam_result.grade = grade
                    submission.exam_result.save()
                
                # Create notification for student
                from .models import StudentNotification
                StudentNotification.objects.create(
                    student=submission.student,
                    submission=submission,
                    message=f"Your exam '{submission.exam_title}' has been evaluated. Score: {final_obtained}/{total_marks} ({percentage:.1f}%)",
                    notification_type='exam_evaluated'
                )
                
                messages.success(request, "✅ Evaluation completed successfully!")
                return redirect('teacher_pending_evaluations')
                
            except Exception as e:
                messages.error(request, f"Error saving evaluation: {str(e)}")
        
        # GET request - show evaluation form
        context = {
            'submission': submission,
            'paper': paper,
            'questions': questions_with_answers,
            'total_questions': len(questions_with_answers),
            'total_marks': submission.total_marks or 100,
            'has_answer_file': submission.answer_file and hasattr(submission.answer_file, 'url'),
            'title': f"Evaluate {submission.student_name}'s Exam"
        }
        
        if context['has_answer_file']:
            try:
                context['answer_file_url'] = submission.answer_file.url
            except:
                context['has_answer_file'] = False
        
        return render(request, 'evaluate_exam.html', context)
        
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('teacher_pending_evaluations')


# views.py
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from io import BytesIO
from django.shortcuts import get_object_or_404

def download_answer_key_pdf(request, submission_id):
    submission = get_object_or_404(StudentExamSubmission, id=submission_id)
    
    # Create PDF buffer
    buffer = BytesIO()
    
    # Create document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Story to hold elements
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        textColor=colors.gray
    )
    
    question_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10,
        leftIndent=20
    )
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20,
        leftIndent=40,
        textColor=colors.green,
        backColor=colors.lightgrey
    )
    
    # Add title
    story.append(Paragraph(f"ANSWER KEY", title_style))
    story.append(Paragraph(f"Exam: {submission.exam_title}", subtitle_style))
    story.append(Paragraph(f"Date: {submission.submitted_at.strftime('%B %d, %Y')}", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Add table with summary
    summary_data = [
        ['Total Questions', len(submission.question_marks)],
        ['Total Marks', submission.total_marks],
        ['Student Score', f"{submission.obtained_marks}/{submission.total_marks}"],
        ['Percentage', f"{submission.percentage}%"],
        ['Grade', submission.grade]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 40))
    
    # Add answer key section title
    story.append(Paragraph("QUESTION-WISE ANSWER KEY", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    # Add questions and answers
    for i, (question_text, data) in enumerate(submission.question_marks.items(), 1):
        # Add question number and text
        story.append(Paragraph(f"<b>Q{i}. {question_text}</b>", question_style))
        
        # Add correct answer
        correct_answer = data.get('correct_answer', 'Not available')
        story.append(Paragraph(f"<b>Correct Answer:</b> {correct_answer}", answer_style))
        
        # Add student's answer if available
        student_answer = data.get('student_answer')
        if student_answer:
            story.append(Paragraph(f"<b>Your Answer:</b> {student_answer}", 
                                  ParagraphStyle(
                                      'StudentAnswer',
                                      parent=styles['Normal'],
                                      fontSize=11,
                                      leftIndent=40,
                                      textColor=colors.blue
                                  )))
        
        # Add marks
        marks = data.get('marks', 0)
        max_marks = data.get('max_marks', 1)
        story.append(Paragraph(f"<b>Marks:</b> {marks}/{max_marks}", 
                              ParagraphStyle(
                                  'MarksStyle',
                                  parent=styles['Normal'],
                                  fontSize=11,
                                  leftIndent=40,
                                  textColor=colors.purple
                              )))
        
        story.append(Spacer(1, 15))
    
    # Add teacher comments if available
    if submission.teacher_comments:
        story.append(Spacer(1, 30))
        story.append(Paragraph("TEACHER'S COMMENTS", styles['Heading2']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(submission.teacher_comments, 
                              ParagraphStyle(
                                  'CommentsStyle',
                                  parent=styles['Normal'],
                                  fontSize=11,
                                  backColor=colors.lightyellow,
                                  borderPadding=10,
                                  leftIndent=10
                              )))
    
    # Add footer
    story.append(Spacer(1, 50))
    story.append(Paragraph(f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M')}", 
                          ParagraphStyle(
                              'Footer',
                              parent=styles['Normal'],
                              fontSize=9,
                              alignment=1,
                              textColor=colors.grey
                          )))
    story.append(Paragraph(f"Evaluated by: {submission.evaluated_by.get_full_name()}", 
                          ParagraphStyle(
                              'Footer',
                              parent=styles['Normal'],
                              fontSize=9,
                              alignment=1,
                              textColor=colors.grey
                          )))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF value
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="answer_key_{submission.exam_title.replace(" ", "_")}.pdf"'
    return response


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@login_required
@csrf_exempt
def mark_notifications_read(request):
    """Mark all notifications as read for the current user"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mark_all = data.get('mark_all', False)
            
            # Import the notification model
            from .models import StudentNotification
            
            if mark_all:
                # Mark all unread notifications as read
                StudentNotification.objects.filter(
                    student=request.user,
                    is_read=False
                ).update(is_read=True)
                
                return JsonResponse({
                    'success': True,
                    'message': 'All notifications marked as read'
                })
            
            return JsonResponse({
                'success': False,
                'error': 'Invalid request'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })


# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def student_notifications(request):
    """Student notifications page"""
    try:
        from .models import StudentNotification
        # Get all notifications for this student
        notifications = StudentNotification.objects.filter(
            student=request.user
        ).order_by('-created_at')
        
        # Mark all as read when viewing the page
        notifications.filter(is_read=False).update(is_read=True)
        
        # Count unread (should be 0 after marking all as read)
        unread_notifications_count = 0
        
    except Exception as e:
        print(f"Error fetching notifications: {e}")
        notifications = []
        unread_notifications_count = 0
    
    context = {
        'data': {'username': request.user.username},
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
    }
    
    return render(request, 'student_notifications.html', context)

@login_required
def student_mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    try:
        from .models import StudentNotification
        notification = get_object_or_404(StudentNotification, id=notification_id, student=request.user)
        notification.is_read = True
        notification.save()
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def student_mark_all_notifications_read(request):
    """Mark all notifications as read"""
    try:
        from .models import StudentNotification
        StudentNotification.objects.filter(
            student=request.user,
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def mark_notifications_read(request):
    # Placeholder for marking notifications as read
    from django.http import JsonResponse
    import json
    
    if request.method == 'POST':
        # Add your logic here to mark notifications as read
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
@user_passes_test(lambda u: u.user_type == 2)  # Only teachers
def teacher_view_submission(request, submission_id):
    """View a submitted exam with answer file"""
    # FIXED: Use correct field names in select_related
    submission = get_object_or_404(
        StudentExamSubmission.objects.select_related(
            'student', 
            'generated_paper', 
            'question_paper', 
            'exam_result',
            'evaluated_by'
        ),
        id=submission_id
    )
    
    # Get the paper using the property method
    paper = submission.paper
    
    context = {
        'submission': submission,
        'paper': paper,  # This uses the @property method
        'student': submission.student,
        'title': f'View Submission - {submission.student_name}'
    }
    
    return render(request, 'view_submission.html', context)

@login_required
@user_passes_test(lambda u: u.user_type == 2)  # Only teachers
def teacher_evaluated_exams(request):
    """List all evaluated exams"""
    evaluated_submissions = StudentExamSubmission.objects.filter(
        status='evaluated'
    ).select_related('student', 'paper', 'evaluated_by').order_by('-evaluated_at')
    
    context = {
        'evaluated_submissions': evaluated_submissions,
        'title': 'Evaluated Exams'
    }
    
    return render(request, 'evaluate_exam.html', context)



@login_required
def download_answer_file(request, submission_id):
    """Download the student's answer file"""
    submission = get_object_or_404(StudentExamSubmission, id=submission_id)
    
    if submission.answer_file and submission.answer_file.storage.exists(submission.answer_file.name):
        response = HttpResponse(submission.answer_file, content_type='application/octet-stream')
        filename = f"{submission.student_name}_{submission.exam_title}{os.path.splitext(submission.answer_file.name)[1]}"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    messages.error(request, "No answer file found.")
    return redirect('teacher_view_submission', submission_id=submission_id)

@login_required
@user_passes_test(lambda u: u.user_type == 2)  # Only teachers
@require_POST
def save_draft_evaluation(request, submission_id):
    """Save evaluation as draft (not final)"""
    submission = get_object_or_404(StudentExamSubmission, id=submission_id)
    
    try:
        data = json.loads(request.body)
        
        # Save draft data to the submission (temporary fields)
        submission.teacher_comments = data.get('teacher_comments', '')
        submission.total_marks = data.get('total_marks', 100)
        submission.obtained_marks = data.get('obtained_marks', 0)
        submission.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Draft saved successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@user_passes_test(lambda u: u.user_type == 2)  # Only teachers
def teacher_evaluate_existing_result(request, result_id):
    """Teacher evaluates an existing ExamResult (for direct ExamResult evaluation)"""
    result = get_object_or_404(ExamResult, id=result_id)
    
    # Determine which paper field to use
    paper = result.paper  # This might be GeneratedQuestionPaper or QuestionPaper
    
    # Create defaults based on paper type
    defaults = {
        'student': result.student,
        'student_name': result.student.get_full_name() or result.student.username,
        'student_email': result.student.email,
        'exam_title': paper.exam_name if paper and hasattr(paper, 'exam_name') else f"Exam {result.id}",
        'status': 'submitted',
        'total_marks': result.total_marks,
        'obtained_marks': result.obtained_marks,
        'percentage': result.percentage,
        'grade': result.grade if hasattr(result, 'grade') else ''
    }
    
    # Set the correct paper field based on type
    if hasattr(result, 'paper') and result.paper:
        # Check if it's a GeneratedQuestionPaper
        from .models import GeneratedQuestionPaper
        if isinstance(result.paper, GeneratedQuestionPaper):
            defaults['generated_paper'] = result.paper
        else:
            defaults['question_paper'] = result.paper
    elif hasattr(result, 'question_paper') and result.question_paper:
        defaults['question_paper'] = result.question_paper
    
    # Get or create submission for teacher comments
    submission, created = StudentExamSubmission.objects.get_or_create(
        exam_result=result,
        defaults=defaults
    )
    
    if request.method == 'POST':
        # Update teacher comments
        submission.teacher_comments = request.POST.get('teacher_comments', '')
        submission.status = 'evaluated'
        submission.evaluated_by = request.user
        submission.evaluated_at = timezone.now()
        submission.save()
        
        messages.success(request, "✅ Evaluation submitted!")
        return redirect('teacher_pending_evaluations')
    
    context = {
        'result': result,
        'submission': submission,
        'student': result.student,
        'paper': paper,  # This is the actual paper object
        'title': f'Evaluate {result.student.username}\'s Exam'
    }
    
    return render(request, 'evaluate_existing.html', context)

@login_required
def create_submission_for_teacher(request, result_id):
    """Create a StudentExamSubmission from existing ExamResult (for students)"""
    if request.method == 'POST':
        exam_result = get_object_or_404(ExamResult, id=result_id, student=request.user)
        
        # Check if already exists
        if not StudentExamSubmission.objects.filter(exam_result=exam_result).exists():
            submission = StudentExamSubmission.objects.create(
                student=request.user,
                paper=exam_result.paper,
                exam_result=exam_result,
                student_name=request.user.get_full_name() or request.user.username,
                student_email=request.user.email,
                exam_title=exam_result.paper.exam_name if exam_result.paper else f"Exam {exam_result.id}",
                total_marks=exam_result.total_marks,
                obtained_marks=exam_result.obtained_marks,
                percentage=exam_result.percentage,
                grade=exam_result.grade,
                status='submitted'
            )
            
            # Create notifications for teachers
            teachers = User.objects.filter(user_type=2)
            for teacher in teachers:
                TeacherNotification.objects.create(
                    teacher=teacher,
                    submission=submission,
                    message=f"New exam submission from {request.user.username} for evaluation"
                )
            
            messages.success(request, "✅ Your exam has been submitted for teacher evaluation!")
        else:
            messages.info(request, "✅ Your exam is already submitted for evaluation.")
        
        return redirect('student_exam_results')
    
    return redirect('student_exam_results')

# views.py - Complete submit_exam view
import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from .models import User 
import os

@login_required
def submit_exam(request):
    """Handle exam submission and save for teacher evaluation"""
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Invalid request method'
        })

    try:
        print("\n" + "="*60)
        print("EXAM SUBMISSION FOR TEACHER EVALUATION")
        print("="*60)

        # Get paper ID
        paper_id = request.POST.get('paper_id')
        if not paper_id:
            return JsonResponse({
                'success': False,
                'error': 'No exam paper found'
            })

        print(f"Paper ID: {paper_id}")

        # Try to get the paper
        paper = None
        try:
            from .models import GeneratedQuestionPaper
            paper = GeneratedQuestionPaper.objects.get(id=paper_id)
            print(f"Found GeneratedQuestionPaper: {paper.exam_name}")
            is_generated_paper = True
        except GeneratedQuestionPaper.DoesNotExist:
            try:
                from .models import QuestionPaper
                paper = QuestionPaper.objects.get(id=paper_id)
                print(f"Found QuestionPaper: {paper.title}")
                is_generated_paper = False
            except QuestionPaper.DoesNotExist:
                print("Paper not found in any model")
                return JsonResponse({
                    'success': False,
                    'error': 'Exam paper not found'
                })

        # Check if already submitted
        from .models import StudentExamSubmission
        existing_submission = StudentExamSubmission.objects.filter(
            student=request.user,
            generated_paper=paper if is_generated_paper else None,
            question_paper=None if is_generated_paper else paper
        ).first()

        if existing_submission:
            print(f"Already submitted: {existing_submission.id}")
            return JsonResponse({
                'success': False,
                'error': 'You have already submitted this exam for evaluation'
            })

        # Get time taken
        time_taken = int(request.POST.get('time_taken', 0))
        print(f"Time taken: {time_taken} seconds")

        # Handle file upload
        answer_file = request.FILES.get('answer_file')
        print(f"Files in request: {list(request.FILES.keys())}")
        print(f"Answer file received: {answer_file}")

        if not answer_file:
            return JsonResponse({
                'success': False,
                'error': 'Please upload your answer sheet'
            })

        # Validate file
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
        file_extension = os.path.splitext(answer_file.name)[1].lower()

        if file_extension not in allowed_extensions:
            return JsonResponse({
                'success': False,
                'error': f'Invalid file type. Please upload {", ".join(allowed_extensions)} files'
            })

        # Validate file size (10MB)
        if answer_file.size > 10 * 1024 * 1024:
            return JsonResponse({
                'success': False,
                'error': 'File size too large. Maximum size is 10MB'
            })

        additional_notes = request.POST.get('additional_notes', '')

        print(f"File details: {answer_file.name}, Size: {answer_file.size}, Type: {file_extension}")

        # Create StudentExamSubmission
        submission = StudentExamSubmission.objects.create(
            student=request.user,
            generated_paper=paper if is_generated_paper else None,
            question_paper=None if is_generated_paper else paper,
            student_name=request.user.get_full_name() or request.user.username,
            student_email=request.user.email,
            exam_title=paper.exam_name if hasattr(paper, 'exam_name') else getattr(paper, 'title', f"Exam Paper {paper.id}"),
            answer_file=answer_file,
            additional_notes=additional_notes,
            time_taken=time_taken,
            status='submitted'
        )

        print(f"Submission created: ID {submission.id}")

        # FIXED: Create ExamResult with correct parameters
        from .models import ExamResult
        exam_result = ExamResult.objects.create(
            student=request.user,
            paper=paper if is_generated_paper else None,
            question_paper=paper if not is_generated_paper else None,
            total_marks=paper.total_marks if hasattr(paper, 'total_marks') else 100,
            obtained_marks=0,
            percentage=0,  # Required field
            grade='Pending',  # Required field
            correct_answers=0,  # Required field
            wrong_answers=0,  # Required field
            unattempted=0,  # Required field
            time_taken=time_taken // 60,  # Convert seconds to minutes
            answers={"note": "Submitted for teacher evaluation"},  # Must be dict for JSONField
            exam_time=timezone.now(),  # Changed from integer to datetime
            status='completed'  # Changed from 'submitted_for_evaluation' to 'completed'
        )

        # Link submission to exam result
        submission.exam_result = exam_result
        submission.save()

        # Create notification for teachers
        from .models import TeacherNotification
        teachers = User.objects.filter(user_type=2)  # Teachers
        for teacher in teachers:
            TeacherNotification.objects.create(
                teacher=teacher,
                submission=submission,
                message=f"New exam submission from {request.user.username} for '{submission.exam_title}'"
            )

        print(f"Created notifications for {teachers.count()} teachers")

        # Clear session data
        session_keys = [
            'current_exam_id', 'exam_start_time', 'exam_questions',
            'exam_answers', 'current_question_index', 'answered_questions'
        ]
        for key in session_keys:
            if key in request.session:
                del request.session[key]

        print(f"✅ Submission saved successfully: {submission.id}")
        print(f"✅ Answer file path: {submission.answer_file.path if submission.answer_file else 'No file'}")

        return JsonResponse({
            'success': True,
            'message': '✅ Exam submitted successfully! Your answers have been sent to teachers for evaluation.',
            'submission_id': submission.id,
            'redirect_url': reverse('student_available_exams')  # ADD THIS LINE
        })

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

        return JsonResponse({
            'success': False,
            'error': f'Error submitting exam: {str(e)}'
        })





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import os

@login_required
@user_passes_test(lambda u: u.user_type == 2)  # Only teachers
@csrf_exempt
def teacher_save_draft_evaluation(request):
    """Save evaluation as draft"""
    if request.method == 'POST':
        try:
            submission_id = request.POST.get('submission_id')
            submission = get_object_or_404(StudentExamSubmission, id=submission_id)
            
            # Save marking data
            marking_data = request.POST.get('marking_data')
            if marking_data:
                submission.marking_data = json.loads(marking_data)
            
            # Save as draft
            submission.evaluation_status = 'draft'
            submission.evaluated_by = request.user
            submission.evaluated_at = timezone.now()
            submission.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Draft saved successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@user_passes_test(lambda u: u.user_type == 2)  # Only teachers
@csrf_exempt
def teacher_save_marked_sheet(request):
    """Save marked answer sheet and finalize evaluation"""
    if request.method == 'POST':
        try:
            submission_id = request.POST.get('submission_id')
            submission = get_object_or_404(StudentExamSubmission, id=submission_id)
            
            # ... [existing code] ...
            
            # Create notification for student - FIXED
            from .models import StudentNotification
            StudentNotification.objects.create(
                student=submission.student,
                submission=submission,  # Changed from related_submission to submission
                message=f"Your exam '{submission.exam_title}' has been evaluated by {request.user.username}. Score: {marks_obtained}/{total_marks}",
                notification_type='evaluation_complete'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Evaluation completed successfully!',
                'download_url': submission.marked_answer_sheet.url if submission.marked_answer_sheet else ''
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@user_passes_test(lambda u: u.user_type == 2)  # Only teachers
def teacher_finalize_evaluation(request, submission_id):
    """Finalize and publish evaluation to student"""
    if request.method == 'POST':
        try:
            submission = get_object_or_404(StudentExamSubmission, id=submission_id)
            
            # Get form data
            total_marks = float(request.POST.get('total_marks', 100))
            obtained_marks = float(request.POST.get('obtained_marks', 0))
            teacher_comments = request.POST.get('teacher_comments', '')
            marking_data = request.POST.get('marking_data', '{}')
            grade = request.POST.get('grade', '')
            
            # Calculate percentage
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Auto-calculate grade if not provided
            if not grade:
                if percentage >= 90:
                    grade = 'A+'
                elif percentage >= 80:
                    grade = 'A'
                elif percentage >= 70:
                    grade = 'B+'
                elif percentage >= 60:
                    grade = 'B'
                elif percentage >= 50:
                    grade = 'C'
                elif percentage >= 40:
                    grade = 'D'
                else:
                    grade = 'F'
            
            # Update submission
            submission.total_marks = total_marks
            submission.obtained_marks = obtained_marks
            submission.teacher_comments = teacher_comments
            submission.percentage = percentage
            submission.grade = grade
            submission.marking_data = json.loads(marking_data) if marking_data else None
            submission.evaluation_status = 'published'  # Published to student
            submission.evaluated_by = request.user
            submission.evaluated_at = timezone.now()
            submission.save()
            
            # Update ExamResult
            if submission.exam_result:
                submission.exam_result.obtained_marks = obtained_marks
                submission.exam_result.total_marks = total_marks
                submission.exam_result.percentage = percentage
                submission.exam_result.grade = grade
                submission.exam_result.save()
            
            # Create student notification - FIXED: Use 'submission' field, not 'related_submission'
            from .models import StudentNotification
            StudentNotification.objects.create(
                student=submission.student,
                submission=submission,  # Changed from related_submission to submission
                message=f"Your exam '{submission.exam_title}' has been evaluated. Score: {obtained_marks}/{total_marks} ({percentage:.1f}%) - Grade: {grade}",
                notification_type='exam_evaluated',
            )
            
            messages.success(request, f"✅ Evaluation published to student! Score: {obtained_marks}/{total_marks}")
            return redirect('teacher_pending_evaluations')
            
        except Exception as e:
            messages.error(request, f"❌ Error publishing evaluation: {str(e)}")
            return redirect('teacher_evaluate_exam', submission_id=submission_id)
    
    return redirect('teacher_pending_evaluations')

# ================================
# STUDENT VIEWS FOR EVALUATED EXAMS
# ================================

@login_required
@user_passes_test(lambda u: u.user_type == 4)  # Only students
def student_evaluated_exams(request):
    """Student view of all evaluated exams"""
    # Get all evaluated submissions for this student
    evaluated_submissions = StudentExamSubmission.objects.filter(
        student=request.user,
        evaluation_status__in=['evaluated', 'published']
    ).select_related('evaluated_by').order_by('-evaluated_at')
    
    context = {
        'evaluated_submissions': evaluated_submissions,
        'title': 'My Evaluated Exams'
    }
    
    return render(request, 'student_evaluated_exams.html', context)

@login_required
def student_view_evaluation(request, submission_id):
    """Student view of a specific evaluated exam"""
    # Get the submission
    submission = get_object_or_404(
        StudentExamSubmission,
        id=submission_id,
        student=request.user,
        status__in=['evaluated', 'published']
    )
    
    # Get the paper
    paper = submission.paper
    
    # ✅ Ensure question_marks is properly handled
    # If it's a string, try to parse it as JSON
    question_marks = submission.question_marks
    
    if isinstance(question_marks, str):
        try:
            question_marks = json.loads(question_marks)
        except:
            question_marks = {}
    elif question_marks is None:
        question_marks = {}
    
    # Calculate total questions
    total_questions = len(question_marks) if isinstance(question_marks, dict) else 0
    
    context = {
        'submission': submission,
        'paper': paper,
        'teacher': submission.evaluated_by,
        'marking_data': submission.marking_data or {},
        'question_marks': question_marks,
        'total_questions': total_questions,
        'title': f'Evaluation - {submission.exam_title}'
    }
    
    return render(request, 'student_view_evaluation.html', context)


@login_required
def download_marked_sheet(request, submission_id):
    """Download the marked answer sheet"""
    submission = get_object_or_404(StudentExamSubmission, id=submission_id)
    
    # Check if student has access to this submission
    if request.user.user_type == 4 and submission.student != request.user:
        messages.error(request, "You don't have permission to access this file.")
        return redirect('student_evaluated_exams')
    
    if submission.marked_answer_sheet and submission.marked_answer_sheet.storage.exists(submission.marked_answer_sheet.name):
        response = HttpResponse(submission.marked_answer_sheet, content_type='application/octet-stream')
        filename = f"marked_{submission.student_name}_{submission.exam_title}{os.path.splitext(submission.marked_answer_sheet.name)[1]}"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    messages.error(request, "Marked answer sheet not found.")
    if request.user.user_type == 4:
        return redirect('student_view_evaluation', submission_id=submission_id)
    else:
        return redirect('teacher_evaluate_exam', submission_id=submission_id)



def debug_exam_submit(request):
    """Debug view to test exam submission"""
    if request.method == 'POST':
        print("\n=== DEBUG: Exam Submit Test ===")
        print(f"POST keys: {list(request.POST.keys())}")
        print(f"Paper ID: {request.POST.get('paper_id')}")
        print("="*40)
        
        # Try to find the paper
        from .models import GeneratedQuestionPaper, QuestionPaper
        
        paper_id = request.POST.get('paper_id')
        if paper_id:
            try:
                paper = GeneratedQuestionPaper.objects.get(id=paper_id)
                print(f"Found GeneratedQuestionPaper: {paper.title}")
            except:
                print("Not a GeneratedQuestionPaper")
                
            try:
                paper = QuestionPaper.objects.get(id=paper_id)
                print(f"Found QuestionPaper: {paper.exam_name}")
            except:
                print("Not a QuestionPaper either")
        
        return HttpResponse("Debug complete - check console")
    
    return render(request, 'debug_form.html')

@login_required
def exam_result_detail(request, result_id):
    """Display detailed exam result"""
    try:
        # Get the result
        result = get_object_or_404(ExamResult, id=result_id, student=request.user)
        
        # Parse answers
        answers_data = {}
        if result.answers:
            try:
                answers_data = json.loads(result.answers)
            except:
                pass
        
        # Get paper name
        paper_name = ""
        if result.paper:
            paper_name = result.paper.title
        elif result.question_paper:
            paper_name = result.question_paper.exam_name
        
        context = {
            'result': result,
            'answers_data': answers_data,
            'paper_name': paper_name,
            'student': request.user
        }
        
        return render(request, 'exam_result_detail.html', context)
        
    except ExamResult.DoesNotExist:
        messages.error(request, "Result not found.")
        return redirect('student_exam_results')

@login_required
def student_exam_results(request):
    """Display all exam results for the student, focusing on evaluated ones"""
    # Get ExamResults (for auto-graded exams)
    exam_results = ExamResult.objects.filter(student=request.user).order_by('-submitted_at')
    
    # Get evaluated submissions (for teacher-evaluated exams)
    evaluated_submissions = StudentExamSubmission.objects.filter(
        student=request.user,
        status='evaluated'
    ).select_related('evaluated_by').order_by('-evaluated_at')
    
    # Get pending submissions
    pending_submissions = StudentExamSubmission.objects.filter(
        student=request.user,
        status='submitted'
    ).order_by('-submitted_at')
    
    context = {
        'exam_results': exam_results,
        'evaluated_submissions': evaluated_submissions,
        'pending_submissions': pending_submissions,
        'total_evaluated': evaluated_submissions.count(),
        'total_pending': pending_submissions.count(),
        'username': request.user.username,
    }
    
    return render(request, 'student_exam_results.html', context)
@login_required
def teacher_question_papers(request):
    """Teacher view to see all their created papers"""
    papers = QuestionPaper.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        "question_papers": papers
    }
    return render(request, "teacher/question_papers_list.html", context)

def get_questions_json(request):
    """API endpoint to get questions for filtering (AJAX)"""
    subject = request.GET.get('subject')
    question_type = request.GET.get('type', 'all')
    
    if subject == 'mathematics':
        queryset = MathematicsQuestion.objects.all()
    elif subject == 'physics':
        queryset = PhysicsQuestion.objects.all()
    elif subject == 'chemistry':
        queryset = ChemistryQuestion.objects.all()
    elif subject == 'biology':
        queryset = BiologyQuestion.objects.all()
    else:
        return JsonResponse({'questions': []})
    
    if question_type != 'all':
        queryset = queryset.filter(question_type=question_type)
    
    questions = []
    for q in queryset:
        questions.append({
            'id': q.id,
            'text': q.question[:100] + "..." if len(q.question) > 100 else q.question,
            'type': q.question_type,
            'chapter': q.chapter,
            'topic': q.topic,
            'marks': getattr(q, 'marks', 4)  # Default to 4 marks if not specified
        })
    
    return JsonResponse({'questions': questions})



from django.http import JsonResponse

def test_paper_access(request, paper_id):
    """API endpoint to test if a paper is accessible"""
    try:
        # Check if paper exists
        from .models import GeneratedQuestionPaper
        
        try:
            paper = GeneratedQuestionPaper.objects.get(id=paper_id)
        except GeneratedQuestionPaper.DoesNotExist:
            return JsonResponse({
                'exists': False,
                'accessible': False,
                'message': 'Paper not found'
            })
        
        # Check if published
        if not paper.is_published:
            return JsonResponse({
                'exists': True,
                'accessible': False,
                'message': 'Paper is not published yet'
            })
        
        # Check if student has already taken it
        if ExamResult.objects.filter(student=request.user, paper=paper).exists():
            return JsonResponse({
                'exists': True,
                'accessible': False,
                'message': 'You have already taken this exam'
            })
        
        # Check if paper has questions
        has_questions = False
        if paper.question_data:
            if isinstance(paper.question_data, list) and len(paper.question_data) > 0:
                has_questions = True
            elif isinstance(paper.question_data, dict):
                questions = paper.question_data.get('selected_questions', [])
                if isinstance(questions, list) and len(questions) > 0:
                    has_questions = True
        
        if not has_questions:
            return JsonResponse({
                'exists': True,
                'accessible': False,
                'message': 'This exam has no questions'
            })
        
        return JsonResponse({
            'exists': True,
            'accessible': True,
            'message': 'Paper is accessible',
            'title': paper.exam_name or f'Paper {paper.id}',
            'published': paper.is_published,
            'has_questions': has_questions
        })
        
    except Exception as e:
        return JsonResponse({
            'exists': False,
            'accessible': False,
            'message': f'Error: {str(e)}'
        }, status=500)



def exam_result(request, result_id):
    result = get_object_or_404(ExamResult, id=result_id)

    # Parse answers stored in plain text to a dictionary (e.g., "Q12: answer" -> {12: answer})
    parsed_answers = {}
    if result.answers:
        lines = result.answers.splitlines()
        for line in lines:
            if ':' in line:
                qid, ans = line.split(':', 1)
                parsed_answers[qid.strip()] = ans.strip()

    context = {
        "result": result,
        "parsed_answers": parsed_answers
    }
    return render(request, "exam_result.html", context)

def search_staff(request):
    query = request.GET.get('q')
    staff_results = None
    if query:
        staff_results = Staff.objects.filter(first_name__icontains=query) | Staff.objects.filter(last_name__icontains=query)

    staff_list = Staff.objects.all()
    return render(request, 'search_staff.html', {
        'query': query,
        'staff_results': staff_results,
        'staff_list': staff_list
    })


def view_purchases(request):
    purchases = Payment.objects.all()
    return render(request, 'package_list.html', {'purchases': purchases})

def remove_purchase(request, purchase_id):
    purchase = get_object_or_404(Payment, id=purchase_id)
    purchase.delete()
    return redirect('view_purchases')


# views.py
from django.http import JsonResponse
from .models import Question
from django.shortcuts import render


def question_filter_page(request):
    return render(request, "admin_view_questions.html")


def get_chapters(request):
    subject = request.GET.get("subject")

    chapters = (
        Question.objects.filter(subject=subject)
        .values_list("chapter", flat=True)
        .distinct()
    )

    return JsonResponse({"chapters": list(chapters)})


def get_topics(request):
    subject = request.GET.get("subject")
    chapter = request.GET.get("chapter")

    topics = (
        Question.objects.filter(subject=subject, chapter=chapter)
        .values_list("topic", flat=True)
        .distinct()
    )

    return JsonResponse({"topics": list(topics)})


def get_subtopics(request):
    subject = request.GET.get("subject")
    chapter = request.GET.get("chapter")
    topic = request.GET.get("topic")

    subtopics = (
        Question.objects.filter(subject=subject, chapter=chapter, topic=topic)
        .values_list("sub_topic", flat=True)
        .distinct()
    )

    return JsonResponse({"subtopics": list(subtopics)})


def get_questions(request):
    subject = request.GET.get("subject")
    chapter = request.GET.get("chapter")
    topic = request.GET.get("topic")
    subtopic = request.GET.get("subtopic")

    questions = Question.objects.filter(
        subject=subject,
        chapter=chapter,
        topic=topic,
        sub_topic=subtopic
    ).values()

    return JsonResponse({"questions": list(questions)})



@login_required
def teacher_generated_papers(request):
    """List all question papers generated by teacher for editing"""
    # Get all papers created by this teacher
    generated_papers = GeneratedQuestionPaper.objects.filter(
        created_by=request.user
    ).order_by('-created_at')
    
    context = {
        'generated_papers': generated_papers,
        'title': 'My Generated Papers'
    }
    
    return render(request, 'teacher_generated_papers.html', context)

@login_required
def edit_generated_paper(request, paper_id):
    """Edit an existing generated paper"""
    try:
        paper = GeneratedQuestionPaper.objects.get(id=paper_id)
        
        # Check if user can edit
        if not paper.can_edit(request.user):
            messages.error(request, "You don't have permission to edit this paper.")
            return redirect('teacher_generated_papers')
        
        # If paper is published, create a copy for editing
        if paper.is_published:
            paper = paper.create_copy(request.user)
            messages.info(request, "A copy has been created for editing since the original was published.")
            return redirect('edit_generated_paper', paper_id=paper.id)
        
        # Load the paper data into the form
        if request.method == 'GET':
            # Get all data for the template
            subjects = Subject.objects.all().select_related('class_name')
            courses = Course.objects.all()
            school_classes = SchoolClass.objects.all()
            chapters = Chapter.objects.all()
            
            # Get all questions
            all_questions = Question.objects.all().select_related('subject', 'subject__class_name')
            
            # Prepare context with paper data
            context = {
                'paper': paper,
                'subjects': subjects,
                'courses': courses,
                'classes': school_classes,
                'chapters': chapters,
                'all_questions': all_questions[:50],
                'edit_mode': True,
                'paper_data': {
                    'school_name': paper.school_name,
                    'school_address': paper.school_address,
                    'school_contact': paper.school_contact,
                    'affiliation_no': paper.affiliation_number,
                    'exam_name': paper.exam_name,
                    'class_filter': paper.class_name,
                    'course_filter': paper.course_name,
                    'total_marks': paper.total_marks,
                    'time_duration': paper.time_duration,
                    'exam_date': paper.exam_date.strftime('%Y-%m-%d') if paper.exam_date else '',
                    'instructions': paper.instructions,
                    'logo_position': paper.logo_position,
                    'question_data': paper.question_data,
                    'additional_elements': paper.additional_elements or [],
                    'logo_image': paper.logo_image.url if paper.logo_image else None
                }
            }
            
            return render(request, 'Question_creation.html', context)
        
        # Handle POST request (save edits)
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                
                # Update paper data
                paper.school_name = data.get('school_name', paper.school_name)
                paper.school_address = data.get('school_address', paper.school_address)
                paper.school_contact = data.get('school_contact', paper.school_contact)
                paper.affiliation_number = data.get('affiliation_number', paper.affiliation_number)
                paper.exam_name = data.get('exam_name', paper.exam_name)
                paper.class_name = data.get('class_name', paper.class_name)
                paper.course_name = data.get('course_name', paper.course_name)
                paper.total_marks = data.get('total_marks', paper.total_marks)
                paper.time_duration = data.get('time_duration', paper.time_duration)
                paper.instructions = data.get('instructions', paper.instructions)
                paper.logo_position = data.get('logo_position', paper.logo_position)
                
                # Update question data
                if 'selected_questions' in data:
                    paper.question_data = data
                    paper.total_questions = len(data.get('selected_questions', []))
                
                # Update additional elements
                if 'additional_elements' in data:
                    paper.additional_elements = data['additional_elements']
                
                # Update edit tracking
                paper.edit_count += 1
                paper.last_edited_by = request.user
                paper.last_edited_at = timezone.now()
                
                paper.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Paper updated successfully!',
                    'paper_id': paper.id
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
                
    except GeneratedQuestionPaper.DoesNotExist:
        messages.error(request, "Paper not found.")
        return redirect('teacher_generated_papers')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('teacher_generated_papers')

@login_required
def regenerate_paper_copy(request, paper_id):
    """Create a copy of a paper for regeneration"""
    try:
        original_paper = GeneratedQuestionPaper.objects.get(id=paper_id)
        
        # Create a copy
        new_paper = original_paper.create_copy(request.user)
        
        messages.success(request, f"Copy created successfully! You can now edit the new paper.")
        return redirect('edit_generated_paper', paper_id=new_paper.id)
        
    except GeneratedQuestionPaper.DoesNotExist:
        messages.error(request, "Paper not found.")
        return redirect('teacher_generated_papers')

@login_required
def preview_generated_paper(request, paper_id):
    """Preview a generated paper"""
    try:
        paper = GeneratedQuestionPaper.objects.get(id=paper_id)
        
        # Check if user can view
        if paper.created_by != request.user and not request.user.is_staff:
            messages.error(request, "You don't have permission to view this paper.")
            return redirect('teacher_generated_papers')
        
        context = {
            'paper': paper,
            'title': f'Preview - {paper.exam_name}'
        }
        
        return render(request, 'preview_generated_paper.html', context)
        
    except GeneratedQuestionPaper.DoesNotExist:
        messages.error(request, "Paper not found.")
        return redirect('teacher_generated_papers')

@login_required
def delete_generated_paper(request, paper_id):
    """Delete a generated paper (only if not published)"""
    if request.method == 'POST':
        try:
            paper = GeneratedQuestionPaper.objects.get(id=paper_id)
            
            # Only allow deletion of drafts or papers created by user
            if (paper.created_by == request.user or request.user.is_staff) and not paper.is_published:
                paper_title = paper.exam_name
                paper.delete()
                messages.success(request, f"Paper '{paper_title}' deleted successfully!")
            else:
                messages.error(request, "Cannot delete published papers or papers you don't own.")
                
        except GeneratedQuestionPaper.DoesNotExist:
            messages.error(request, "Paper not found.")
    
    return redirect('teacher_generated_papers')

# In views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import GeneratedQuestionPaper
from django.utils import timezone

@login_required
def check_new_papers_api(request):
    """API endpoint to check for new papers"""
    try:
        # Get count of all papers
        total_count = GeneratedQuestionPaper.objects.filter(
            created_by=request.user
        ).count()
        
        # Get papers created in the last 30 seconds
        thirty_seconds_ago = timezone.now() - timezone.timedelta(seconds=30)
        new_papers = GeneratedQuestionPaper.objects.filter(
            created_by=request.user,
            created_at__gte=thirty_seconds_ago
        ).values('id', 'exam_name', 'created_at')[:5]
        
        return JsonResponse({
            'success': True,
            'count': total_count,
            'new_papers': list(new_papers),
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.contrib import messages

@login_required
def edit_generated_paper_only_questions(request, paper_id):
    """Simple page for editing ONLY questions in a paper - no filters"""
    try:
        # Get the paper
        paper = get_object_or_404(GeneratedQuestionPaper, id=paper_id)
        
        # Check permission
        if paper.created_by != request.user and not request.user.is_staff:
            messages.error(request, "You don't have permission to edit this paper.")
            return redirect('teacher_generated_papers')
        
        # Extract existing questions from paper
        existing_questions = []
        if paper.question_data:
            try:
                if isinstance(paper.question_data, dict):
                    questions_data = paper.question_data.get('selected_questions', [])
                elif isinstance(paper.question_data, list):
                    questions_data = paper.question_data
                else:
                    questions_data = []
                
                if isinstance(questions_data, list):
                    existing_questions = questions_data
            except:
                existing_questions = []
        
        # Get questions from database for the subjects in the paper
        subjects_included = paper.subjects_included or []
        related_questions = []
        
        if subjects_included:
            # Map subject names to database subjects
            for subject_name in subjects_included[:3]:  # Limit to 3 subjects
                try:
                    subject_obj = Subject.objects.filter(name__icontains=subject_name).first()
                    if subject_obj:
                        questions = Question.objects.filter(
                            subject=subject_obj
                        ).select_related('subject')[:20]  # Limit to 20 per subject
                        for q in questions:
                            related_questions.append({
                                'id': q.id,
                                'question': q.question[:100] + '...' if len(q.question) > 100 else q.question,
                                'subject': q.subject.name,
                                'marks': q.marks,
                                'type': q.question_type,
                                'chapter': q.chapter or '',
                                'topic': q.topic or ''
                            })
                except:
                    pass
        
        context = {
            'paper': paper,
            'edit_mode': True,
            'edit_only_questions': True,
            'existing_questions': existing_questions,
            'existing_questions_json': json.dumps(existing_questions) if existing_questions else '[]',
            'related_questions': related_questions[:30],  # Limit to 30 related questions
            'paper_title': paper.exam_name or f"Paper #{paper.id}",
        }
        
        return render(request, 'edit_questions_simple.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading paper: {str(e)}")
        return redirect('teacher_generated_papers')

@login_required
@csrf_exempt
def update_paper_questions_only(request):
    """API endpoint to update only questions in a paper"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            paper_id = data.get('paper_id')
            
            if not paper_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Paper ID required'
                })
            
            # Get the paper
            paper = get_object_or_404(GeneratedQuestionPaper, id=paper_id)
            
            # Check permission
            if paper.created_by != request.user and not request.user.is_staff:
                return JsonResponse({
                    'success': False,
                    'error': 'Permission denied'
                })
            
            # Update only questions
            selected_questions = data.get('selected_questions', [])
            
            # Prepare question data
            question_data = {
                'selected_questions': selected_questions,
                'total_marks': sum(q.get('marks', 1) for q in selected_questions),
                'subjects_included': list(set(q.get('subject_name', 'General') for q in selected_questions))
            }
            
            # Update paper
            paper.question_data = question_data
            paper.total_questions = len(selected_questions)
            paper.total_marks = question_data['total_marks']
            paper.subjects_included = question_data['subjects_included']
            paper.edit_count += 1
            paper.last_edited_by = request.user
            paper.last_edited_at = timezone.now()
            paper.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Questions updated successfully',
                'paper_id': paper.id,
                'total_questions': paper.total_questions,
                'total_marks': paper.total_marks
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def update_question_paper(request):
    """Update an existing generated question paper"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            paper_id = data.get('paper_id')
            
            if not paper_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Paper ID is required for update'
                })
            
            # Get the paper
            paper = get_object_or_404(GeneratedQuestionPaper, id=paper_id, created_by=request.user)
            
            # Update paper fields
            paper.title = data.get('title', paper.title)
            paper.description = data.get('description', paper.description)
            paper.school_name = data.get('school_name', paper.school_name)
            paper.school_address = data.get('school_address', paper.school_address)
            paper.school_contact = data.get('school_contact', paper.school_contact)
            paper.affiliation_number = data.get('affiliation_number', paper.affiliation_number)
            paper.exam_name = data.get('exam_name', paper.exam_name)
            paper.class_name = data.get('class_name', paper.class_name)
            paper.course_name = data.get('course_name', paper.course_name)
            paper.total_marks = data.get('total_marks', paper.total_marks)
            paper.time_duration = data.get('time_duration', paper.time_duration)
            paper.exam_date = data.get('exam_date')
            paper.instructions = data.get('instructions', paper.instructions)
            paper.logo_position = data.get('logo_position', paper.logo_position)
            
            # Update content
            paper.question_data = data.get('selected_questions', [])
            paper.additional_elements = data.get('additional_elements', [])
            
            # Update publishing flags if changed
            if 'is_published' in data:
                paper.is_published = data['is_published']
                paper.status = 'published' if data['is_published'] else 'draft'
            
            # Update statistics
            paper.total_questions = len(data.get('selected_questions', []))
            paper.subjects_included = data.get('subjects_included', [])
            
            # Update edit tracking
            paper.edit_count += 1
            paper.last_edited_by = request.user
            paper.last_edited_at = timezone.now()
            
            paper.save()
            
            return JsonResponse({
                'success': True,
                'paper_id': paper.id,
                'title': paper.title,
                'is_published': paper.is_published,
                'message': 'Paper updated successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def get_question_details(request, question_id):
    """Get details of a specific question for editing"""
    try:
        question = get_object_or_404(Question, id=question_id)
        
        return JsonResponse({
            'success': True,
            'question': {
                'id': question.id,
                'question': question.question,
                'subject': question.subject.name if question.subject else '',
                'marks': question.marks,
                'type': question.question_type,
                'chapter': question.chapter or '',
                'topic': question.topic or '',
                'option1': question.option1 or '',
                'option2': question.option2 or '',
                'option3': question.option3 or '',
                'option4': question.option4 or '',
                'correct_options': question.correct_options or '',
                'answer': question.answer or '',
                'difficulty': question.difficulty or 'medium'
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import (
    User, GeneratedQuestionPaper, AutoExamPaper, 
    AutoExamSelection, AutoExamTemplate, QuestionUsageLog,
    Question, Subject, SchoolClass, Staff
)
import random
from datetime import timedelta
import json

@login_required
def auto_create_exam(request):
    """Display the auto exam creation form"""
    # Check if user is staff/mainstaff
    if request.user.user_type not in [2, 5]:  # Staff or MainStaff
        messages.error(request, 'Access denied. Only teachers can create exams.')
        return redirect('teacher_dashboard')
    
    # Get subjects for dropdown
    subjects = Subject.objects.all()
    
    # Get classes for dropdown
    classes = SchoolClass.objects.all()
    
    # Load template data from session if exists
    template_data = request.session.pop('template_data', {})
    
    context = {
        'subjects': subjects,
        'classes': classes,
        'template_data': template_data,
        'step': 1
    }
    return render(request, 'auto_create_exam.html', context)

@login_required
def generate_auto_exam(request):
    """Generate exam paper based on manually selected questions"""
    if request.method != 'POST':
        return redirect('auto_create_exam')
    
    # Check if user is staff/mainstaff
    if request.user.user_type not in [2, 5]:
        messages.error(request, 'Access denied. Only teachers can create exams.')
        return redirect('teacher_dashboard')
    
    # Get form data
    exam_title = request.POST.get('exam_title')
    class_id = request.POST.get('class_name')
    subject_id = request.POST.get('subject')
    duration = int(request.POST.get('duration', 60))
    
    # Get selected questions
    selected_questions_json = request.POST.getlist('selected_questions')
    
    if not selected_questions_json:
        messages.error(request, 'No questions selected. Please select at least one question.')
        return redirect('auto_create_exam')
    
    # Parse selected questions
    selected_questions = []
    total_marks = 0
    
    for q_json in selected_questions_json:
        try:
            q_data = json.loads(q_json)
            selected_questions.append(q_data)
            total_marks += float(q_data.get('marks', 0))
        except:
            continue
    
    if not selected_questions:
        messages.error(request, 'Invalid question data.')
        return redirect('auto_create_exam')
    
    # Get subject object
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        messages.error(request, 'Selected subject not found.')
        return redirect('auto_create_exam')
    
    # Create AutoExamPaper instance
    auto_exam = AutoExamPaper.objects.create(
        teacher=request.user,
        subject=subject.name,
        total_marks=total_marks,
        duration=duration,
        total_questions=len(selected_questions),
        status='DRAFT'
    )
    
    # Create GeneratedQuestionPaper
    generated_paper = GeneratedQuestionPaper.objects.create(
        title=exam_title,
        exam_name=exam_title,
        total_marks=int(total_marks),
        time_duration=f"{duration} minutes",
        exam_time=duration,
        created_by=request.user,
        status='draft',
        is_published=False,
        total_questions=len(selected_questions),
        subjects_included=[subject.name],
        question_data={
            'subject': subject.name,
            'subject_id': subject_id,
            'class_id': class_id,
            'total_marks': total_marks,
            'duration': duration,
            'questions': selected_questions
        }
    )
    
    # Link auto_exam to generated_paper
    auto_exam.generated_paper = generated_paper
    auto_exam.save()
    
    # Save question selections and create usage logs
    question_number = 1
    content_type = ContentType.objects.get_for_model(Question)
    
    for q_data in selected_questions:
        try:
            question = Question.objects.get(id=q_data['id'])
            
            # Create AutoExamSelection
            AutoExamSelection.objects.create(
                auto_exam=auto_exam,
                content_type=content_type,
                object_id=question.id,
                question_number=question_number,
                section=q_data.get('question_type', 'Unknown'),
                marks=float(q_data.get('marks', 0)),
                difficulty=q_data.get('difficulty', 'MEDIUM')
            )
            
            # Create QuestionUsageLog (this tracks usage instead of usage_count field)
            QuestionUsageLog.objects.create(
                content_type=content_type,
                object_id=question.id,
                auto_exam=auto_exam,
                used_by=request.user
            )
            
            # REMOVED: question.usage_count += 1
            # REMOVED: question.last_used = timezone.now()
            # REMOVED: question.save()
            
            question_number += 1
        except Question.DoesNotExist:
            continue
    
    messages.success(request, f'Exam paper generated successfully with {len(selected_questions)} questions!')
    return redirect('review_auto_exam', exam_id=auto_exam.id)


def check_available_questions(subject, mcq_needed, short_needed, long_needed, vlong_needed,
                             topics_list, exclude_topics_list, avoid_recent):
    """Check if enough questions are available before generating"""
    
    def get_count(question_type):
        query = Q(subject=subject)
        
        # Filter by question type
        query &= Q(question_type__iexact=question_type)
        
        # Filter by topics/chapters
        if topics_list:
            topic_query = Q()
            for topic in topics_list:
                topic_query |= Q(topic__icontains=topic) | Q(chapter__icontains=topic)
            query &= topic_query
        
        # Exclude topics
        if exclude_topics_list:
            for topic in exclude_topics_list:
                query &= ~(Q(topic__icontains=topic) | Q(chapter__icontains=topic))
        
        # Avoid recently used
        if avoid_recent:
            thirty_days_ago = timezone.now() - timedelta(days=30)
            content_type = ContentType.objects.get_for_model(Question)
            recent_usage = QuestionUsageLog.objects.filter(
                content_type=content_type,
                used_at__gte=thirty_days_ago
            ).values_list('object_id', flat=True)
            
            if recent_usage:
                query &= ~Q(id__in=list(recent_usage))
        
        return Question.objects.filter(query).count()
    
    mcq_available = get_count('MCQ') if mcq_needed > 0 else mcq_needed
    short_available = get_count('SHORT') if short_needed > 0 else short_needed
    long_available = get_count('LONG') if long_needed > 0 else long_needed
    vlong_available = get_count('VLONG') if vlong_needed > 0 else vlong_needed
    
    has_enough = (
        mcq_available >= mcq_needed and
        short_available >= short_needed and
        long_available >= long_needed and
        vlong_available >= vlong_needed
    )
    
    return {
        'has_enough': has_enough,
        'mcq_available': mcq_available,
        'short_available': short_available,
        'long_available': long_available,
        'vlong_available': vlong_available
    }


def select_questions_for_exam(subject, question_type, required_count, marks_per_question,
                             topics_list, exclude_topics_list, difficulty_dist, avoid_recent=False):
    """Select appropriate questions from Question model"""
    
    # Build query
    query = Q(subject=subject, question_type__iexact=question_type, marks=marks_per_question)
    
    # Filter by topics/chapters
    if topics_list:
        topic_query = Q()
        for topic in topics_list:
            topic_query |= Q(topic__icontains=topic) | Q(chapter__icontains=topic)
        query &= topic_query
    
    # Exclude topics
    if exclude_topics_list:
        for topic in exclude_topics_list:
            query &= ~(Q(topic__icontains=topic) | Q(chapter__icontains=topic))
    
    # Avoid recently used questions
    if avoid_recent:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        content_type = ContentType.objects.get_for_model(Question)
        recent_usage = QuestionUsageLog.objects.filter(
            content_type=content_type,
            used_at__gte=thirty_days_ago
        ).values_list('object_id', flat=True)
        
        if recent_usage:
            query &= ~Q(id__in=list(recent_usage))
    
    # Get available questions
    available_questions = Question.objects.filter(query)
    
    if available_questions.count() < required_count:
        # Try without marks filter
        query = Q(subject=subject, question_type__iexact=question_type)
        if topics_list:
            topic_query = Q()
            for topic in topics_list:
                topic_query |= Q(topic__icontains=topic) | Q(chapter__icontains=topic)
            query &= topic_query
        
        if exclude_topics_list:
            for topic in exclude_topics_list:
                query &= ~(Q(topic__icontains=topic) | Q(chapter__icontains=topic))
        
        available_questions = Question.objects.filter(query)
    
    if available_questions.count() == 0:
        return []
    
    # Calculate difficulty distribution
    if difficulty_dist == 'easy_focused':
        dist = {'easy': 0.5, 'medium': 0.3, 'hard': 0.2}
    elif difficulty_dist == 'hard_focused':
        dist = {'easy': 0.2, 'medium': 0.3, 'hard': 0.5}
    else:  # balanced
        dist = {'easy': 0.3, 'medium': 0.4, 'hard': 0.3}
    
    selected_questions = []
    
    for difficulty, percentage in dist.items():
        count_needed = int(required_count * percentage)
        if count_needed > 0:
            difficulty_questions = available_questions.filter(difficulty__iexact=difficulty)
            
            if difficulty_questions.count() < count_needed:
                count_needed = difficulty_questions.count()
            
            if count_needed > 0:
                selected = list(difficulty_questions.order_by('?')[:count_needed])
                selected_questions.extend(selected)
    
    # Fill remaining with any difficulty
    if len(selected_questions) < required_count:
        remaining = required_count - len(selected_questions)
        existing_ids = [q.id for q in selected_questions]
        additional = available_questions.exclude(id__in=existing_ids).order_by('?')[:remaining]
        selected_questions.extend(list(additional))
    
    return selected_questions[:required_count]


@login_required
def get_chapters_by_subject(request):
    """AJAX view to get chapters for a subject from Question model"""
    subject_id = request.GET.get('subject_id')
    
    if not subject_id:
        return JsonResponse({'chapters': []})
    
    try:
        subject = Subject.objects.get(id=subject_id)
        
        # Get unique chapters from Question model for this subject
        chapters = Question.objects.filter(
            subject=subject,
            chapter__isnull=False
        ).exclude(chapter='').values_list('chapter', flat=True).distinct().order_by('chapter')[:50]
        
        chapter_list = [{'id': ch, 'name': ch} for ch in chapters]
        
        return JsonResponse({'chapters': chapter_list})
    
    except Exception as e:
        return JsonResponse({'chapters': [], 'error': str(e)})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q
from .models import Subject, Chapter, Question, SchoolClass
import json

@login_required
def auto_create_exam(request):
    """Display the auto exam creation form"""
    classes = SchoolClass.objects.all()
    context = {
        'classes': classes,
    }
    return render(request, 'auto_create_exam.html', context)

@login_required
@require_GET
def get_subjects_by_class(request):
    """Get subjects for a specific class"""
    class_id = request.GET.get('class_id')
    if not class_id:
        return JsonResponse({'error': 'Class ID required'}, status=400)
    
    try:
        subjects = Subject.objects.filter(class_name_id=class_id).values('id', 'name')
        return JsonResponse({'subjects': list(subjects)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_GET
def get_chapters_by_subjects(request):
    """Get chapters for multiple subjects"""
    subject_ids = request.GET.get('subject_ids', '')
    if not subject_ids:
        return JsonResponse({'error': 'Subject IDs required'}, status=400)
    
    try:
        subject_id_list = subject_ids.split(',')
        chapters = Chapter.objects.filter(
            subject_id__in=subject_id_list
        ).select_related('subject').values(
            'id', 'name', 'subject__name'
        )
        
        chapters_list = [{
            'id': ch['id'],
            'name': ch['name'],
            'subject_name': ch['subject__name']
        } for ch in chapters]
        
        return JsonResponse({'chapters': chapters_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_GET
def get_questions_by_chapters(request):
    """Get questions from selected chapters - FIXED: Match by subject"""
    chapter_ids = request.GET.get('chapter_ids', '')
    if not chapter_ids:
        return JsonResponse({'error': 'Chapter IDs required'}, status=400)
    
    try:
        chapter_id_list = chapter_ids.split(',')
        
        # Get the subjects from selected chapters
        chapters = Chapter.objects.filter(id__in=chapter_id_list).select_related('subject').values(
            'id', 'name', 'subject__id', 'subject__name'
        )
        
        # Get subject IDs
        subject_ids = []
        for ch in chapters:
            if ch['subject__id']:
                subject_ids.append(ch['subject__id'])
        
        print(f"Selected chapters: {[ch['name'] for ch in chapters]}")
        print(f"Subject IDs to filter by: {subject_ids}")
        
        # If no subject IDs, return empty
        if not subject_ids:
            return JsonResponse({'questions': []})
        
        # Get questions that belong to these subjects
        questions = Question.objects.filter(
            subject_id__in=subject_ids
        ).select_related('subject').values(
            'id', 'question', 'marks', 'subject__name', 'chapter', 'topic', 'question_type', 'difficulty'
        )
        
        print(f"Found {questions.count()} total questions for these subjects")
        
        questions_list = []
        for q in questions:
            questions_list.append({
                'id': q['id'],
                'question': q['question'][:100] + '...' if q['question'] and len(q['question']) > 100 else (q['question'] or ''),
                'full_question': q['question'] or '',
                'marks': q['marks'] or 0,
                'difficulty': q['difficulty'] or 'medium',
                'subject': q['subject__name'] or 'Unknown',
                'chapter': q['chapter'] or '',
                'topic': q['topic'] or '',
                'question_type': q['question_type'] or 'descriptive'
            })
        
        return JsonResponse({'questions': questions_list})
    except Exception as e:
        print(f"Error in get_questions_by_chapters: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def generate_questions_from_bank(request):
    """Generate questions based on distribution"""
    try:
        data = json.loads(request.body)
        chapter_ids = data.get('chapter_ids', [])
        distribution = data.get('distribution', {})
        
        print(f"Chapter IDs received: {chapter_ids}")
        print(f"Distribution received: {distribution}")
        
        # Get subjects from selected chapters
        chapters = Chapter.objects.filter(id__in=chapter_ids).select_related('subject').values(
            'id', 'name', 'subject__id', 'subject__name'
        )
        
        # Get subject IDs
        subject_ids = []
        for ch in chapters:
            if ch['subject__id']:
                subject_ids.append(ch['subject__id'])
        
        print(f"Subject IDs: {subject_ids}")
        
        # If no subject IDs, return empty
        if not subject_ids:
            return JsonResponse({'questions': []})
        
        selected_questions = []
        
        # For each mark type, select the required number of questions
        for marks, count_needed in distribution.items():
            marks = int(marks)
            count_needed = int(count_needed)
            
            if count_needed > 0:
                print(f"Looking for {count_needed} questions of {marks} marks")
                
                # Get questions of this mark from these subjects
                questions = Question.objects.filter(
                    subject_id__in=subject_ids,
                    marks=marks
                ).select_related('subject').values(
                    'id', 'question', 'marks', 'subject__name', 'chapter', 'topic', 'question_type', 'difficulty'
                )
                
                print(f"Found {questions.count()} questions of {marks} marks")
                
                # Convert to list and shuffle
                import random
                questions_list = list(questions)
                random.shuffle(questions_list)
                
                # Take required number of questions
                selected = questions_list[:count_needed]
                print(f"Selected {len(selected)} questions of {marks} marks")
                
                for q in selected:
                    selected_questions.append({
                        'id': q['id'],
                        'question': q['question'][:100] + '...' if q['question'] and len(q['question']) > 100 else (q['question'] or ''),
                        'full_question': q['question'] or '',
                        'marks': q['marks'] or 0,
                        'difficulty': q['difficulty'] or 'medium',
                        'subject': q['subject__name'] or 'Unknown',
                        'chapter': q['chapter'] or '',
                        'topic': q['topic'] or '',
                        'question_type': q['question_type'] or 'descriptive'
                    })
        
        # Shuffle all selected questions together
        random.shuffle(selected_questions)
        
        print(f"Total selected questions: {len(selected_questions)}")
        
        return JsonResponse({'questions': selected_questions})
    except Exception as e:
        print(f"Error in generate_questions: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def debug_question_data(request):
    """Debug view to see what's in your question table"""
    try:
        response = {
            'total_questions': Question.objects.count(),
            'questions_by_marks': {},
            'subjects_in_questions': [],
            'chapters_in_questions': [],
            'sample_questions': []
        }
        
        # Count by marks
        for marks in range(1, 11):
            count = Question.objects.filter(marks=marks).count()
            response['questions_by_marks'][str(marks)] = count
        
        # Get all subjects in questions
        subjects = Question.objects.exclude(subject__isnull=True).values(
            'subject', 'subject__name'
        ).distinct()[:20]
        response['subjects_in_questions'] = list(subjects)
        
        # Get chapters in questions
        chapters = Question.objects.exclude(chapter__isnull=True).exclude(chapter='').values_list('chapter', flat=True).distinct()[:20]
        response['chapters_in_questions'] = list(chapters)
        
        # Get sample questions
        sample = Question.objects.select_related('subject').values('id', 'subject__name', 'marks', 'chapter', 'question')[:10]
        response['sample_questions'] = list(sample)
        
        # If chapter_ids provided, show filtered
        chapter_ids = request.GET.get('chapter_ids', '')
        if chapter_ids:
            chapter_id_list = chapter_ids.split(',')
            chapters = Chapter.objects.filter(id__in=chapter_id_list).select_related('subject')
            
            subject_ids = []
            for ch in chapters:
                if ch.subject_id:
                    subject_ids.append(ch.subject_id)
            
            filtered = Question.objects.filter(subject_id__in=subject_ids) if subject_ids else Question.objects.none()
            response['filtered_count'] = filtered.count()
            response['filtered_by_mark'] = {}
            
            for marks in range(1, 11):
                count = filtered.filter(marks=marks).count()
                response['filtered_by_mark'][str(marks)] = count
        
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def generate_auto_exam(request):
    """Generate exam paper based on selected questions"""
    if request.method != 'POST':
        return redirect('auto_create_exam')
    
    # Get form data
    exam_title = request.POST.get('exam_title')
    class_id = request.POST.get('class_name')
    duration = int(request.POST.get('duration', 60))
    
    # Get selected questions
    selected_questions_json = request.POST.getlist('selected_questions')
    
    if not selected_questions_json:
        messages.error(request, 'No questions selected.')
        return redirect('auto_create_exam')
    
    # Parse selected questions
    selected_questions = []
    total_marks = 0
    
    for q_json in selected_questions_json:
        try:
            q_data = json.loads(q_json)
            selected_questions.append(q_data)
            total_marks += float(q_data.get('marks', 0))
        except:
            continue
    
    # Store in session
    request.session['generated_exam'] = {
        'title': exam_title,
        'class_id': class_id,
        'duration': duration,
        'total_marks': total_marks,
        'questions': selected_questions
    }
    
    messages.success(request, f'Exam paper generated with {len(selected_questions)} questions!')
    return redirect('review_auto_exam', exam_id=1)  # You'll need proper ID handling

@login_required
def review_auto_exam(request, exam_id):
    """Review generated exam paper before publishing"""
    auto_exam = get_object_or_404(AutoExamPaper, id=exam_id, teacher=request.user)
    
    # Get all selected questions with their details
    selections = auto_exam.question_selections.all().order_by('question_number')
    
    questions_data = []
    for selection in selections:
        question = selection.question
        questions_data.append({
            'number': selection.question_number,
            'section': selection.section,
            'marks': selection.marks,
            'difficulty': selection.difficulty,
            'question': question,
            'has_options': bool(question.option1 or question.option2 or question.option3 or question.option4),
            'options': {
                'option1': question.option1,
                'option2': question.option2,
                'option3': question.option3,
                'option4': question.option4,
            } if question.question_type == 'MCQ' else None,
            'correct_answer': question.correct_options or question.answer,
        })
    
    context = {
        'auto_exam': auto_exam,
        'generated_paper': auto_exam.generated_paper,
        'questions_data': questions_data,
        'step': 3
    }
    return render(request, 'review_auto_exam.html', context)


@login_required
def publish_auto_exam(request, exam_id):
    """Publish the generated exam paper"""
    auto_exam = get_object_or_404(AutoExamPaper, id=exam_id, teacher=request.user)
    
    auto_exam.status = 'PUBLISHED'
    auto_exam.published_at = timezone.now()
    auto_exam.save()
    
    if auto_exam.generated_paper:
        auto_exam.generated_paper.status = 'published'
        auto_exam.generated_paper.is_published = True
        auto_exam.generated_paper.save()
    
    messages.success(request, 'Exam paper published successfully!')
    return redirect('teacher_generated_papers')


@login_required
def regenerate_auto_exam(request, exam_id):
    """Regenerate exam paper with same parameters"""
    auto_exam = get_object_or_404(AutoExamPaper, id=exam_id, teacher=request.user)
    
    # Delete existing selections and usage logs
    auto_exam.question_selections.all().delete()
    auto_exam.usage_logs.all().delete()
    
    # Get subject
    try:
        subject = Subject.objects.get(name__iexact=auto_exam.subject)
    except Subject.DoesNotExist:
        messages.error(request, 'Subject not found.')
        return redirect('review_auto_exam', exam_id=exam_id)
    
    # Parse topics
    topics_list = [t.strip() for t in auto_exam.topics.split(',') if t.strip()] if auto_exam.topics else []
    exclude_topics_list = [t.strip() for t in auto_exam.exclude_topics.split(',') if t.strip()] if auto_exam.exclude_topics else []
    
    # Generate new questions
    all_selected_questions = []
    
    if auto_exam.mcq_count > 0:
        questions = select_questions_for_exam(
            subject, 'MCQ', auto_exam.mcq_count, auto_exam.mcq_marks,
            topics_list, exclude_topics_list, auto_exam.difficulty_distribution,
            auto_exam.avoid_recent_questions
        )
        all_selected_questions.extend([(q, 'MCQ', auto_exam.mcq_marks) for q in questions])
    
    if auto_exam.short_count > 0:
        questions = select_questions_for_exam(
            subject, 'SHORT', auto_exam.short_count, auto_exam.short_marks,
            topics_list, exclude_topics_list, auto_exam.difficulty_distribution,
            auto_exam.avoid_recent_questions
        )
        all_selected_questions.extend([(q, 'SHORT', auto_exam.short_marks) for q in questions])
    
    if auto_exam.long_count > 0:
        questions = select_questions_for_exam(
            subject, 'LONG', auto_exam.long_count, auto_exam.long_marks,
            topics_list, exclude_topics_list, auto_exam.difficulty_distribution,
            auto_exam.avoid_recent_questions
        )
        all_selected_questions.extend([(q, 'LONG', auto_exam.long_marks) for q in questions])
    
    if auto_exam.vlong_count > 0:
        questions = select_questions_for_exam(
            subject, 'VLONG', auto_exam.vlong_count, auto_exam.vlong_marks,
            topics_list, exclude_topics_list, auto_exam.difficulty_distribution,
            auto_exam.avoid_recent_questions
        )
        all_selected_questions.extend([(q, 'VLONG', auto_exam.vlong_marks) for q in questions])
    
    # Randomize if needed
    if auto_exam.randomize_order:
        random.shuffle(all_selected_questions)
    
    # Save new selections
    question_number = 1
    content_type = ContentType.objects.get_for_model(Question)
    
    for question, section, marks in all_selected_questions:
        AutoExamSelection.objects.create(
            auto_exam=auto_exam,
            content_type=content_type,
            object_id=question.id,
            question_number=question_number,
            section=section,
            marks=marks,
            difficulty=question.difficulty.upper() if question.difficulty else 'MEDIUM'
        )
        
        QuestionUsageLog.objects.create(
            content_type=content_type,
            object_id=question.id,
            auto_exam=auto_exam,
            used_by=request.user
        )
        
        question.usage_count += 1
        question.last_used = timezone.now()
        question.save()
        
        question_number += 1
    
    messages.success(request, f'Exam regenerated successfully with {len(all_selected_questions)} questions!')
    return redirect('review_auto_exam', exam_id=auto_exam.id)


# Template management views
@login_required
def save_auto_exam_template(request):
    """Save current exam configuration as template"""
    if request.method != 'POST':
        return redirect('auto_create_exam')
    
    template_name = request.POST.get('template_name')
    template_description = request.POST.get('template_description', '')
    exam_id = request.POST.get('exam_id')
    
    if not template_name:
        messages.error(request, 'Template name is required.')
        return redirect('review_auto_exam', exam_id=exam_id)
    
    auto_exam = get_object_or_404(AutoExamPaper, id=exam_id, teacher=request.user)
    
    template = AutoExamTemplate.objects.create(
        name=template_name,
        description=template_description,
        teacher=request.user,
        subject=auto_exam.subject,
        total_marks=auto_exam.total_marks,
        duration=auto_exam.duration,
        total_questions=auto_exam.total_questions,
        mcq_count=auto_exam.mcq_count,
        mcq_marks=auto_exam.mcq_marks,
        short_count=auto_exam.short_count,
        short_marks=auto_exam.short_marks,
        long_count=auto_exam.long_count,
        long_marks=auto_exam.long_marks,
        vlong_count=auto_exam.vlong_count,
        vlong_marks=auto_exam.vlong_marks,
        difficulty_distribution=auto_exam.difficulty_distribution,
        randomize_order=auto_exam.randomize_order,
        include_answer_key=auto_exam.include_answer_key,
        avoid_recent_questions=auto_exam.avoid_recent_questions
    )
    
    messages.success(request, f'Template "{template_name}" saved successfully!')
    return redirect('review_auto_exam', exam_id=exam_id)


@login_required
def list_auto_exam_templates(request):
    """List all saved templates"""
    templates = AutoExamTemplate.objects.filter(teacher=request.user)
    
    context = {
        'templates': templates
    }
    return render(request, 'teacher/auto_exam_templates.html', context)


@login_required
def load_auto_exam_template(request, template_id):
    """Load a template into the exam creation form"""
    template = get_object_or_404(AutoExamTemplate, id=template_id, teacher=request.user)
    
    template.usage_count += 1
    template.last_used = timezone.now()
    template.save()
    
    request.session['template_data'] = {
        'subject': template.subject,
        'total_marks': template.total_marks,
        'duration': template.duration,
        'total_questions': template.total_questions,
        'mcq_count': template.mcq_count,
        'mcq_marks': template.mcq_marks,
        'short_count': template.short_count,
        'short_marks': template.short_marks,
        'long_count': template.long_count,
        'long_marks': template.long_marks,
        'vlong_count': template.vlong_count,
        'vlong_marks': template.vlong_marks,
        'difficulty_distribution': template.difficulty_distribution,
        'randomize_order': template.randomize_order,
        'include_answer_key': template.include_answer_key,
        'avoid_recent_questions': template.avoid_recent_questions,
    }
    
    messages.success(request, f'Template "{template.name}" loaded successfully!')
    return redirect('auto_create_exam')


@login_required
def delete_auto_exam_template(request, template_id):
    """Delete a template"""
    template = get_object_or_404(AutoExamTemplate, id=template_id, teacher=request.user)
    template.delete()
    
    messages.success(request, 'Template deleted successfully!')
    return redirect('list_auto_exam_templates')


@login_required
def list_auto_exam_templates(request):
    """List all saved templates"""
    # Get all templates created by the logged-in teacher
    templates = AutoExamTemplate.objects.filter(teacher=request.user).order_by('-created_at')
    
    context = {
        'templates': templates
    }
    return render(request, 'list_auto_exam_templates.html', context)


from django.http import JsonResponse
from .models import Subject, Question

@login_required
def get_chapters_by_subject(request):
    """AJAX view to get chapters for a subject from Question model"""
    subject_id = request.GET.get('subject_id')
    
    if not subject_id:
        return JsonResponse({'chapters': []})
    
    try:
        subject = Subject.objects.get(id=subject_id)
        
        # Get unique chapters from Question model for this subject
        chapters = Question.objects.filter(
            subject=subject,
            chapter__isnull=False
        ).exclude(chapter='').values_list('chapter', flat=True).distinct().order_by('chapter')[:50]
        
        chapter_list = [{'id': ch, 'name': ch} for ch in chapters]
        
        return JsonResponse({'chapters': chapter_list})
    
    except Subject.DoesNotExist:
        return JsonResponse({'chapters': [], 'error': 'Subject not found'})
    except Exception as e:
        return JsonResponse({'chapters': [], 'error': str(e)})

from .models import Package, Student, Staff, Course, Question

@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def manage_packages(request, package_id=None):
    """
    Handle package operations:
    - GET: Retrieve package(s)
    - POST: Create/Update package
    - DELETE: Delete package
    """
    if request.method == "GET":
        if package_id:
            # Get single package
            try:
                package = Package.objects.get(id=package_id)
                return JsonResponse({
                    'status': 'success',
                    'package': {
                        'id': package.id,
                        'name': package.name,
                        'type': package.type,
                        'price': float(package.price),
                        'original_price': float(package.original_price),
                        'validity': package.validity,
                        'description': package.description,
                        'features': package.get_features_list(),
                        'subjects': package.get_subjects_list(),
                        'badge': package.badge,
                        'image': package.image,
                        'is_active': package.is_active,
                        'display_order': package.display_order
                    }
                })
            except Package.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Package not found'}, status=404)
        else:
            # Get all packages
            packages = Package.objects.all().order_by('display_order')
            package_list = []
            for pkg in packages:
                package_list.append({
                    'id': pkg.id,
                    'name': pkg.name,
                    'type': pkg.type,
                    'price': float(pkg.price),
                    'original_price': float(pkg.original_price),
                    'validity': pkg.validity,
                    'description': pkg.description,
                    'features': pkg.get_features_list(),
                    'subjects': pkg.get_subjects_list(),
                    'badge': pkg.badge,
                    'image': pkg.image,
                    'is_active': pkg.is_active,
                    'display_order': pkg.display_order
                })
            return JsonResponse({'status': 'success', 'packages': package_list})
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            
            if package_id:
                # Update existing package
                package = get_object_or_404(Package, id=package_id)
            else:
                # Create new package
                package = Package()
            
            # Update fields
            package.name = data.get('name', package.name)
            package.type = data.get('type', package.type)
            package.price = data.get('price', package.price)
            package.original_price = data.get('original_price', package.original_price)
            package.validity = data.get('validity', package.validity)
            package.description = data.get('description', package.description)
            
            # Handle features (convert list to newline-separated string)
            data = json.loads(request.body)

            features = data.get('features', [])
            subjects = data.get('subjects', [])

            package.features = '\n'.join(features) if isinstance(features, list) else features
            package.subjects = ','.join(subjects) if isinstance(subjects, list) else subjects
            
            package.badge = data.get('badge', package.badge)
            package.image = data.get('image', package.image)
            package.is_active = data.get('is_active', package.is_active)
            package.display_order = data.get('display_order', package.display_order)
            
            package.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Package saved successfully',
                'package_id': package.id
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    elif request.method == "DELETE":
        try:
            package = get_object_or_404(Package, id=package_id)
            package.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Package deleted successfully'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def edit_package_page(request):
    """Render the package edit page"""
    package_id = request.GET.get('id')
    package = None
    if package_id:
        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            messages.error(request, 'Package not found')
            return redirect('admin_dashboard')
    
    return render(request, 'edit_package.html', {'package': package})

@login_required
def get_packages(request):
    """Get all packages"""
    try:
        packages = Package.objects.all().order_by('display_order')
        package_list = []
        for pkg in packages:
            package_list.append({
                'id': pkg.id,
                'name': pkg.name,
                'type': pkg.type,
                'price': float(pkg.price),
                'original_price': float(pkg.original_price),
                'validity': pkg.validity,
                'description': pkg.description,
                'features': pkg.get_features_list(),
                'subjects': pkg.get_subjects_list(),
                'badge': pkg.badge,
                'image': pkg.image,
                'is_active': pkg.is_active,
                'display_order': pkg.display_order
            })
        return JsonResponse({'status': 'success', 'packages': package_list})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def get_package(request, package_id):
    """Get single package by ID"""
    try:
        package = get_object_or_404(Package, id=package_id)
        return JsonResponse({
            'status': 'success',
            'package': {
                'id': package.id,
                'name': package.name,
                'type': package.type,
                'price': float(package.price),
                'original_price': float(package.original_price),
                'validity': package.validity,
                'description': package.description,
                'features': package.get_features_list(),
                'subjects': package.get_subjects_list(),
                'badge': package.badge,
                'image': package.image,
                'is_active': package.is_active,
                'display_order': package.display_order
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@login_required

def save_package(request):

    if request.method == "POST":

        data = json.loads(request.body)

        name = data.get("name")
        type = data.get("type")
        price = data.get("price")
        original_price = data.get("original_price")
        validity = data.get("validity")
        description = data.get("description")

        features = data.get("features", "")
        subjects = data.get("subjects", "")

        badge = data.get("badge")
        image = data.get("image")
        is_active = data.get("is_active", True)
        display_order = data.get("display_order", 0)

        package = Package.objects.create(
            name=name,
            type=type,
            price=price,
            original_price=original_price,
            validity=validity,
            description=description,
            features=features,
            subjects=subjects,
            badge=badge,
            image=image,
            is_active=is_active,
            display_order=display_order
        )

        return JsonResponse({
            "status": "success",
            "id": package.id
        })

    return JsonResponse({"status": "error"})
@csrf_exempt
@login_required
def update_package(request, package_id):
    """Update existing package"""
    if request.method == 'POST':
        try:
            package = get_object_or_404(Package, id=package_id)
            data = json.loads(request.body)

            # Update fields
            package.name = data.get('name', package.name)
            package.type = data.get('type', package.type)
            package.price = data.get('price', package.price)
            package.original_price = data.get('original_price', package.original_price)
            package.validity = data.get('validity', package.validity)
            package.description = data.get('description', package.description)

            # ✅ FIX HERE
            features = data.get('features', [])
            if isinstance(features, list):
                package.features = '\n'.join(features)
            else:
                package.features = features

            # Subjects
            subjects = data.get('subjects', [])
            if isinstance(subjects, list):
                package.subjects = ','.join(subjects)
            else:
                package.subjects = subjects

            package.badge = data.get('badge', package.badge)
            package.image = data.get('image', package.image)
            package.is_active = data.get('is_active', package.is_active)
            package.display_order = data.get('display_order', package.display_order)

            package.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Package updated successfully'
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def delete_package(request, package_id):
    """Delete package"""
    if request.method == 'POST':
        try:
            package = get_object_or_404(Package, id=package_id)
            package.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Package deleted successfully'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def toggle_package_status(request, package_id):
    """Toggle package active status"""
    if request.method == 'POST':
        try:
            package = get_object_or_404(Package, id=package_id)
            package.is_active = not package.is_active
            package.save()
            return JsonResponse({
                'status': 'success',
                'message': f'Package {"activated" if package.is_active else "deactivated"} successfully',
                'is_active': package.is_active
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def buy_package(request, package_id):

    package = get_object_or_404(Package, id=package_id)

    # check if already purchased
    already = PackagePurchase.objects.filter(
        student=request.user,
        package=package,
        is_active=True
    ).first()

    if not already:
        expiry = now() + timedelta(days=30)

        PackagePurchase.objects.create(
            student=request.user,
            package=package,
            expiry_date=expiry,
            amount_paid=package.price
        )

    return redirect('student')


import razorpay

def payment_view(request, package_id):

    package = get_object_or_404(Package, id=package_id)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": int(package.price * 100),  # Razorpay uses paise
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "package": package,
        "razorpay_order_id": payment["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": int(package.price * 100),
        "currency": "INR"
    }

    return render(request, "payment.html", context)
@csrf_exempt
@login_required
def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)

        package_id = data.get("package_id")
        payment_id = data.get("payment_id")
        order_id = data.get("order_id")

        package = get_object_or_404(Package, id=package_id)

        expiry = now() + timedelta(days=30)

        PackagePurchase.objects.create(
            student=request.user,
            package=package,
            expiry_date=expiry,
            amount_paid=package.price,
            payment_id=payment_id,
            order_id=order_id,
            status="SUCCESS"
        )

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"})
def transaction_history(request):
    transactions = PackagePurchase.objects.filter(
        student=request.user
    ).order_by('-created_at')

    return render(request, "transaction.html", {
        "transactions": transactions
    })