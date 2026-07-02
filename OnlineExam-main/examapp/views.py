import uuid
from django.shortcuts import get_object_or_404, render ,redirect,HttpResponse
from Online_App.models import User 
from django.contrib.auth import authenticate ,login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from Online_App.models import User,Staff,ExamSchedule
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib import messages
from .models import Order, StudentProfile,Exam, Option, UserAnswer,Question1, Feedback
from .forms import PaymentForm,ExamSubmissionForm,QuestionForm


def Index(request):
    return render(request,'index1.html')

User = get_user_model()
# def Register(request):
#     if request.method == "POST":
#         a = request.POST['firstname']
#         b = request.POST['email']
#         c = request.POST['username']
#         d = request.POST['password']
#         e = int(request.POST['usertype'])

#         # Check if the username or email already exists
#         if User.objects.filter(username=c).exists():
#             return HttpResponse("<script>window.alert('Username already exists. Please choose a different one.');window.location.href='/reg/';</script>")
#         if User.objects.filter(email=b).exists():
#             return HttpResponse("<script>window.alert('Email already exists. Please use a different one.');window.location.href='/reg/';</script>")

#         try:
#             with transaction.atomic():  # Wrap the user creation within a transaction
#                 f = User.objects.create_user(
#                     first_name=a,
#                     email=b,
#                     username=c,
#                     password=d,
#                     user_type=e
#                 )
#                 if e == 1:  # Admin
#                     f.is_superuser = True
#                     f.is_staff = True
#                 elif e == 2:  # Staff
#                     f.is_staff = True
#                 else:  # Parent or Student
#                     f.is_staff = False
#                     f.is_superuser = False
#                 f.save()
#             return HttpResponse("<script>window.alert('Saved Successfully');window.location.href='/log/';</script>")
#         except IntegrityError:
#             return HttpResponse("<script>window.alert('An error occurred while saving the user. Please try again.');window.location.href='/reg/';</script>")
#     else:
#         return render(request, 'register.html')

# def Login(request):
#     if request.method == "POST":
#         a = request.POST['username']
#         b = request.POST['password']
#         user = authenticate(request, username=a, password=b)

#         if user is not None:
#             login(request, user)

#             # Check if the user is a superuser
#             if user.is_superuser:
#                 return redirect('admin_dashboard')  # Redirect to the admin dashboard or admin page

#             # Check for the user type if not a superuser
#             if user.user_type == 1:
#                 return redirect('admin_dashboard')  # Redirect to admin dashboard
#             elif user.user_type == 2:
#                 return redirect('Teacher')
#             elif user.user_type == 3:
#                 return redirect('Parent')
#             else:
#                 return redirect('Student')  # Student user type

#         else:
#             return HttpResponse("<script>window.alert('Invalid Credentials');window.location.href='/log/';</script>")

#     return render(request, 'login.html')


# def View(request):
#     if request.user.is_superuser:  # Check if the user is a superuser
#         return render(request, 'admin-dashboard.html', {'data': request.user})
#     else:
#         return HttpResponse("<script>window.alert('Unauthorized Access!');window.location.href='/log/';</script>")
# def Student(request):
#     if request.user.is_authenticated:
#         context = {'data': {'username': request.user.username}}
#         return render(request, 'student.html', context)
#     else:
#         return redirect('Login')  # Redirect to the login page if the user is not authenticated
def Profile(request):
    return render(request,'Profile.html')
def Parent(request):
    if request.user.is_authenticated:
        # Pass the username in the context dictionary
        context = {'data': {'username': request.user.username}}
        return render(request, 'Parent.html', context)
    else:
        return redirect('Login')  # Redirect to the login page if the user is not authenticated

def Exams(request):
    if request.user.is_authenticated:
        context = {'data': {'username': request.user.username}}
        return render(request, 'Exam.html', context)
    else:
        return redirect('Login') 
def Data(request):
    return render(request,'Data-entry.html')
# def Teacher(request):
#     if request.user.is_authenticated:
#         context = {'data': {'username': request.user.username}}
#         return render(request, 'teacher.html', context)
#     else:
#         return redirect('Login')  # Redirect to the login page if the user is not authenticated

def staff_list(request):
    if request.user.is_authenticated:  # Ensure the user is logged in
        staff_members = Staff.objects.all()
        return render(request, 'staff_list.html', {'staff_members': staff_members})
    else:
        return redirect('Login')  # Redirect to login if not authenticated


@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_summary.html', {'order': order})

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


def buy_product(request):
    # Razorpay Client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Item price (in paise)
    amount = 999  # ₹9.99 means 9.99 * 100 = 999 paise

    # Create order
    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "order_id": payment["id"],
        "amount": amount,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }

    return render(request, "buy_product.html", context)


@csrf_exempt
def payment_success(request):
    messages.success(request, "Payment Successful!")
    return render(request, "success.html")


@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == "POST":
        form = ExamSubmissionForm(request.POST, exam=exam)
        
        if form.is_valid():
            for question in exam.questions.all():
                selected_option_id = form.cleaned_data.get(f'question_{question.id}')
                
                if selected_option_id:  # Ensure the user selected an option
                    try:
                        selected_option = Option.objects.get(id=selected_option_id)
                        UserAnswer.objects.create(
                            user=request.user, question=question, selected_option=selected_option
                        )
                    except Option.DoesNotExist:
                        messages.error(request, f"Invalid option selected for question {question.id}")
                        return redirect('take_exam', exam_id=exam.id)

            return redirect('exam_result', exam_id=exam.id)
        else:
            messages.error(request, "There was an error with your submission.")
    
    else:
        form = ExamSubmissionForm(exam=exam)

    return render(request, 'exam/test_page.html', {'exam': exam, 'form': form})
@login_required
def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    user_answers = UserAnswer.objects.filter(user=request.user, question__exam=exam)
    correct_answers = sum(1 for answer in user_answers if answer.is_correct())
    total_questions = exam.questions.count()

    return render(request, 'exam/result.html', {
        'exam': exam, 
        'correct_answers': correct_answers, 
        'total_questions': total_questions
    })
def test_page(request):
    session_id = str(uuid.uuid4())
    if request.user.is_authenticated:
        request.session['test_started'] = False
        request.session['test_data'] = {}  # You can store test data here if needed

        subject = request.GET.get('subject')  # Get subject from query parameter

        if subject:
            questions = Question1.objects.filter(subject=subject)  # Fetch questions for the selected subject
        else:
            questions = Question1.objects.all()  # Fetch all questions if no subject is selected

        context = {
            'data': {'username': request.user.username},
            'questions': questions,
            'selected_subject': subject  # Pass selected subject to the template
        }
        return render(request, 'test_page.html', context)
    else:
        return redirect('Login')
# View for starting a new test or logging in
def start_new_test(request):
    if request.user.is_authenticated:
        # Clear the previous session test data for a fresh start
        request.session['test_started'] = False
        return redirect('exam_page')  # Redirect to the test page

    return redirect('login_page')  # If not logged in, redirect to login page   

#question adding
@login_required
def submit_test(request):
    if request.method == "POST":
        total_questions = Question1.objects.count()
        correct_answers = 0
        user_answers = []

        # Assuming `exam_id` is stored in session or passed via form
        exam_id = request.session.get("exam_id")
        exam = Exam.objects.get(id=exam_id) if exam_id else None

        for question in Question1.objects.all():
            selected_option_id = request.POST.get(f"q{question.id}")

            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=selected_option_id)
                    is_correct = selected_option.is_correct

                    user_answers.append({
                        "question": question.question,  # Fix reference to `question`
                        "selected": selected_option.text,
                        "correct": question.option_set.filter(is_correct=True).first().text
                    })

                    if is_correct:
                        correct_answers += 1

                    # Save user response
                    UserAnswer.objects.create(
                        user=request.user,
                        question=question,
                        selected_option=selected_option,
                        exam=exam  # Fixed exam reference
                    )

                except Option.DoesNotExist:
                    messages.error(request, f"Invalid option selected for question {question.id}")
                    return redirect("test_page")

        score = f"{correct_answers} / {total_questions}"
        time_taken = request.session.get("time_taken", "N/A")  # Safely retrieve time data

        return render(request, "result.html", {
            "username": request.user.username,
            "score": score,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "time_taken": time_taken,
            "user_answers": user_answers
        })
    
    return redirect("test_page")

def student_profile(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        date_of_birth = request.POST.get("date_of_birth")
        mobile_number = request.POST.get("mobile_number")
        email = request.POST.get("email")
        guardian_name = request.POST.get("guardian_name")
        guardian_number = request.POST.get("guardian_number")
        address = request.POST.get("address")
        pin_code = request.POST.get("pin_code")

        # Clean numeric/optional fields
        classX_board = request.POST.get("classX_board") or None
        classX_percentage = request.POST.get("classX_percentage") or None
        classX_year = request.POST.get("classX_year") or None

        classXII_board = request.POST.get("classXII_board") or None
        classXII_percentage = request.POST.get("classXII_percentage") or None
        classXII_year = request.POST.get("classXII_year") or None

        gender = request.POST.get("gender")
        course_applied_for = request.POST.get("course_applied_for")

        # Convert numeric fields to float/int (only if not empty)
        if classX_percentage:
            classX_percentage = float(classX_percentage)

        if classXII_percentage:
            classXII_percentage = float(classXII_percentage)

        if classX_year:
            classX_year = int(classX_year)

        if classXII_year:
            classXII_year = int(classXII_year)

        # Prevent duplicate student records
        if StudentProfile.objects.filter(user=request.user).exists():
            messages.error(request, "Profile already exists.")
            return redirect("student_profile")

        # Check if email is already used by another user
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Email already exists. Please use another email.")
            return redirect("student_profile")

        # Save student profile
        student = StudentProfile(
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

            classX_board=classX_board,
            classX_percentage=classX_percentage,
            classX_year=classX_year,

            classXII_board=classXII_board,
            classXII_percentage=classXII_percentage,
            classXII_year=classXII_year,

            gender=gender,
            course_applied_for=course_applied_for,
        )

        student.save()
        messages.success(request, "Registration successful!")
        return redirect("student_profile")

    return render(request, "student.html")


#exam schedule
def exam_schedule_view(request):
    exams = ExamSchedule.objects.all().order_by('exam_date', 'exam_time')  # Order by date and time
    return render(request, 'exam_schedule.html', {'exams': exams})

#feedback schedule
def submit_feedback(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")

        Feedback.objects.create(name=name, email=email, message=message)
        return HttpResponse("<script>window.alert('thankyou for the feedback.');window.location.href='/student/';</script>")

    return render(request, "feedback.html")
#adding question
def add_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_question")  # Redirect to the same page after saving
    else:
        form = QuestionForm()

    return render(request, "add_question.html", {"form": form})

@login_required
def test_results(request):
    # Dummy data (Replace with actual data from your database)
    user_answers = [
        {'question': 'What is 2 + 2?', 'selected': '4', 'correct': '4'},
        {'question': 'What is the capital of France?', 'selected': 'Paris', 'correct': 'Paris'},
        {'question': 'What is the boiling point of water?', 'selected': '90°C', 'correct': '100°C'},
    ]

    context = {
        'username': request.user.username,
        'score': 2,  # Example score (Replace with real data)
        'time_taken': '10 min',  # Example time (Replace with real data)
        'user_answers': user_answers
    }

    return render(request, 'result.html', context)



# In views.py
from django.utils import timezone
from datetime import timedelta
import json

# Student Exam Views
@login_required
def student_available_exams(request):
    """Show all exams available to the student"""
    # Get current date and time
    now = timezone.now()
    
    # Get all question papers that are available for students
    available_papers = QuestionPaper.objects.filter(
        is_published=True,
        exam_date_actual__lte=now.date()  # Past or today's papers
    ).order_by('-created_at')
    
    # Get exams the student has already taken
    completed_exam_ids = ExamResult.objects.filter(
        student=request.user
    ).values_list('question_paper_id', flat=True)
    
    # Filter out completed exams
    available_papers = available_papers.exclude(id__in=completed_exam_ids)
    
    context = {
        'exams': available_papers,
        'username': request.user.username,
        'today': now.date()
    }
    return render(request, 'student/available_exams.html', context)

@login_required
def student_start_exam(request, paper_id):
    """Student starts an exam"""
    paper = get_object_or_404(QuestionPaper, id=paper_id, is_published=True)
    
    # Check if student has already taken this exam
    if ExamResult.objects.filter(student=request.user, question_paper=paper).exists():
        messages.error(request, "You have already taken this exam.")
        return redirect('student_available_exams')
    
    # Store exam info in session
    request.session['current_exam_id'] = paper_id
    request.session['exam_start_time'] = str(timezone.now())
    request.session['exam_answers'] = {}
    
    # Get all questions from the paper
    all_questions = []
    
    # Get mathematics questions
    math_questions = paper.mathematics_questions.all()
    for q in math_questions:
        all_questions.append({
            'id': f'math_{q.id}',
            'subject': 'Mathematics',
            'question': q.question,
            'type': q.question_type,
            'marks': 4,
            'options': get_options_dict(q) if q.question_type == 'objective' else None,
            'correct_answer': get_correct_answer(q)
        })
    
    # Get physics questions
    physics_questions = paper.physics_questions.all()
    for q in physics_questions:
        all_questions.append({
            'id': f'physics_{q.id}',
            'subject': 'Physics',
            'question': q.question,
            'type': q.question_type,
            'marks': 4,
            'options': get_options_dict(q) if q.question_type == 'objective' else None,
            'correct_answer': get_correct_answer(q)
        })
    
    # Get chemistry questions
    chemistry_questions = paper.chemistry_questions.all()
    for q in chemistry_questions:
        all_questions.append({
            'id': f'chemistry_{q.id}',
            'subject': 'Chemistry',
            'question': q.question,
            'type': q.question_type,
            'marks': 4,
            'options': get_options_dict(q) if q.question_type == 'objective' else None,
            'correct_answer': get_correct_answer(q)
        })
    
    # Get biology questions
    biology_questions = paper.biology_questions.all()
    for q in biology_questions:
        all_questions.append({
            'id': f'biology_{q.id}',
            'subject': 'Biology',
            'question': q.question,
            'type': q.question_type,
            'marks': 4,
            'options': get_options_dict(q) if q.question_type == 'objective' else None,
            'correct_answer': get_correct_answer(q)
        })
    
    # Shuffle questions (optional)
    import random
    random.shuffle(all_questions)
    
    # Store questions in session
    request.session['exam_questions'] = all_questions
    request.session['current_question_index'] = 0
    
    context = {
        'paper': paper,
        'total_questions': len(all_questions),
        'exam_time': paper.exam_time if paper.exam_time else 180,  # Default 3 hours
        'username': request.user.username
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

@login_required
def student_exam_results(request):
    """View all exam results for the student"""
    results = ExamResult.objects.filter(student=request.user).order_by('-submitted_at')
    
    context = {
        'results': results,
        'username': request.user.username
    }
    
    return render(request, 'student/exam_results.html', context)

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