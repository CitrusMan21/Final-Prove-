# Week 12 Reflection: Playlist Using a Linked List

## Implementation Summary
This version uses a **custom singly linked list** (a `Node` class plus a `Playlist` class with `head` and `tail` pointers). The playlist keeps insertion order and supports the same operations from Week 11:

- `add_song(song)`
- `remove_song(song)`
- `play_next()`
- `move_song_up(song)`
- `move_song_down(song)`
- `show_playlist()`

The constructor also accepts an optional iterable of initial songs for easy testing.

## Functional Test Summary
Unit tests verify:
- adding songs and empty-song rejection
- removing existing and missing songs
- playing from non-empty and empty playlists
- moving songs up/down with boundary conditions
- list output safety (`show_playlist()` returns a fresh list)
- pointer correctness after removing head and tail nodes

## Performance Notes
### Big O analysis (linked-list version)
- `add_song(song)`: **O(1)** (append at tail using stored tail pointer)
- `remove_song(song)`: **O(n)** (linear search to find song)
- `play_next()`: **O(1)** (remove head)
- `move_song_up(song)`: **O(n)** (linear search + pointer swap)
- `move_song_down(song)`: **O(n)** (linear search + pointer swap)
- `show_playlist()`: **O(n)** (traversal to build list)

### Benchmark comparison with list-based version
Measured with `python performance_test.py` (operation time only; setup excluded).

| Size | add_end (linked/list) | remove_middle (linked/list) | remove_front (linked/list) | middle_position_edit* (linked/list) |
|---:|---:|---:|---:|---:|
| 10 | 0.00000145 / 0.00000056 | 0.00000265 / 0.00000074 | 0.00000099 / 0.00000057 | 0.00000196 / 0.00000071 |
| 1,000 | 0.00000176 / 0.00000134 | 0.00005512 / 0.00000812 | 0.00000160 / 0.00000082 | 0.00008813 / 0.00000107 |
| 10,000 | 0.00000597 / 0.00000226 | 0.00061292 / 0.00009148 | 0.00000409 / 0.00003689 | 0.00103404 / 0.00000403 |

\* `middle_position_edit` benchmarks linked-list `move_song_down` versus list `insert_middle` as representative middle-position edits.

Interpretation:
- Linked list clearly wins for **remove_front** at large sizes (10,000), matching the expected O(1) vs O(n) trend.
- Python lists are faster in many other operations because list operations run in optimized C, while this linked list is pure Python.
- Asymptotically, linked lists still provide predictable O(1) head removal and O(1) tail append.

## Recommendation for This Version
If your product frequently plays/removes from the front of very large playlists, linked list is a good conceptual fit and has better asymptotic behavior there. In CPython specifically, however, built-in list or `collections.deque` may outperform a custom linked list in wall-clock time due to lower interpreter overhead.
