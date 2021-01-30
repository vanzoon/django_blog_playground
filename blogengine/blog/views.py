from django.views.generic import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Tag
from .forms import TagForm, PostForm
from .utils import *

def pagination(objects: 'QuerySet', requested_page, num_on_page=4) -> dict:
    paginator = Paginator(objects, num_on_page)
    page = paginator.get_page(requested_page)
    next_url = ''
    prev_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'

    return {
            'page_object': page,
            'is_paginated': page.has_other_pages(),
            'next_url': next_url,
            'prev_url': prev_url
    }


def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query)
                                   | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    context = pagination(posts,
                         requested_page=request.GET.get('page', 1))
    return render(request, 'blog/index.html', context=context)



class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    form_model = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    form_model = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})
