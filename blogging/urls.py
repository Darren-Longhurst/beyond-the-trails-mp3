from django.urls import path, include, re_path
from blogging.views import post_list, post_detail

urlpatterns = [
    path('blog/', post_list, name='post_list'),
    re_path('post/<int:post_id>/', post_detail, name='post_detail'),
]