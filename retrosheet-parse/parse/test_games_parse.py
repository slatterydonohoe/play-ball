from unittest import TestCase
from games_parse import GamesParse

file_path = '../test_files/2018ANA.EVA'


class TestGamesParse(TestCase):
    def test_ANA20180402(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804020")
        self.assertEqual(("CLE", "ANA", 6, 27), (visitor, home, hits, outs))

    def test_ANA20180403(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804030")
        self.assertEqual(("CLE", "ANA", 13, 24), (visitor, home, hits, outs))

    def test_ANA20180404(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804040")
        self.assertEqual(("CLE", "ANA", 6, 37), (visitor, home, hits, outs))

    def test_ANA20180406(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804060")
        self.assertEqual(("OAK", "ANA", 14, 24), (visitor, home, hits, outs))

    def test_ANA20180407(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804070")
        self.assertEqual(("OAK", "ANA", 7, 27), (visitor, home, hits, outs))

    def test_ANA20180408(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804080")
        self.assertEqual(("OAK", "ANA", 7, 24), (visitor, home, hits, outs))

    def test_ANA20180417(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804170")
        self.assertEqual(("BOS", "ANA", 4, 27), (visitor, home, hits, outs))

    def test_ANA20180418(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804180")
        self.assertEqual(("BOS", "ANA", 6, 27), (visitor, home, hits, outs))

    def test_ANA20180419(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804190")
        self.assertEqual(("BOS", "ANA", 4, 27), (visitor, home, hits, outs))

    def test_ANA20180420(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804200")
        self.assertEqual(("SFN", "ANA", 5, 27), (visitor, home, hits, outs))

    def test_ANA20180421(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804210")
        self.assertEqual(("SFN", "ANA", 6, 24), (visitor, home, hits, outs))

    def test_ANA20180422(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804220")
        self.assertEqual(("SFN", "ANA", 6, 27), (visitor, home, hits, outs))

    def test_ANA20180427(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201804270")
        self.assertEqual(("NYA", "ANA", 6, 30), (visitor, home, hits, outs))

    def test_ANA20180618(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, "ANA201806180")
        self.assertEqual(("ARI", "ANA", 12, 27), (visitor, home, hits, outs))

    def test_ANA20180706(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, 'ANA201807060')
        self.assertEqual(("LAN", "ANA", 5, 27), (visitor, home, hits, outs))

    def test_ANA20180812(self):
        (visitor, home, hits, outs, plays) = GamesParse.parse_file_for_game(file_path, 'ANA201808120')
        self.assertEqual(("OAK", "ANA", 11, 27), (visitor, home, hits, outs))
