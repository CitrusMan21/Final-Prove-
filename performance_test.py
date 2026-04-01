from __future__ import annotations

import statistics
import time
from collections import deque
from typing import Callable

from playlist import Playlist

SMALL_SIZE = 10
MEDIUM_SIZE = 1_000
LARGE_SIZE = 10_000
RUNS = 20


class ListPlaylist:
    """Small baseline implementation using Python list for benchmark comparison."""

    def __init__(self, songs: list[str]) -> None:
        self.songs = list(songs)

    def add_song(self, song: str) -> None:
        self.songs.append(song)

    def remove_song(self, song: str) -> bool:
        try:
            self.songs.remove(song)
            return True
        except ValueError:
            return False

    def remove_first(self) -> str | None:
        if not self.songs:
            return None
        return self.songs.pop(0)

    def insert_middle(self, song: str) -> None:
        self.songs.insert(len(self.songs) // 2, song)


class DequePlaylist:
    """Utility baseline to show front-removal behavior with deque."""

    def __init__(self, songs: list[str]) -> None:
        self.songs = deque(songs)

    def remove_first(self) -> str | None:
        if not self.songs:
            return None
        return self.songs.popleft()


def benchmark_mutation(setup: Callable[[], object], mutate: Callable[[object], None]) -> float:
    """Benchmark only the operation cost; setup is excluded from the timer."""
    durations = []
    for _ in range(RUNS):
        structure = setup()
        start = time.perf_counter()
        mutate(structure)
        durations.append(time.perf_counter() - start)
    return statistics.mean(durations)


def seed_songs(size: int) -> list[str]:
    return [f"Song {index}" for index in range(size)]


def run() -> None:
    for size in (SMALL_SIZE, MEDIUM_SIZE, LARGE_SIZE):
        songs = seed_songs(size)
        middle_song = f"Song {size // 2}"

        linked_add_end = benchmark_mutation(lambda: Playlist(songs), lambda p: p.add_song("New Song"))
        list_add_end = benchmark_mutation(lambda: ListPlaylist(songs), lambda p: p.add_song("New Song"))

        linked_remove_mid = benchmark_mutation(
            lambda: Playlist(songs), lambda p: p.remove_song(middle_song)
        )
        list_remove_mid = benchmark_mutation(
            lambda: ListPlaylist(songs), lambda p: p.remove_song(middle_song)
        )

        linked_remove_front = benchmark_mutation(lambda: Playlist(songs), lambda p: p.play_next())
        list_remove_front = benchmark_mutation(lambda: ListPlaylist(songs), lambda p: p.remove_first())
        deque_remove_front = benchmark_mutation(lambda: DequePlaylist(songs), lambda p: p.remove_first())

        linked_move_down = benchmark_mutation(
            lambda: Playlist(songs), lambda p: p.move_song_down(middle_song)
        )
        list_insert_middle = benchmark_mutation(
            lambda: ListPlaylist(songs), lambda p: p.insert_middle("Inserted Song")
        )

        print(f"Playlist size: {size}")
        print(f"  add_end                linked={linked_add_end:.8f}s   list={list_add_end:.8f}s")
        print(f"  remove_middle          linked={linked_remove_mid:.8f}s   list={list_remove_mid:.8f}s")
        print(
            "  remove_front           "
            f"linked={linked_remove_front:.8f}s   list={list_remove_front:.8f}s   deque={deque_remove_front:.8f}s"
        )
        print(
            f"  middle_position_edit   linked={linked_move_down:.8f}s   list={list_insert_middle:.8f}s"
        )
        print()


if __name__ == "__main__":
    run()
