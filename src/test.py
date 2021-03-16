import unittest
import encryption

class TestSum(unittest.TestCase):

    def test_salt(self):
        self.assertEqual(len(encryption.generateSalt()), 16)

    def test_encryption_simple(self):

        ciphertext = encryption.encrypt("i hate mushrooms but broccooli is cool", "super_bad_password")
        self.assertEqual(type(ciphertext), type("string"))

        plaintext = encryption.decrypt(ciphertext, "super_bad_password")
        self.assertEqual(plaintext, "i hate mushrooms but broccooli is cool")


    def test_encryption_hard(self):
        ciphertext = encryption.encrypt("Co#mPl@x Ex()mP1e", "super_bad_password")
        plaintext = encryption.decrypt(ciphertext, "super_bad_password")
        self.assertEqual(plaintext, "Co#mPl@x Ex()mP1e")


if __name__ == '__main__':
    unittest.main()
