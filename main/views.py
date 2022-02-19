from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from .models import *
from .serializers import PostSerializer, ReplySerializer, CommentSerializer
from .permissions import IsAuthorPost


class PermissionMixin:

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPost]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]


class PostViewSet(PermissionMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    # поиск
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(Q(title__icontains=query) | Q(description__icontains=query))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context
    #
    @action(detail=True, methods=['get'])   # detail=True будет ждать slug или pk или id
    def like(self, request, pk):
        user = request.user
        reply = get_object_or_404(Reply, pk=pk)
        if user.is_authenticated:
            if user in reply.likes.all():
                reply.likes.remove(user)
                message = 'Unliked!'
            else:
                reply.likes.add(user)
                message = 'Liked!'
        context = {'Status': message}
        return Response(context, status=200)


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

