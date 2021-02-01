from datetime import datetime

from django.db.models import Count, When, Case, Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import UpdateModelMixin

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
                                        BasePermission,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly
                                       )

from blog.models import Post, UserPostRelation
from .serializers import *
from .permissions import IsAuthorOrStaffOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().annotate(
        likes_count_annotate=
            Count(Case(When(userpostrelation__like=True, then=1))),
        rating=Avg('userpostrelation__rate')
    )
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title', 'body']
    search_fields = ['title', 'body']
    ordering_filters = ['-pub_date']

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()

    def perform_update(self, serializer):
        self.get_object().last_modify_date = datetime.now()
        serializer.save()


class UserPostRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserPostRelation.objects.all()
    serializer_class = UserPostRelationSerializer
    lookup_field = "post"

    def get_object(self):
        obj, _ = UserPostRelation.objects.get_or_create(user=self.request.user,
                                                        post_id=self.kwargs['post'])
        return obj
