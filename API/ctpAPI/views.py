from rest_framework.pagination import PageNumberPagination
from API.ctpAPI.serializers import CTPListSerializer
from rest_framework.generics import ListAPIView
from apps.ctp.models import CTP


class CTPPagination(PageNumberPagination):
    page_size = 60


class GetCTPList(ListAPIView):
    queryset = CTP.objects.all()
    serializer_class = CTPListSerializer
    pagination_class = CTPPagination


class GetCTPSearch(ListAPIView):
    queryset = CTP.objects.all()
    serializer_class = CTPListSerializer
    pagination_class = CTPPagination

    def get_queryset(self):
        key = self.request.query_params.get('Key', None)
        return CTP.objects.filter(name__iregex=f'C\.T\.P\. of .*{key}.*')