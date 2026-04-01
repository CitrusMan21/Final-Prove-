from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Node:
    song: str
    next: Optional["Node"] = None


class Playlist:
    """Playlist backed by a custom singly linked list."""

    def __init__(self, songs: Optional[Iterable[str]] = None) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.length = 0

        if songs:
            for song in songs:
                self.add_song(song)

    def add_song(self, song: str) -> None:
        if not song:
            raise ValueError("song name must not be empty")

        node = Node(song=song)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            assert self.tail is not None
            self.tail.next = node
            self.tail = node
        self.length += 1

    def remove_song(self, song: str) -> bool:
        previous: Optional[Node] = None
        current = self.head

        while current is not None:
            if current.song == song:
                self._unlink_node(previous, current)
                return True
            previous, current = current, current.next
        return False

    def play_next(self) -> Optional[str]:
        if self.head is None:
            return None

        song = self.head.song
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.length -= 1
        return song

    def move_song_up(self, song: str) -> bool:
        if self.head is None or self.head.song == song:
            return False

        before_prev: Optional[Node] = None
        prev = self.head
        current = self.head.next

        while current is not None:
            if current.song == song:
                # Swap prev and current node positions.
                prev.next = current.next
                current.next = prev
                if before_prev is None:
                    self.head = current
                else:
                    before_prev.next = current
                if prev.next is None:
                    self.tail = prev
                return True
            before_prev, prev, current = prev, current, current.next
        return False

    def move_song_down(self, song: str) -> bool:
        if self.head is None or self.head.next is None:
            return False

        previous: Optional[Node] = None
        current = self.head

        while current is not None and current.next is not None:
            nxt = current.next
            if current.song == song:
                # Swap current and nxt node positions.
                current.next = nxt.next
                nxt.next = current
                if previous is None:
                    self.head = nxt
                else:
                    previous.next = nxt
                if current.next is None:
                    self.tail = current
                return True
            previous, current = current, current.next
        return False

    def show_playlist(self) -> list[str]:
        songs: list[str] = []
        current = self.head
        while current is not None:
            songs.append(current.song)
            current = current.next
        return songs

    def _unlink_node(self, previous: Optional[Node], current: Node) -> None:
        if previous is None:
            self.head = current.next
        else:
            previous.next = current.next

        if current.next is None:
            self.tail = previous

        self.length -= 1
