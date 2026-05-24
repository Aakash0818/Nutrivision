from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('upload/', views.upload_food, name='upload_food'),
    path("result/<int:record_id>/", views.result_page, name="result_page"),


    # custom admin
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
]
