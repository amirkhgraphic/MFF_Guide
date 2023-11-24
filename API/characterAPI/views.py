from API.characterAPI.serializers import CharacterListSerializer, CharacterDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.character.models import Character


class GetCharacterList(ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterListSerializer


class GetCharacterDetail(RetrieveAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterDetailSerializer
