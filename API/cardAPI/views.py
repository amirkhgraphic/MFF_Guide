from API.cardAPI.serializers import CardListSerializer
from rest_framework.generics import ListAPIView
from apps.card.models import Card


class GetCardList(ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardListSerializer


class GetCardSearch(ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardListSerializer

    def get_queryset(self):
        key = self.request.query_params.get('Key', None)
        return Card.objects.filter(name__icontains=key)
