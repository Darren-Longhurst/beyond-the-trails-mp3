from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('blog', views.PostList.as_view(), name='blog'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path(
        'post/<slug:slug>/edit_comment/<int:comment_id>/',
        views.comment_edit,
        name='comment_edit'
    ),
    path(
        'post/<slug:slug>/delete_comment/<int:comment_id>/',
        views.comment_delete,
        name='comment_delete'
    ),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('post/<slug:slug>/like/', views.post_like, name='post_like'),
# --- Exception error message testing ---
    path(
        '403-test/',
        views.Force403View.as_view(),
        name='403-test'
    ),
    path(
        '404-test/',
        views.Force404View.as_view(),
        name='404-test'
    ),
    path(
        '405-test/',
        views.Force405View.as_view(),
        name='405-test'
    ),
    path(
        '500-test/',
        views.Force500View.as_view(),
        name='500-test'
    ),
]
