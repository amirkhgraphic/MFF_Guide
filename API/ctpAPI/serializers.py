from rest_framework import serializers
from apps.card.models import Card


class CardListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        exclude = ('id', 'image')
