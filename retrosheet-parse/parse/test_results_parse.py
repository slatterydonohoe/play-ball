from unittest import TestCase
from games_parse import GamesParse


class TestResultsParse(TestCase):
    batter = 'player1'
    on_1b = 'player2'
    on_2b = 'player3'
    on_3b = 'player4'

    def testParseSingleWithRunnerFirstToThird(self):
        GamesParse.onBases = [self.batter, self.on_1b, '', '']
        (play, outs, baserunning_only) = GamesParse.parse_result('S76/F.1-3', 'game1', 1, self.batter, True)
        self.assertEqual(0, outs)
        self.assertFalse(baserunning_only)
        self.assertEqual('S', play.result)
        self.assertEqual(1, play.finished_H)
        self.assertEqual(3, play.finished_1B)
        self.assertListEqual(['', self.batter, '', self.on_1b], GamesParse.onBases)

    def testRoutineDoublePlay(self):
        GamesParse.onBases = [self.batter, self.on_1b, '', '']
        (play, outs, baserunning_only) = GamesParse.parse_result('64(1)3/GDP', 'game1', 1, self.batter, True)
        self.assertEqual(2, outs)
        self.assertFalse(baserunning_only)
        self.assertEqual('GDP', play.result)
        self.assertEqual(-1, play.finished_H)
        self.assertEqual(-1, play.finished_1B)
        self.assertListEqual(['', '', '', ''], GamesParse.onBases)

    def testBuntFieldersChoiceAtHome(self):
        GamesParse.onBases = [self.batter, self.on_1b, '', self.on_3b]
        (play, outs, baserunning_only) = GamesParse.parse_result('FC1/BG.3XH(12);1-2', 'game1', 1, self.batter, True)
        self.assertEqual(1, outs)
        self.assertFalse(baserunning_only)
        self.assertEqual('FC', play.result)
        self.assertEqual(1, play.finished_H)
        self.assertEqual(2, play.finished_1B)
        self.assertEqual(0, play.finished_2B)
        self.assertEqual(-1, play.finished_3B)
        self.assertListEqual(['', self.batter, self.on_1b, ''], GamesParse.onBases)

    def testStealSecond(self):
        GamesParse.onBases = [self.batter, self.on_1b, '', '']
        (play, outs, baserunning_only) = GamesParse.parse_result('SB2', 'game1', 1, self.batter, True)
        self.assertTrue(baserunning_only)
        self.assertEqual('SB', play.result)
        self.assertEqual(0, play.finished_H)
        self.assertEqual(2, play.finished_1B)
        self.assertEqual(0, play.finished_2B)
        self.assertEqual(0, play.finished_3B)
        self.assertListEqual(['', '', self.on_1b, ''], GamesParse.onBases)

    def testCaughtStealingSecond(self):
        GamesParse.onBases = [self.batter, self.on_1b, '', '']
        (play, outs, baserunning_only) = GamesParse.parse_result('CS2(24)', 'game1', 1, self.batter, True)
        self.assertEqual(1, outs)
        self.assertTrue(baserunning_only)
        self.assertEqual(0, play.finished_H)
        self.assertEqual(-1, play.finished_1B)
        self.assertEqual(0, play.finished_2B)
        self.assertEqual(0, play.finished_3B)
        self.assertListEqual(['', '', '', ''], GamesParse.onBases)

    def testStrikeoutThrowoutAtSecond(self):
        GamesParse.onBases = [self.batter, self.on_1b, '', '']
        (play, outs, baserunning_only) = GamesParse.parse_result('K+CS2(24)/DP', 'game1', 1, self.batter, True)
        self.assertEqual(2, outs)
        self.assertFalse(baserunning_only)
        self.assertEqual('K+CS', play.result)
        self.assertEqual(-1, play.finished_H)
        self.assertEqual(-1, play.finished_1B)
        self.assertEqual(0, play.finished_2B)
        self.assertEqual(0, play.finished_3B)
        self.assertListEqual(['', '', '', ''], GamesParse.onBases)

    def testStrikeoutWithError(self):
        GamesParse.onBases = [self.batter, '', self.on_2b, '']
        (play, outs, baserunning_only) = GamesParse.parse_result('K+E2/TH.B-1', 'game1', 1, self.batter, True)
        self.assertEqual(0, outs)
        self.assertFalse(baserunning_only)
        self.assertEqual('K+E', play.result)
        self.assertEqual(1, play.finished_H)
        self.assertEqual(0, play.finished_1B)
        self.assertEqual(2, play.finished_2B)
        self.assertEqual(0, play.finished_3B)
        self.assertListEqual(['', self.batter, self.on_2b, ''], GamesParse.onBases)
