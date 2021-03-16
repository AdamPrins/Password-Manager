import unittest
import encryption

class TestSum(unittest.TestCase):

    def test_salt(self):
        self.assertEqual(len(encryption.generateSalt()), 16)

    def test_encryption(self):

        ciphertext = encryption.encrypt("i hate mushrooms but broccooli is cool", "super_bad_password")
        self.assertEqual(type(ciphertext), type(b'bytes'))

        plaintext = encryption.decrypt(ciphertext, "super_bad_password")
        self.assertEqual(plaintext, "i hate mushrooms but broccooli is cool")

if __name__ == '__main__':
    unittest.main()
