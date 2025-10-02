from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employees.models import Task
from notes.models import Note
from employees.serializers import TaskSerializer
from notes.serializers import NoteSerializer
from django.db.models import Q

class SearchAPIView(APIView):
    """
    Search across Tasks and Notes using a 'q' query parameter.
    Example: /api/search/?q=django
    """

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response({"detail": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Search tasks
        tasks = Task.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        task_data = TaskSerializer(tasks, many=True).data

        # Search notes
        notes = Note.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        note_data = NoteSerializer(notes, many=True).data

        return Response({
            "tasks": task_data,
            "notes": note_data
        }, status=status.HTTP_200_OK)
