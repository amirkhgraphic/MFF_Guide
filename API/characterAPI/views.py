from django.db.models import Q

from API.characterAPI.serializers import CharacterListSerializer, CharacterDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.character.models import Character


class GetCharacterList(ListAPIView):
    queryset = Character.objects.all().order_by('name', 'id')
    serializer_class = CharacterListSerializer


class GetCharacterDetail(RetrieveAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterDetailSerializer


class GetCharacterSearch(ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterListSerializer

    def get_queryset(self):
        key = self.request.query_params.get('Key', None)
        return Character.objects.filter(Q(name__icontains=key) | Q(uniform__icontains=key))
