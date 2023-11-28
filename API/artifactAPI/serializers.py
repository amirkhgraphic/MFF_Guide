from rest_framework import serializers
from apps.artifact.models import Artifact
from apps.character.models import Character


class ArtifactListSerializer(serializers.ModelSerializer):
    character_name = serializers.SerializerMethodField()

    class Meta:
        model = Artifact
        exclude = ('id', 'image', 'character')

    def get_character_name(self, obj: Artifact):
        return Character.objects.get(pk=obj.character_id).name
