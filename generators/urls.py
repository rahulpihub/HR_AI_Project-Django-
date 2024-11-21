# generators/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bio/', views.bio_generator, name='bio_generator'),
    path('interview/', views.interview_answer, name='interview_answer'),
    path('interview-question-generator/', views.interview_question_generator, name='interview_question_generator'),
    path('job-responsibilities/', views.job_responsibilities_generator, name='job_responsibilities_generator'),
    path('job-description/', views.job_description_generator, name='job_description_generator'),
    path('job-title-generator/', views.job_title_generator, name='job_title_generator'),
    path('letter_of_recommendation/', views.letter_of_recommendation, name='letter_of_recommendation'),
    path('mission-statement/', views.mission_statement_generator, name='mission_statement_generator'),
    path('offer-letter/', views.offer_letter_generator, name='offer_letter_generator'),
    path('job-qualification/', views.job_qualification_generator, name='job_qualification_generator'),
    path('skills-generator/', views.skills_generator, name='skills_generator'),
    path('vision-statement-generator/', views.vision_statement_generator, name='vision_statement_generator'),
    path('speech_writer/', views.speech_writer, name='speech_writer'),
    path("character-reference/", views.generate_character_reference, name="character_reference"),
    path("linkedin-bio-generator/", views.linkedin_bio_generator, name="linkedin_bio_generator"),
    path("performance-review/", views.performance_review_view, name="performance_review"),
    path("interview-feedback/", views.interview_feedback_view, name="interview_feedback"),
    path("linkedin-request/", views.linkedin_request_view, name="linkedin_request"),
    path("resume-bullet-generator", views.resume_bullet_generator, name="resume_bullet_generator"),
    path("peer-review-generator", views.peer_review_generator, name="peer_review_generator"),
    path("sop-generator", views.sop_generator, name="sop_generator"),
    path("linkedin-post-generator/", views.linkedin_post_generator, name="linkedin_post_generator"),
    path("job-summary/", views.job_summary_generator, name="job_summary_generator"),
    path("okr-generator/", views.okr_generator, name="okr_generator"),
    path("kpi-generator/", views.kpi_generator, name="kpi_generator"),
    path("schedule-view/", views.schedule_view, name="schedule_view"),
    path('policy-generator/', views.policy_generator, name='policy_generator'),
    
      
]



