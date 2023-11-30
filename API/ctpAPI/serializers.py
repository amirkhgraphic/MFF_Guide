from rest_framework import serializers
from apps.ctp.models import CTP


class CTPListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CTP
        exclude = ('id', 'image')
