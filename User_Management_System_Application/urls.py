from django.urls import path

from polls import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),
    path('add_user/', views.add_user, name='add_user'),
    path('users_list/', views.users_list, name='user_list'),
    path('users_list/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users_list/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users_list/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]
