from django.test import TestCase
from auth.models import YankUser
import bcrypt

class YankUserTestCase(TestCase):

    def setUp(self):
        YankUser.objects.create(
            username="user", 
            password_digest="password"
        )

    def test_api_key_starts_at_none(self):
        user = YankUser.objects.get(username="user")
        self.assertEqual(user.api_key, None)
        