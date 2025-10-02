from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Note, Tag

class NotesTagsAPITestCase(APITestCase):

    def setUp(self):
        # Create some tags
        self.tag1 = Tag.objects.create(name="work")
        self.tag2 = Tag.objects.create(name="django")

        # Create a note with tags
        self.note = Note.objects.create(
            title="Initial Note",
            content="This is a test note"
        )
        self.note.tags.add(self.tag1, self.tag2)

    # ----------------- Tag Tests -----------------
    def test_create_tag(self):
        url = reverse("tag-list")
        data = {"name": "urgent"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tag.objects.filter(name="urgent").exists())

    # ----------------- Note Tests -----------------
    def test_create_note_with_tags(self):
        url = reverse("note-list")
        data = {
            "title": "New Note",
            "content": "Note with tags",
            "tag_names": ["work", "newtag"]  # 'newtag' will be auto-created
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        note = Note.objects.get(title="New Note")
        self.assertEqual(note.tags.count(), 2)
        self.assertTrue(Tag.objects.filter(name="newtag").exists())

    def test_list_notes_filter_by_tag(self):
        url = reverse("note-list") + "?tag=django"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("django" in [t["name"] for t in note["tags"]] for note in response.data))

    def test_list_notes_filter_by_search_keyword(self):
        url = reverse("note-list") + "?search=test"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("test" in note["title"].lower() or "test" in note["content"].lower() for note in response.data))

    def test_update_note_title_content_tags(self):
        url = reverse("note-detail", args=[str(self.note.id)])
        data = {
            "title": "Updated Note",
            "content": "Updated content",
            "tag_names": ["updated", "django"]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Note")
        self.assertEqual(self.note.tags.count(), 2)
        self.assertTrue(Tag.objects.filter(name="updated").exists())

    def test_delete_note(self):
        url = reverse("note-detail", args=[str(self.note.id)])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
