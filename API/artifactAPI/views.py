from django.db.models import Q
from API.artifactAPI.serializers import ArtifactListSerializer
from rest_framework.generics import ListAPIView
from apps.artifact.models import Artifact


def get_queryset():
    qs = Artifact.objects.all().order_by('character_id__name')
    names = []
    result = []
    for item in qs:
        if item.name in names:
            continue
        result.append(item)
        names.append(item.name)
    return result


class GetArtifactList(ListAPIView):
    queryset = get_queryset()
    serializer_class = ArtifactListSerializer


class GetArtifactSearch(ListAPIView):
    queryset = get_queryset()
    serializer_class = ArtifactListSerializer

    def get_queryset(self):
        def distinct(instances):
            names, result = [], []
            for item in instances:
                if item.name in names:
                    continue
                names.append(item.name)
                result.append(item)
            return result

        key = self.request.query_params.get('Key', None)
        return distinct(Artifact.objects.filter(Q(name__icontains=key) | Q(character__name__icontains=key)))