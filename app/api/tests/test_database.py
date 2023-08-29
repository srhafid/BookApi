# Unit tests
import unittest
from app.api.models.model import Urls, User


class TestModels(unittest.TestCase):
    def test_user_model(self):
        user = User(username="john", password="secret", role="user")
        self.assertEqual(user.username, "john")
        self.assertEqual(user.password, "secret")
        self.assertEqual(user.role, "user")

    def test_urls_model(self):
        url = Urls(
            title="Example URL",
            description="An example URL",
            author="John Doe",
            rating=5,
        )
        self.assertEqual(url.title, "Example URL")
        self.assertEqual(url.description, "An example URL")
        self.assertEqual(url.author, "John Doe")
        self.assertEqual(url.rating, 5)



