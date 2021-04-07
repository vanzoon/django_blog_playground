from django.urls import path

from .views import *


urlpatterns = [
    path('', PostListView.as_view(), name='posts_list_url'),
    path('post/create/', PostCreateView.as_view(), name='post_create_url'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail_url'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update_url'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete_url'),
    path('tags/', TagsListView.as_view(), name='tags_list_url'),
    path('tag/create/', TagCreateView.as_view(), name='tag_create_url'),
    path('tag/<slug:slug>/', TagDetailView.as_view(), name='tag_detail_url'),
    path('tag/<slug:slug>/update/', TagUpdateView.as_view(), name='tag_update_url'),
    path('tag/<slug:slug>/delete/', TagDeleteView.as_view(), name='tag_delete_url')
]
