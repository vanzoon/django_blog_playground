from django.views.generic import View
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import TagForm, PostForm
from .pagination import pagination
from .utils import *

# TODO: optimize queries
# TODO: optionally rewrite self-made mixins - they are obscure for query optimization


def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)) \
            .select_related('author') \
            .prefetch_related('tags')
    else:
        posts = Post.objects.all() \
            .select_related('author') \
            .prefetch_related('tags')

    context = pagination(
        posts, requested_page=request.GET.get('page', 1)
    )
    return render(request, 'blog/index.html', context=context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True
    permission_required = 'blog.add_post'


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    form_model = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True
    permission_required = 'blog.update_post'


class PostDelete(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True
    permission_required = 'blog.delete_post'


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, PermissionRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    form_model = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True
    permission_required = 'blog.update_tag'


class TagDelete(LoginRequiredMixin, PermissionRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True
    permission_required = 'blog.delete_tag'


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class Favorites:
    pass
