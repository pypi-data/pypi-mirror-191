from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from blogorama.views.blog import PostDetailView

User = get_user_model()


class AnnonymousUserViewTests(TestCase):
    fixtures = [
        "blogorama.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_post_detail_page(self):
        response = self.client.get(reverse("blogorama_post", kwargs={"slug": "bacon-galore"}))
        self.assertEqual(response.status_code, 200)

    def test_post_list_page(self):
        response = self.client.get(reverse("blogorama_post-list"))
        self.assertEqual(response.status_code, 200)

    def test_post_create_page(self):
        """Make sure by default Annonymous user does not have access to the creation page"""
        target_url = reverse("blogorama_post-create")

        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("account_login") + "?next=" + target_url)

    def test_post_update_page(self):
        """Make sure by default Annonymous user does not have access to the creation page"""
        target_url = reverse("blogorama_post-update", kwargs={"slug": "bacon-galore"})
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("account_login") + "?next=" + target_url)


# TODO: Test user permissions and make sure they have the correct access
class AuthenticatedUserViewTests(TestCase):
    fixtures = [
        "blogorama.json",
    ]

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

    def test_user_post_detail_page_can_edit(self):
        """Confirm the edit button is present for this user"""
        target_url = reverse("blogorama_post-update", kwargs={"slug": "bacon-galore"})
        request = self.factory.get(target_url)
        request.user = self.user1
        response = PostDetailView.as_view()(request, slug="bacon-galore")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Post")

    def test_user_post_detail_page_can_not_edit(self):
        """Confirm the edit button is present for this user"""
        target_url = reverse("blogorama_post-update", kwargs={"slug": "bacon-galore"})
        request = self.factory.get(target_url)
        request.user = self.user2
        response = PostDetailView.as_view()(request, slug="bacon-galore")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Edit Post")


# TODO: Test cross-site posting of Posts


# TODO: Test comments

# TODO: Test Banned user permissions
