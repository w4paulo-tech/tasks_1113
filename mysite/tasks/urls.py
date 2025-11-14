from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('workers/', views.CustomUserListView.as_view(), name='workers'),
    path('workers/<int:pk>', views.CustomUserDetailView.as_view(), name='worker'),
    path('uzduotis/create/', views.UzduotisInstanceCreateView.as_view(), name='uzduotis_create'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]