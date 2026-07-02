"""
URL configuration for Online_Exam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path,include
from examapp import views


from django.conf import settings
from django.conf.urls.static import static

# app_name = "examapp"

urlpatterns = [
    
    path('',views.Index,name='Index'),
    # path('reg/',views.Register,name='Register'),
    # path('log/',views.Login,name='Login'),
    # path('view/',views.View,name='View'),
    # path('student/',views.Student1,name='Student'),
    path('profile/',views.Profile,name='Profile'),
    path('parent/',views.Parent,name='Parent'),
    
    path('data/',views.Data,name='Data'),
    #path('teacher/',views.Teacher,name='Teacher'),
    # path('staffs/', views.staff_list, name='staff_list'),
    path("create/", views.student_profile, name="student_profile"),
    # path('list/', views.student_list, name='student_list'),
    path('exam/',views.Exams,name='Exam'),
    path('buy/', views.buy_product, name='buy_product'),
    path('order/<int:order_id>/', views.order_summary, name='order_summary'),
    path('takeexam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('examresult/<int:exam_id>/result/', views.exam_result, name='exam_result'),
    path('submit/', views.submit_test, name='submit_test'),
    path('test/', views.test_page, name='test_page'),
    path('start-new-test/', views.start_new_test, name='start_new_test'),
    path('exam-schedule/', views.exam_schedule_view, name='exam_schedule'),
    path("feedbacks/",views.submit_feedback, name="submit_feedback"),
    path("add/", views.add_question, name="add_question"),
    path('test-results/',views. test_results, name='test_results'),


    path("buy-product/", views.buy_product, name="buy-product"),
    path("payment-success/", views.payment_success, name="payment-success"),


   
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)