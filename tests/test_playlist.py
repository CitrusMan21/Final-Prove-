import unittest

from playlist import Playlist


class PlaylistTests(unittest.TestCase):
    def test_add_song_appends_to_end(self):
        playlist = Playlist()
        playlist.add_song("Yellow Submarine")
        playlist.add_song("Hey Jude")

        self.assertEqual(["Yellow Submarine", "Hey Jude"], playlist.show_playlist())

    def test_add_song_rejects_empty_name(self):
        playlist = Playlist()

        with self.assertRaises(ValueError):
            playlist.add_song("")

    def test_remove_song_returns_true_when_removed(self):
        playlist = Playlist(["One", "Two", "Three"])

        removed = playlist.remove_song("Two")

        self.assertTrue(removed)
        self.assertEqual(["One", "Three"], playlist.show_playlist())

    def test_remove_song_returns_false_when_missing(self):
        playlist = Playlist(["One"])

        removed = playlist.remove_song("Two")

        self.assertFalse(removed)
        self.assertEqual(["One"], playlist.show_playlist())

    def test_remove_song_updates_head_and_tail_correctly(self):
        playlist = Playlist(["A", "B", "C"])

        self.assertTrue(playlist.remove_song("A"))
        self.assertEqual(["B", "C"], playlist.show_playlist())

        self.assertTrue(playlist.remove_song("C"))
        self.assertEqual(["B"], playlist.show_playlist())

        self.assertTrue(playlist.remove_song("B"))
        self.assertEqual([], playlist.show_playlist())
        self.assertIsNone(playlist.head)
        self.assertIsNone(playlist.tail)

    def test_play_next_returns_and_removes_first_song(self):
        playlist = Playlist(["First", "Second"])

        next_song = playlist.play_next()

        self.assertEqual("First", next_song)
        self.assertEqual(["Second"], playlist.show_playlist())

    def test_play_next_returns_none_for_empty_playlist(self):
        playlist = Playlist()

        self.assertIsNone(playlist.play_next())

    def test_move_song_up_swaps_song_with_previous_song(self):
        playlist = Playlist(["A", "B", "C"])

        moved = playlist.move_song_up("C")

        self.assertTrue(moved)
        self.assertEqual(["A", "C", "B"], playlist.show_playlist())

    def test_move_song_up_returns_false_for_first_song(self):
        playlist = Playlist(["A", "B"])

        moved = playlist.move_song_up("A")

        self.assertFalse(moved)
        self.assertEqual(["A", "B"], playlist.show_playlist())

    def test_move_song_down_swaps_song_with_next_song(self):
        playlist = Playlist(["A", "B", "C"])

        moved = playlist.move_song_down("A")

        self.assertTrue(moved)
        self.assertEqual(["B", "A", "C"], playlist.show_playlist())

    def test_move_song_down_returns_false_for_last_song(self):
        playlist = Playlist(["A", "B"])

        moved = playlist.move_song_down("B")

        self.assertFalse(moved)
        self.assertEqual(["A", "B"], playlist.show_playlist())

    def test_show_playlist_returns_copy(self):
        playlist = Playlist(["A", "B"])

        songs = playlist.show_playlist()
        songs.append("C")

        self.assertEqual(["A", "B"], playlist.show_playlist())


if __name__ == "__main__":
    unittest.main()
