from django.contrib.auth.models import User
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import TagForm, PostForm  # CommentForm
from .models import Post, Tag, Comment

# TODO: check queries for optimization (similar queries in PostDetail,
#  unnecessary in TagDetail)
# TODO: implement view for comments too..


class ProfileView(generic.TemplateView):
    model = User
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
            queryset = self.model.objects.get_queryset()
        return queryset


class PostDetailView(generic.DetailView):
    model = Post
    # form_class = CommentForm
    template_name = 'blog/post_detail.html'
    # success_url = 'post_detail_url'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
            'comments': Comment.objects.comments_for_post(self.object),
            # 'comment_form': CommentForm(initial={'post': self.object})
            # 'new_comment': True,
        })
        return context

# class CommentFormView(B, generic.FormView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'blog/post_detail.html'
#
# #
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         new_comment = self.get_form()
#
#         if new_comment.is_valid():
#             new_comment.save(commit=False)
#             new_comment.post = self.post
#             new_comment.save()
#         else:
#             return self.form_invalid(new_comment)
#         #
        # kwargs.update({
        #     'new_comment': new_comment
        # })
        # return self.get(self, request, *args, **kwargs)
        # return super(CommentFormView, self).post(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create_form.html'
    permission_required = 'blog.add_post'


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update_form.html'
    permission_required = 'blog.update_post'


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
