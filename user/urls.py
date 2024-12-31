from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from user import views
from user.views import RegistrationView, SpeakingView, ieltsView, essentView, \
    writing_task_view, submit_response, part1View, LoginFormView, get_vocabs, readingView, part2View, part3View

urlpatterns = [
    path('', views.home_main, name='homee'),  # Asosiy sahifa
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout sahifasi
    path('register/', RegistrationView.as_view(), name='register'),
    path('login', LoginFormView.as_view(), name='login'),
    path('writing/task/<int:task_type>/', writing_task_view, name='writing_task'),
    path('user/speaking/', SpeakingView, name='speaking'),
    path('user/ielts/', ieltsView, name='ielts'),
    path('take_test/<int:topic_id>/', views.take_test, name='take_test'),
    path('take_test2/<int:topic_id>/', views.take_test2, name='take_test2'),
    path('take_test3/<int:topic_id>/', views.take_test3, name='take_test3'),
    path('upload_audio/', views.upload_audio, name='upload_audio'),
    path('submit-response/', submit_response, name='submit-response'),
    path('user/ielts/part1', part1View, name='part1'),
    path('user/ielts/part2', part2View, name='part2'),
    path('user/ielts/part3', part3View, name='part3'),
    path('user/ielts/part4', part1View, name='fulltest'),




    path('user/reading/', readingView, name='reading'),





    path('user/essential/', views.essentView, name='essential'),
    path('user/test/', views.testview, name='test_user'),
    path('get_vocabs/', views.get_vocabs, name='get_vocabs'),
    path('start_test/', views.start_test, name='start_test'),
    path('submit_test/', views.submit_test, name='submit_test'),

    # path('login/', views.register_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    # path('profile/', views.profile_view, name='profile'),
]
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
