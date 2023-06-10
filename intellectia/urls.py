from django.contrib import admin
from django.urls import path
from UserApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about/',views.about,name='payment'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login_user, name='login'),
    path('signup/',views.signup,name='signup'),
    path('upgrade/',views.upgrade,name='upgrade'),
    path('payment',views.payment,name='payment'),
    path('Intellectia/',views.intellectia,name='Intellectia'),
    path('profile/',views.profile,name='profile'),
    path('quiz/',views.quiz,name='quiz'),
    path('quizResults/',views.quizResults,name='quizResults'),
    path('dashboard/',views.dashboard,name='dashboard')
]
