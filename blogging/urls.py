from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_page, name='home'),
    path('blog', views.PostList.as_view(), name='blog'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit_comment/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('post/<slug:slug>/delete_comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('post/<slug:slug>/like/', views.post_like, name='post_like'),
]