import unittest
import encryption

class TestSum(unittest.TestCase):

    def test_salt(self):
        self.assertEqual(len(encryption.generateSalt()), 16)

if __name__ == '__main__':
    unittest.main()
