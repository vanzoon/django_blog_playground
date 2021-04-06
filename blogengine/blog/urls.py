from django.conf.urls.static import static

from django.urls import path

from .views import *


urlpatterns = [
    path('', PostListView.as_view(), name='posts_list_url'),
    path('post/create/', PostCreate.as_view(), name='post_create_url'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('post/<slug:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('post/<slug:slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<slug:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<slug:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<slug:slug>/delete/', TagDelete.as_view(), name='tag_delete_url')
]
