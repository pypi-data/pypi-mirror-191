import logging
import unittest
from puf.model import class_to_table
from puf.model import IntField, DateField, Model


logging.basicConfig(level=logging.DEBUG)


class TestUtils(unittest.TestCase):
    def test_class_to_table(self):
        self.assertEqual("user_profile", class_to_table("UserProfile"))
        self.assertEqual("a1_b2", class_to_table("a1B2"))
        self.assertEqual("a1_b2", class_to_table("A1B2"))


class TestModel(unittest.TestCase):
    def test_fields(self):
        class User(Model, table="user"):
            id = IntField()
            register_at = DateField("created_at")

        self.assertIsNotNone(User._opts)
        self.assertIsNotNone(User.objects)
        self.assertEqual(User.id.name, "id")
        self.assertEqual(User.register_at.name, "created_at")
        print(User._opts)
        print(User.objects.get(1))
