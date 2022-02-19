from rest_framework import serializers

from main.models import Post, CodeImage, Comment, Reply


class CodeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image',)

    def _get_image_url(self, instance): # instance -> obj-> CodeImage
        if instance.image:
            url = instance.image.url
            return 'localhost:8000' + url

    def to_representation(self, instance):
        representation = super(CodeImageSerializer, self).to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username') # это поле не обязателен для заполнения
    class Meta:
        model = Post
        fields = '__all__'
        # exclude = ('author',)

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES
        author = request.user
        post = Post.objects.create(author=author, **validated_data)
        for image in images.getlist('images'):    # чтобы получить картинку в виде списка
            CodeImage.objects.create(image=image, post= post)
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        images = request.FILES
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if images.getlist('new_images'):
            instance.images.all().delete()
            for image in images.getlist('new_images'):
                CodeImage.objects.create(image=image, post=instance)
        return instance

    # если мы хотим высветить содержимое (картины) нашего поста в виде словаря
    def to_representation(self, instance):
        representation = super().to_representation(instance)    # instance -> это объет
        representation['images '] = CodeImageSerializer(instance.images.all(), many=True).data       # >-= instance.images.all()
        action = self.context.get('action')
        if action == 'list':
            representation['replies'] = instance.replies.count()
        else:
            representation['replies'] = ReplySerializer(instance.replies.all(), many=True).data
        return representation


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Reply
        fields = "__all__"

    def create(self, validated_data):
        author = self.context.get('request').user
        reply = Reply.objects.create(author=author, **validated_data)
        return reply

    def to_representation(self, instance):
        representation = super(ReplySerializer, self).to_representation(instance)
        representation['likes'] = instance.likes.count()
        action = self.context.get('action')
        if action == 'list':
            representation['comments'] = instance.comments.count()
        else:
            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        author = self.context.get('request').user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment