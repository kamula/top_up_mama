from rest_framework import serializers
from . models import BookComment


class BookCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookComment
        fields = ['id', 'comment']
