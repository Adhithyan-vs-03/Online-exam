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
from django.contrib.auth import views as auth_views
from Online_App import views
from django.urls import path,include
# from Online_App import views


urlpatterns = [
    path('',include('examapp.urls')),
    path('admin/', admin.site.urls),
    path('',views.Index,name='Index'),
    path('reg/',views.Register,name='Register'),
    path('log/',views.user_login,name='login'),


# -----------------------------------------------Admin------------------------------------
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('staff/', views.add_staff, name='add_staff'),
    path('staffs/', views.admin_staff_list, name='admin_staff_list'),
    path('staff/edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),

    path('studentss/', views.add_student, name='add_student'),
    path('students/', views.student_list, name='student_list'),
    path('students/view/<str:student_type>/<int:student_id>/', views.view_student, name='view_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),

    path('examschedule/', views.exam_schedule_view, name='exam_schedule'),
    path('delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),

    path('plans/', views.plan_list, name='plan_list'),
    path('plans/create/', views.create_plan, name='create_plan'),
    path('plans/edit/<int:plan_id>/', views.edit_plan, name='edit_plan'),
    path('plans/delete/<int:plan_id>/', views.delete_plan, name='delete_plan'),

    # urls.py
    path('main-dashboard/', views.mainstaff_dashboard, name='mainstaff_dashboard'),
    path('mainstaff/profile/', views.mainstaff_profile, name='main_staff_dashboard'),
    path('mainstaff/profile/edit/', views.mainstaff_edit_profile, name='mainstaff_edit_profile'),

    path('add-class/', views.add_class, name='add_class'),
    path('mainstaff/profile/', views.mainstaff_profile, name='mainstaff_profile'),
    path('mainstaff/profile/photo/', views.mainstaff_update_photo, name='mainstaff_update_photo'),
   
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('add-subject/', views.add_subject, name='add_subject'),
    # path('subject/added/<int:subject_id>/', views.subject_added, name="subject_added"),
    # path('add-chapter/<int:subject_id>/', views.add_chapter, name="add_chapter"),
    # path('add-questions/', views.add_questions, name='add_questions'),
   
    path('add-class/', views.add_class, name='add_class'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('add-chapter/', views.add_chapter, name='add_chapter'),  # FIXED
    path('add-topic/', views.add_topic, name='add_topic'),
    path('add-subtopic/', views.add_subtopic, name='add_subtopic'),

    path('class_list/', views.class_list, name='class_list'),

    path("class-details/", views.class_list, name="class_list"),               # list page (no id)
    path("class-details/<int:class_id>/", views.class_details, name="class_details"),  # detail (needs id)
    path('manage_subjects/', views.manage_subjects, name='manage_subjects'),


    path('ai-process-content/', views.ai_process_content, name='ai_process_content'),
    path('save-ai-content/', views.save_ai_content, name='save_ai_content'),

    path('ai-content-importer/', views.ai_content_importer, name='ai_content_importer'),
    path('ai-process-content/', views.ai_process_content, name='ai_process_content'),
    path('save-ai-content/', views.save_ai_content, name='save_ai_content'),
    path('notifications/', views.notifications_page, name='notifications_page'),

    
    
    path('upload-question-image/', views.upload_question_image, name='upload_question_image'),

    path('view-questions/', views.question_filter_page, name="view_questions"),
    path('ajax/get-chapters/', views.get_chapters, name="get_chapters"),
    path('ajax/get-topics/', views.get_topics, name="get_topics"),
    path('ajax/get-subtopics/', views.get_subtopics, name="get_subtopics"),
    path('ajax/get-questions/', views.get_questions, name="get_questions"),

    path('view-chemistry-question/<int:question_id>/', views.view_chemistry_question_detail, name='view_chemistry_question_detail'),
    path('mathematics-question/<int:question_id>/', views.view_mathematics_question_detail, name='view_mathematics_question_detail'),
    path('physics-question/<int:question_id>/', views.view_physics_question_detail, name='view_physics_question_detail'),
    path('add-biology-question/', views.add_biology_question, name='add_biology_question'),
    path('biology-question/<int:question_id>/', views.view_biology_question_detail, name='view_biology_question_detail'),



    path('student/',views.Student1,name='Student'),
    path('profile/',views.Profile,name='Profile'),
    path('parent/',views.Parent,name='Parent'),
    path('data/',views.Data,name='Data'),
    path('teacher/',views.Teacher,name='Teacher'),
    # path('staffs/', views.staff_list, name='staff_list'),
    # path('students/', views.student_profiles, name='student_list'),
    path('teachers/', views.teacher_profile, name='teacher_profile'),
    path('marks/', views.student_marks, name='student_marks'),
    path('create-exam/', views.create_exam_and_question_paper, name='Create-exam'),
    path('parent-result/', views.parent_result, name='Parent_result'),
    
    path('add-exam-schedule/', views.add_exam_schedule, name='Add_exam_schedule'),  # Page for adding exams
    path('save-exam-details/', views.save_exam_details, name='Save_exam_details'),  # Save exam data
    path('get-exam-details/', views.get_exam_details, name='Get_exam_details'),  # Fetch exam details for parent.html


    path('student/available-exams/', views.student_available_exams, name='student_available_exams'),
    # path('student/start-exam/<int:paper_id>/', views.student_start_exam, name='student_start_exam'),
    path('student/take-exam/<int:question_index>/', views.student_take_exam, name='student_take_exam'),
    path('student/submit-exam/', views.student_submit_exam, name='student_submit_exam'),
    # path('student/exam-results/', views.student_exam_results, name='student_exam_results'),
    path('student/view-result/<int:result_id>/', views.student_view_result_detail, name='student_view_result_detail'),
    path('submit-exam/', views.submit_exam, name='submit_exam'),
    # path('student/submit-exam/<int:paper_id>/', views.submit_exam, name='submit_exam'),
    path('student/exam-results/', views.student_exam_results, name='student_exam_results'),
    path('student/exam-result/<int:result_id>/', views.exam_result_detail, name='exam_result_detail'),
     path('api/test-paper/<int:paper_id>/', views.test_paper_access, name='test_paper_access'),
     
    path('debug-exam-submit/', views.debug_exam_submit, name='debug_exam_submit'),
    
    path('start-exam/<int:paper_id>/', views.start_exam, name='start_exam'),
 
    path('addd-biology-question/', views.addd_biology_question, name='addd_biology_question'),
    path('view-all-questions/', views.view_all_questions, name='view_all_questions'),
    path('view-all-question/', views.view_all_question, name='view_all_question'),
    path('viewing-all-questions/', views.viewing_all_questions, name='viewing_all_questions'),

    path('api/questions/all/', views.get_all_questions, name='get_all_questions'),
    path('api/questions/<int:question_id>/', views.get_question_detail, name='get_question_detail'),
    path('api/questions/<int:question_id>/delete/', views.delete_question_api, name='delete_question_api'),

    path('edit-question/<int:question_id>/', views.edit_question_view, name='edit_question'),


    path('question-paper-generator/', views.question_paper_generator, name='question_paper_generator'),
    path('api/get-all-questions/', views.get_all_questions_api, name='get_all_questions_api'),

    
    
    # Teacher evaluation URLs
    path('teacher/pending-evaluations/', views.teacher_pending_evaluations, name='teacher_pending_evaluations'),
    path('teacher/evaluate/<int:submission_id>/', views.teacher_evaluate_exam, name='teacher_evaluate_exam'),
    path('teacher/save-draft-evaluation/', views.teacher_save_draft_evaluation, name='teacher_save_draft_evaluation'),
    path('teacher/save-marked-sheet/', views.teacher_save_marked_sheet, name='teacher_save_marked_sheet'),
    path('teacher/download-answer-file/<int:submission_id>/', views.download_answer_file, name='download_answer_file'),
    
    # Student view evaluated exams
    path('student/evaluated-exams/', views.student_evaluated_exams, name='student_evaluated_exams'),
    path('student/view-evaluation/<int:submission_id>/', views.student_view_evaluation, name='student_view_evaluation'),
    path('student/download-marked-sheet/<int:submission_id>/', views.download_marked_sheet, name='download_marked_sheet'),

    path('mark-notifications-read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('student/view-evaluated-exam/<int:submission_id>/', views.student_view_evaluated_exam, name='student_view_evaluated_exam'),


    path('student/notifications/', views.student_notifications, name='student_notifications'),
    path('student/mark-notifications-read/', views.mark_notifications_read, name='mark_notifications_read'),

        # Teacher Exam Correction URLs
    path('teacher/pending-evaluations/', views.teacher_pending_evaluations, name='teacher_pending_evaluations'),
    path('teacher/evaluate-exam/<int:submission_id>/', views.teacher_evaluate_exam, name='teacher_evaluate_exam'),
    path('teacher/view-submission/<int:submission_id>/', views.teacher_view_submission, name='teacher_view_submission'),
    path('teacher/evaluated-exams/', views.teacher_evaluated_exams, name='teacher_evaluated_exams'),
    path('teacher/evaluate-existing/<int:result_id>/', views.teacher_evaluate_existing_result, name='teacher_evaluate_existing_result'),
    path('student/create-submission/<int:result_id>/', views.create_submission_for_teacher, name='create_submission_for_teacher'),

    path('teacher/download-answer/<int:submission_id>/', views.download_answer_file, name='download_answer_file'),
    path('teacher/save-draft/<int:submission_id>/', views.save_draft_evaluation, name='save_draft_evaluation'),

    path('question/<int:question_id>/', views.view_question_detail, name='view_question_detail'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('api/question/<int:question_id>/detail/', views.get_question_detail_api, name='question_detail_api'),

    path('download-answer-key/<int:submission_id>/', views.download_answer_key_pdf, name='download_answer_key_pdf'),

    path('question_paper_generator/',views. question_paper_generator, name='question_paper_generator'),
    # API endpoints for question paper generator
    path('api/get-filtered-questions/', views.get_filtered_questions, name='get_filtered_questions'),
    # path('api/save-question-paper/', views.save_question_paper, name='save_question_paper'),
    path('api/get-chapters/', views.get_chapters, name='get_chapters'),
    path('buy-package/<int:package_id>/', views.buy_package, name='buy_package'),



    path('student/notifications/mark-read/<int:notification_id>/', views.student_mark_notification_read, name='student_mark_notification_read'),
    path('student/notifications/mark-all-read/', views.student_mark_all_notifications_read, name='student_mark_all_notifications_read'),


    path('api/save-question-paper/', views.save_question_paper, name='save_question_paper'),
    path('api/generate-pdf/', views.generate_and_download_pdf, name='generate_pdf'),
    path('question-papers/<uuid:unique_id>/download/', views.download_saved_paper, name='download_paper'),
    path('question-papers/<uuid:unique_id>/preview/', views.preview_paper, name='preview_paper'),
    path('my-question-papers/', views.list_generated_papers, name='list_papers'),

    path('api/get-chapters-by-subject/', views.get_chapters_by_subject, name='get_chapters_by_subject'),

    path('get-chapters-by-subject/', views.get_chapters_by_subject, name='get_chapters_by_subject'),
    path('get-questions-by-filters/', views.get_questions_by_filters, name='get_questions_by_filters'),

    path('teacher/save-paper-settings/', views.save_teacher_paper_settings, name='save_teacher_paper_settings'),
    path('teacher/get-paper-settings/', views.get_teacher_paper_settings, name='get_teacher_paper_settings'),
    
    # Question paper generator
    path('teacher/question-paper-generator/', views.question_paper_generator, name='question_paper_generator'),

    path('get-chapters-by-subject/', views.get_chapters_by_subject, name='get_chapters_by_subject'),

     # Auto Exam URLs
    path('auto-create-exam/', views.auto_create_exam, name='auto_create_exam'),
    path('generate-auto-exam/', views.generate_auto_exam, name='generate_auto_exam'),
    path('review-auto-exam/<int:exam_id>/', views.review_auto_exam, name='review_auto_exam'),
    path('publish-auto-exam/<int:exam_id>/', views.publish_auto_exam, name='publish_auto_exam'),
    path('regenerate-auto-exam/<int:exam_id>/', views.regenerate_auto_exam, name='regenerate_auto_exam'),
    path('auto-exam-templates/', views.list_auto_exam_templates, name='list_auto_exam_templates'),

    
    path('get-subjects-by-class/', views.get_subjects_by_class, name='get_subjects_by_class'),
    path('get-chapters-by-subjects/', views.get_chapters_by_subjects, name='get_chapters_by_subjects'),
    path('get-questions-by-chapters/', views.get_questions_by_chapters, name='get_questions_by_chapters'),
    path('generate-questions-from-bank/', views.generate_questions_from_bank, name='generate_questions_from_bank'),
    path('debug-questions/', views.debug_question_data, name='debug_questions'),  # Add this for debugging


    path('add-chemistry-question/',views. add_chemistry_question, name='add_chemistry_question'),
    path('add-physics-question/', views.add_physics_question, name='add_physics_question'),
    path("add-mathematics-question/",views. add_mathematics_question, name="add_mathematics_question"),
    path('add-exam-schedule/', views.add_exam_schedule, name='Add_exam_schedule'),  # Page for adding exams
    path('save-exam-details/', views.save_exam_details, name='Save_exam_details'),  # Save exam data
    path('get-exam-details/', views.get_exam_details, name='Get_exam_details'),  # Fetch exam details for parent.html
    path('payment-list/', views.payment_list, name='payment_list'),  # Ensure this exists
    path('admin-pack/', views.pack, name='admin_pack'),
    path('remove-purchase/<int:purchase_id>/',views. remove_purchase, name='remove_purchase'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('admin/feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('exam-schedule/', lambda request: views.exam_schedule(request, 'exam_schedule.html'), name='Exam_schedule'),
    path('exam-schedule/teacher/', lambda request: views.exam_schedule(request, 'teacher.html'), name='Teacher_exam_schedule'),
    path('exam-schedule/parent/', lambda request: views.exam_schedule(request, 'parent.html'), name='Parent_exam_schedule'),
    path('exam-schedule/admin/', lambda request: views.exam_schedule(request, 'admin-dashboard.html'), name='Admin_exam_schedule'),
    # path("question-creation/", views.question_creation, name="question_creation"),
    path("list/", views.question_list, name="question_list"),
    
    path('staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    
    # path('studentss/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('feedback-lists/', views.feedback_staff, name='feedback_lists'),       
    path('search-students/', views. search_students, name='search_students'),
    path('pass-fail-chart/', views. pass_fail_chart, name='pass_fail_chart'),
    path('view-questions/', views.view_all_questions, name='view_questions'),
    # path("create-question-paper/", views.create_question_paper, name="create_question_paper"),
        # Question Paper Creation Page
    # path('create-question-paper/', views.question_creation, name='question_creation'),

    # Start the Exam (Render the question paper for the student)
    path('start-exam/<int:question_paper_id>/', views.start_exam, name='start_exam'),

    path('delete-physics-question/<int:question_id>/', views.delete_physics_question, name='delete_physics_question'),
     path('delete-mathematics-question/<int:question_id>/', 
         views.delete_mathematics_question, 
         name='delete_mathematics_question'),



    # Teacher URLs
    # path('teacher/create-question-paper/', views.create_question_paper, name='create_question_paper'),
    path('teacher/question-papers/', views.teacher_question_papers, name='teacher_question_papers'),
    path('teacher/question-paper/<int:paper_id>/', views.view_question_paper, name='view_question_paper'),
    
    # Student URLs
    path('student/question-papers/', views.student_question_papers, name='student_question_papers'),
    # path('student/start-exam/<int:paper_id>/', views.student_start_exam, name='student_start_exam'),
    
    # API URLs
    path('api/get-questions/', views.get_questions_json, name='get_questions_json'),
    path('get-questions/', views.get_questions_api, name='get_questions_api'),

    path('biology/<int:question_id>/edit/', views.edit_biology_question, name='edit_biology_question'),
    path('biology/<int:question_id>/delete/', views.delete_biology_question, name='delete_biology_question'),
    path('admin/biology/', views.admin_biology_dashboard, name='admin_biology_dashboard'),



    # Edit URLs for manage_subjects
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    
    
    path('edit-class/<int:class_id>/', views.edit_class, name='edit_class'),
    
    
    path('edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    
    
    path('edit-chapter/<int:chapter_id>/', views.edit_chapter, name='edit_chapter'),
    
    
    path('edit-topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    
    
    path('edit-subtopic/<int:subtopic_id>/', views.edit_subtopic, name='edit_subtopic'),
    

     path('teacher/edit-paper-questions/<int:paper_id>/', 
         views.edit_generated_paper_only_questions, 
         name='edit_generated_paper_only_questions'),
    
    # API endpoint to update questions only
    path('api/update-paper-questions/', 
         views.update_paper_questions_only, 
         name='update_paper_questions_only'),



    path('teacher/generated-papers/', views.teacher_generated_papers, name='teacher_generated_papers'),
    path('teacher/edit-paper/<int:paper_id>/', views.edit_generated_paper, name='edit_generated_paper'),
    path('teacher/preview-paper/<int:paper_id>/', views.preview_generated_paper, name='preview_generated_paper'),
    path('teacher/copy-paper/<int:paper_id>/', views.regenerate_paper_copy, name='regenerate_paper_copy'),
    path('teacher/delete-paper/<int:paper_id>/', views.delete_generated_paper, name='delete_generated_paper'),

    path('teacher/clear-logo/', views.clear_teacher_logo, name='clear_teacher_logo'),


    path('api/update-question-paper/', views.update_question_paper, name='update_question_paper'),
    path('api/check-new-papers/', views.check_new_papers_api, name='check_new_papers_api'),

    path('biology/', views.view_biology_questions, name='view_biology_questions'),
    path('chemistry/', views.view_chemistry_questions, name='view_chemistry_questions'),
    path('physics/', views.view_physics_questions, name='view_physics_questions'),
    path('mathematics/', views.view_mathematics_questions, name='view_mathematics_questions'),

     path('biology/<int:question_id>/edit/', views.edit_biology_question, name='edit_biology_question'),
    path('chemistry/<int:question_id>/edit/', views.edit_chemistry_question, name='edit_chemistry_question'),
    path('physics/<int:question_id>/edit/', views.edit_physics_question, name='edit_physics_question'),
    path('mathematics/<int:question_id>/edit/', views.edit_mathematics_question, name='edit_mathematics_question'),


    path('chemistry/<int:question_id>/delete/', views.delete_chemistry_question, name='delete_chemistry_question'),


    # View the Exam Result
    path('exam-result/<int:result_id>/', views.exam_result, name='exam_result'),
    
    path('submit-exam/', views.submit_exam, name='submit_exam'),

    path('search-staff/', views.search_staff, name='search_staff'),
    path('delete-staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    
    path('purchases/', views.view_purchases, name='view_purchases'),
    path('remove-purchase/<int:purchase_id>/', views.remove_purchase, name='remove_purchase'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('get-packages/', views.get_packages, name='get_packages'),
    path('get-package/<int:package_id>/', views.get_package, name='get_package'),
    path('save-package/', views.save_package, name='save_package'),
    path('update-package/<int:package_id>/', views.update_package, name='update_package'),
    path('delete-package/<int:package_id>/', views.delete_package, name='delete_package'),
    path('toggle-package-status/<int:package_id>/', views.toggle_package_status, name='toggle_package_status'),
    
   path('payment/<int:package_id>/', views.payment_view, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
   path("transaction-history/",views.transaction_history,name="transaction_history")
]


