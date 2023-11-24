from rest_framework import serializers
from apps.character.models import Character


class CharacterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = ('id', 'name', 'uniform', 'type', 'rotation')


class CharacterDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        exclude = ('id', 'image_url')
