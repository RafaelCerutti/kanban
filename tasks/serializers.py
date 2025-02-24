from rest_framework import serializers
from tasks import models

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Board
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']

class StatusSerializer(serializers.ModelSerializer):
    board = serializers.SlugRelatedField(slug_field='title', queryset=models.Board.objects.all())

    class Meta:
        model = models.Status
        fields = '__all__'
        read_only_fields = ['created_at']

class CardSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field='title', queryset=models.Status.objects.all())
    board = serializers.SlugRelatedField(slug_field='title', queryset=models.Board.objects.all())

    class Meta:
        model = models.Card 
        fields = '__all__'
        read_only_fields = ['created_at']

