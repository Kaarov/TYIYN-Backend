from rest_framework import serializers

from .models import CardModel


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardModel
        exclude = ('id', 'user')


class CardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardModel
        exclude = ('user',)
