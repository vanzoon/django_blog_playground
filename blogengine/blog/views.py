from django.http import Http404
from django.views.generic import View, ListView, DetailView, CreateView
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.detail import BaseDetailView

from .forms import TagForm, PostForm
from .pagination import pagination
from .utils import *

# TODO: optimize queries
# TODO: optionally rewrite self-made mixins - they are obscure for query optimization


class PostListView(ListView):
    model = Post
    paginate_by = 4
    template_name = 'blog/index.html'

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        if search_query:
            print(self.request.GET.get('search'))

            queryset = self.model.objects.filter(
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query)) \
                .select_related('author') \
                .prefetch_related('tags')
        else:
            queryset = self.model.objects.all() \
                .select_related('author') \
                .prefetch_related('tags')

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_model = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True
    permission_required = 'blog.add_post'

    def post(self, request, slug):
        form = self.form_model(request.POST)
        if form.is_valid():
            form = form.save(commit=False)





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


class TagDetail(BaseDetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'

    def get(self, request, slug):
        self.object = None
        try:
            self.object = self.model.objects.get(slug__iexact=slug)
        except self.model.DoesNotExist:
            raise Http404(f'No {self.model.__name__} matches the given query.')

        context = {
            self.model.__name__.lower(): self.object,
            'admin_obj': self.object,
        }
        return render(request, self.template_name, context=context)


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
