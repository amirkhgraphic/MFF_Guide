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
