import copy
import unittest
from scripts.fetch_lessons import collect, normalize, InvalidData


def lesson(identifier='one', **changes):
    item = {'id': identifier, 'classroomId': 'ROOM', 'classroom': {'id': 'ROOM', 'name': 'テスト教室'},
        'courseId': 'C1', 'course': {'id': 'C1', 'name': 'テストコース'},
        'date': '2026-09-30T15:00:00Z', 'year': 2026, 'month': 10, 'day': 1,
        'startTime': '10:00:00', 'endTime': '11:30:00', 'draft': False,
        'privateEmail': 'not-for-public@example.invalid', 'students': [{'name': '非公開'}]}
    item.update(changes)
    return item


def page(items, number=1, last=1, total=None):
    return {'success': True, 'data': {'total': len(items) if total is None else total,
        'current_page': number, 'last_page': last, 'data': items}}


class FetchTests(unittest.TestCase):
    def test_jst_boundary_and_allowlist(self):
        _, _, row = normalize(lesson(), 'ROOM', '2026-10')
        self.assertEqual(row['date'], '2026-10-01')
        self.assertEqual(set(row), {'date', 'startTime', 'endTime', 'courseName', 'classroomName'})

    def test_all_pages_and_draft_exclusion(self):
        pages = [page([lesson()], last=2, total=2), page([lesson('two', draft=True)], 2, 2, 2)]
        rows = collect('unused', ['ROOM'], ['2026-10'], lambda t, r, m, n: pages[n-1])
        self.assertEqual(len(rows), 1)

    def test_duplicate_is_failure(self):
        with self.assertRaises(InvalidData):
            collect('unused', ['ROOM'], ['2026-10'], lambda *args: page([lesson(), lesson()]))

    def test_count_mismatch_is_failure(self):
        with self.assertRaises(InvalidData):
            collect('unused', ['ROOM'], ['2026-10'], lambda *args: page([lesson()], total=2))

    def test_midway_change_is_failure(self):
        pages = [page([lesson()], last=2, total=2), page([lesson('two')], 2, 2, 3)]
        with self.assertRaises(InvalidData):
            collect('unused', ['ROOM'], ['2026-10'], lambda t, r, m, n: pages[n-1])

    def test_empty_success(self):
        self.assertEqual(collect('unused', ['ROOM'], ['2026-10'], lambda *args: page([])), [])

    def test_wrong_room_and_date_rejected(self):
        for changes in ({'classroomId': 'OTHER'}, {'day': 2}, {'draft': 'false'}, {'endTime': '09:00'}):
            with self.subTest(changes=changes), self.assertRaises(InvalidData):
                normalize(lesson(**changes), 'ROOM', '2026-10')

    def test_simultaneous_distinct_lessons_preserved(self):
        rows = collect('unused', ['ROOM'], ['2026-10'], lambda *args: page([lesson(), lesson('two')]))
        self.assertEqual(len(rows), 2)


if __name__ == '__main__':
    unittest.main()
