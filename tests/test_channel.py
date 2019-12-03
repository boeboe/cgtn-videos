"""Package to test ChannelPrograms """
import unittest

from cgtn_videos.channel import ChannelProgram, ChannelParser, Channel

class ChannelProgramTest(unittest.TestCase):
    """Class to test ChannelProgram """

    def test_constructor(self):
        '''Test function '''
        channel_program = ChannelProgram(epg_id="A", channel_id="B", video_url="C", name="D", start="E", end="F")
        self.assertEqual(channel_program.epg_id, "A")
        self.assertEqual(channel_program.channel_id, "B")
        self.assertEqual(channel_program.video_url, "C")
        self.assertEqual(channel_program.name, "D")
        self.assertEqual(channel_program.start, "E")
        self.assertEqual(channel_program.end, "F")

class ChannelParserTest(unittest.TestCase):
    """Class to test ChannelParser """

    def test_parse_current_live(self):
        '''Test function '''
        parser = ChannelParser()

        live_program = parser.parse_current_live(Channel.ENGLISH)
        self.assertIsNotNone(live_program.epg_id)
        self.assertIsNotNone(live_program.channel_id)
        self.assertIsNotNone(live_program.video_url)
        self.assertIsNotNone(live_program.name)
        self.assertIsNotNone(live_program.start)
        self.assertIsNotNone(live_program.end)
        self.assertTrue(live_program.epg_id)
        self.assertTrue(live_program.channel_id)
        self.assertTrue(live_program.video_url)
        self.assertTrue(live_program.name)
        self.assertTrue(live_program.start)
        self.assertTrue(live_program.end)

    def test_parse_history_count(self):
        '''Test function '''
        parser = ChannelParser()
        program_count = parser.parse_history_count(Channel.ARABIC)
        self.assertTrue(program_count > 0)

    def test_parse_history_by_month(self):
        '''Test function '''
        parser = ChannelParser()

        channel_programs = parser.parse_history_by_month(Channel.SPANISH, year=2019, month=1, day=1)
        self.assertTrue(channel_programs)
        for channel_program in channel_programs:
            self.assertIsNotNone(channel_program.epg_id)
            self.assertIsNotNone(channel_program.channel_id)
            self.assertIsNotNone(channel_program.video_url)
            self.assertIsNotNone(channel_program.name)
            self.assertIsNotNone(channel_program.start)
            self.assertIsNotNone(channel_program.end)
            self.assertTrue(channel_program.epg_id)
            self.assertTrue(channel_program.channel_id)
            self.assertTrue(channel_program.video_url)
            self.assertTrue(channel_program.name)
            self.assertTrue(channel_program.start)
            self.assertTrue(channel_program.end)

    def test_parse_history_from_now(self):
        '''Test function '''
        parser = ChannelParser()

        channel_programs = parser.parse_history_from_now(Channel.RUSSIAN, hours=3)
        self.assertTrue(channel_programs)
        for channel_program in channel_programs:
            self.assertIsNotNone(channel_program.epg_id)
            self.assertIsNotNone(channel_program.channel_id)
            self.assertIsNotNone(channel_program.video_url)
            self.assertIsNotNone(channel_program.name)
            self.assertIsNotNone(channel_program.start)
            self.assertIsNotNone(channel_program.end)
            self.assertTrue(channel_program.epg_id)
            self.assertTrue(channel_program.channel_id)
            self.assertTrue(channel_program.video_url)
            self.assertTrue(channel_program.name)
            self.assertTrue(channel_program.start)
            self.assertTrue(channel_program.end)

if __name__ == '__main__':
    unittest.main()
