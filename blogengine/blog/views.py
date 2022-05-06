from django.contrib.auth import get_user_model
from django.db.models import Count, When
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from pycparser.c_ast import Case

from .forms import TagForm, PostForm, CommentForm
from .models import Post, Tag, Comment

# TODO: check queries for optimization (similar queries in PostDetail,
#  unnecessary in TagDetail)
# TODO: implement view for comments too..
# NOTE: that is happening with permissions here...


class ProfileView(generic.TemplateView):
    model = get_user_model()
    context_object_name = 'user'
    template_name = 'registration/profile.html'


class PostListView(generic.ListView):
    model = Post
    paginate_by = 4
    context_object_name = 'posts'
    template_name = 'blog/posts_list.html'

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = self.model.objects.search(search_query)
        else:
            queryset = self.model.objects.get_published()
        return queryset


class PostDetailView(generic.DetailView):
    model = Post
    # form_class = CommentForm
    template_name = 'blog/post_detail.html'
    # success_url = 'post_detail_url'

    # def get_queryset(self):
    #     queryset = super(PostDetailView, self).get_queryset().annotate(
    #         bookmarked=Count(Case(When(userpostrelation__in_bookmarks=True, then=1)))
    #     )
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
            'comments': Comment.objects.comments_for_post(self.object),
        })
        if self.request.user.is_authenticated:
            context.update({
                'comment_form': CommentForm(instance=self.request.user),
                'new_comment': True,
            })
        return context


class CommentFormView(generic.FormView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create_form.html'
    permission_required = 'blog.add_post'


# ... maybe it would be better to implement in get_from_kwargs?
    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        if 'publish' in request.POST:
            request.POST['status'] = 1
        if 'draft' in request.POST:
            request.POST['status'] = 0
        return super(PostCreateView, self).post(request, *kwargs)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update_form.html'
    permission_required = 'blog.update_post'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete_form.html'
    success_url = 'posts_list_url'
    permission_required = 'blog.delete_post'


class TagDetailView(generic.DetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = TagForm
    template_name = 'blog/tag_create.html'


class TagUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'blog/tag_update_form.html'
    permission_required = 'blog.update_tag'
    raise_exception = True


class TagDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = 'tags_list_url'
    template_name = 'blog/tag_delete_form.html'
    permission_required = 'blog.delete_tag'


class TagsListView(generic.ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'blog/tags_list.html'

class FavoritesView:
    pass
