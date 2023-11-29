from API.cardAPI.serializers import CardListSerializer
from rest_framework.generics import ListAPIView
from apps.card.models import Card


class GetCardList(ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardListSerializer

