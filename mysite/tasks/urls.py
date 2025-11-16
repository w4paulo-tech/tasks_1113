from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('workers/', views.CustomUserListView.as_view(), name='workers'),
    path('workers/<int:pk>', views.CustomUserUpdateView.as_view(), name='worker'),
    path('workers/<int:worker_pk>/task/create/', views.UzduotisInstanceCreateView.as_view(), name='uzduotis_create'),
    path('workers/<int:worker_pk>/task/<int:pk>/update/', views.UzduotisInstanceUpdateView.as_view(), name='uzduotis_update'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('tasks/', views.UzduotisListView.as_view(), name='uzduotys'),
    path('tasks/<int:pk>/', views.UzduotisInstanceListView.as_view(), name='uzduotys_inst'),

]