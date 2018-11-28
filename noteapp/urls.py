from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('login/', views.login, name='login'),
    path('new_user/', views.new_user, name="new_user"),
    path('login_check/', views.login_check, name="login_check"),
    path('signup/', views.signup, name="signup"),
    path('storenote/', views.storenote, name="storenote"),
    path('ajax/', views.ajax, name="ajax"),
    path('logout/', views.logout, name="logout")
]