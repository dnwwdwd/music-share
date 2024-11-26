from django.urls import path

from . import views

urlpatterns = [
    path('api/singer/', views.singer_list),
    path('api/singer/add', views.singer_add),
    path('api/singer/<int:id>', views.singer_detail),
    path('api/singer/list/id', views.singer_id_list),
    path('api/singer/update/<int:id>', views.singer_update),
    path('api/singer/delete/<int:id>', views.singer_delete),
    path('api/music/', views.music_list),
    path('api/hot/music/', views.hot_music_list),
    path('api/music/<int:id>', views.music_detail),
    path('api/music/update/<int:id>', views.music_update),
    path('api/music/delete/<int:id>', views.music_delete),
    path('api/music/upload', views.music_upload),
    path('api/music/add', views.music_add),
    path('api/user/login', views.user_login),
    path('api/user/register', views.user_register),
    path('api/user/current', views.user_current),
    path('api/user/logout', views.user_logout),
    path('api/user/update', views.user_update),
    path('api/user/list', views.user_list),
    path('api/user/delete/<int:id>', views.user_delete),
    path('api/user/add', views.user_add),
    path('api/music_star/list', views.music_star_list),
    path('api/music_star/add', views.music_star_add),
    path('api/music_star/delete', views.music_star_delete),
    path('api/music_starred', views.music_starred),

]