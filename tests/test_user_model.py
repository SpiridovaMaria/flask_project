import unittest
from app.models import User, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        user = User()
        user.set_password = "hash"
        self.assertTrue(user.password_hash is not None)

    def test_password_no_getter(self):
        user = User()
        user.set_password = "hash"
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verify(self):
        user = User()
        user.set_password = "hash"
        self.assertTrue(user.password_verify("hash"))
        self.assertFalse(user.password_verify("has"))

    def test_salt(self):
        user = User()
        user.set_password = "hash"
        user2 = User()
        user2.set_password = "hash2"
        self.assertTrue(user.password_hash != user2.password_hash)

    def test_user_default_role(self):
        Role.insert_roles()
        user = User(user_email='test@test.com')
        user.set_password = "hash"
        self.assertTrue(user.can(Permission.ADD_TO_BASKET))
        self.assertTrue(user.can(Permission.BUY))
        self.assertTrue(user.can(Permission.REVIEW))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.ADMIN))

    def test_anonymous_role(self):
        Role.insert_roles()
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.ADD_TO_BASKET))
        self.assertFalse(user.can(Permission.BUY))
        self.assertFalse(user.can(Permission.REVIEW))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.ADMIN))
