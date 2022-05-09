from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import generic

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin, UserPassesTestMixin
)

from .forms import TagForm, PostForm, CommentForm
from .models import Post, Tag, Comment

# TODO: check queries for optimization (similar queries in PostDetail,
#  unnecessary in TagDetail)
# TODO: implement view for comments too..
# NOTE: that is happening with permissions here...


class ProfileView(LoginRequiredMixin, generic.TemplateView):
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
    template_name = 'blog/post_detail.html'

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


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                     generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create_form.html'
    permission_required = 'blog.add_post'
    redirect_field_name = 'accounts/login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# ... maybe it would be better to implement in get_from_kwargs?
    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        if 'publish' in request.POST:
            request.POST['status'] = 1
        if 'draft' in request.POST:
            request.POST['status'] = 0
        return super(PostCreateView, self).post(request, *kwargs)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                     UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update_form.html'
    permission_required = 'blog.update_post'

    def test_func(self):
        print(self.get_object())
        return bool(self.get_object().author == self.request.user)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                     UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete_form.html'
    permission_required = 'blog.delete_post'

    def get_success_url(self):
        return reverse('posts_list_url')

    def test_func(self):
        return bool(self.get_object().author == self.request.user)


class TagDetailView(generic.DetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = TagForm
    template_name = 'blog/tag_create.html'


class TagUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                    generic.UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'blog/tag_update_form.html'
    permission_required = 'blog.update_tag'
    raise_exception = True


class TagDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                    generic.DeleteView):
    model = Tag
    template_name = 'blog/tag_delete_form.html'
    permission_required = 'blog.delete_tag'

    def get_success_url(self):
        return reverse('tags_list_url')


class TagsListView(generic.ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'blog/tags_list.html'


class FavoritesView:
    pass
