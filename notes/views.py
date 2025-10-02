from rest_framework import viewsets, filters
from .models import Note, Tag
from .serializers import NoteSerializer, TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def get_queryset(self):
        queryset = Note.objects.all()
        tag_name = self.request.query_params.get("tag")
        if tag_name:
            queryset = queryset.filter(tags__name__iexact=tag_name)
        return queryset
