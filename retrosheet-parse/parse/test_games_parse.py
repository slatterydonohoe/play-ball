from unittest import TestCase
from games_parse import GamesParse

file_path = '../test_files/2018ANA.EVA'


class TestGamesParse(TestCase):
    def test_ANA20180402(self):
        self.assertEqual((6, 27), GamesParse.parse_file(file_path, "ANA201804020"))

    def test_ANA20180403(self):
        self.assertEqual((13, 24), GamesParse.parse_file(file_path, "ANA201804030"))

    def test_ANA20180404(self):
        self.assertEqual((6, 37), GamesParse.parse_file(file_path, "ANA201804040"))

    def test_ANA20180406(self):
        self.assertEqual((14, 24), GamesParse.parse_file(file_path, "ANA201804060"))

    def test_ANA20180407(self):
        self.assertEqual((7, 27), GamesParse.parse_file(file_path, "ANA201804070"))

    def test_ANA20180408(self):
        self.assertEqual((7, 24), GamesParse.parse_file(file_path, "ANA201804080"))

    def test_ANA20180417(self):
        self.assertEqual((4, 27), GamesParse.parse_file(file_path, "ANA201804170"))

    def test_ANA20180418(self):
        self.assertEqual((6, 27), GamesParse.parse_file(file_path, "ANA201804180"))

    def test_ANA20180419(self):
        self.assertEqual((4, 27), GamesParse.parse_file(file_path, "ANA201804190"))

    def test_ANA20180420(self):
        self.assertEqual((5, 27), GamesParse.parse_file(file_path, "ANA201804200"))

    def test_ANA20180421(self):
        self.assertEqual((6, 24), GamesParse.parse_file(file_path, "ANA201804210"))

    def test_ANA20180422(self):
        self.assertEqual((6, 27), GamesParse.parse_file(file_path, "ANA201804220"))

    # Note: test for 0427 should be 30 outs, but we're missing handling for outs caught stealing
    def test_ANA20180427(self):
        self.assertEqual((6, 29), GamesParse.parse_file(file_path, "ANA201804270"))

    def test_ANA20180812(self):
        self.assertEqual((11, 27), GamesParse.parse_file(file_path, 'ANA201808120'))
