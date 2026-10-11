"""Fetch a validated, public-only snapshot. Never print credentials or raw responses."""
import calendar
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

JST = ZoneInfo('Asia/Tokyo')
ENDPOINT = 'https://res.8x9.jp/api/external/v1/lessons'


class InvalidData(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidData(message)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_page(token, room, month, page):
    year, number = map(int, month.split('-'))
    query = urllib.parse.urlencode({'classroom_id': room, 'from': month + '-01',
        'to': f'{month}-{calendar.monthrange(year, number)[1]:02}', 'page': page, 'per_page': 100})
    req = urllib.request.Request(ENDPOINT + '?' + query, headers={
        'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'User-Agent': 'Hack-Lesson-Portal'})
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=15) as response:
            require(response.status == 200, 'APIの応答が成功ではありません。')
            raw = response.read(1048577)
            require(len(raw) <= 1048576, 'API応答のサイズ上限を超えました。')
            return json.loads(raw)
    except urllib.error.HTTPError as error:
        raise InvalidData(f'API取得失敗：HTTP {error.code}。認証・権限・利用制限を確認してください。') from None
    except (urllib.error.URLError, TimeoutError, UnicodeError, json.JSONDecodeError):
        raise InvalidData('API通信またはJSONの解析に失敗しました。') from None


def normalize(item, room, month):
    require(isinstance(item, dict), 'レッスンの形式が不正です。')
    classroom, course = item.get('classroom'), item.get('course')
    require(isinstance(classroom, dict) and isinstance(course, dict), '教室・コースがありません。')
    require(item.get('classroomId') == classroom.get('id') == room, '教室IDが一致しません。')
    require(isinstance(item.get('courseId'), str) and item['courseId'] == course.get('id'), 'コースIDが一致しません。')
    require(isinstance(course.get('name'), str) and isinstance(classroom.get('name'), str), '表示名が不正です。')
    require(type(item.get('draft')) is bool, '下書き属性が不正です。')
    identifier = item.get('id')
    require(type(identifier) in (str, int) and str(identifier) != '', 'レッスンIDが不正です。')
    date = item.get('date')
    require(isinstance(date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', date), '日付が不正です。')
    try:
        local_date = dt.datetime.fromisoformat(date.replace('Z', '+00:00')).astimezone(JST).date()
        require(all(type(item.get(k)) is int for k in ('year', 'month', 'day')), '年月日の型が不正です。')
        require(local_date == dt.date(item['year'], item['month'], item['day']), '日本時間の日付が一致しません。')
    except (ValueError, TypeError, KeyError):
        raise InvalidData('日本時間の日付が不正です。') from None
    require(local_date.strftime('%Y-%m') == month, '取得対象月と日付が一致しません。')
    for key in ('startTime', 'endTime'):
        require(isinstance(item.get(key), str) and re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?', item[key]), '時刻が不正です。')
    start, end = item['startTime'][:5], item['endTime'][:5]
    require(start < end, '日跨ぎ・終了時刻の仕様は未対応です。')
    # Only explicitly permitted display fields leave the job. Teacher mapping is unconfirmed.
    return str(identifier), item['draft'], {'date': str(local_date), 'startTime': start,
        'endTime': end, 'courseName': course['name'], 'classroomName': classroom['name']}


def collect(token, rooms, months, getter=request_page):
    result, seen = [], set()
    for room in rooms:
        for month in months:
            page, last, total, received = 1, 1, None, 0
            while page <= last:
                payload = getter(token, room, month, page)
                require(isinstance(payload, dict) and payload.get('success') is True, 'APIが成功を返しませんでした。')
                data = payload.get('data')
                require(isinstance(data, dict) and isinstance(data.get('data'), list), 'レッスン配列が不正です。')
                require(type(data.get('total')) is int and data['total'] >= 0
                    and type(data.get('last_page')) is int and 1 <= data['last_page'] <= 20
                    and type(data.get('current_page')) is int and data['current_page'] == page, 'ページ情報が不正です。')
                if total is not None:
                    require(total == data['total'] and last == data['last_page'], '取得途中で件数が変わりました。')
                total, last = data['total'], data['last_page']
                for item in data['data']:
                    received += 1
                    identifier, draft, row = normalize(item, room, month)
                    require(identifier not in seen, 'レッスンIDが重複しています。')
                    seen.add(identifier)
                    if not draft:
                        result.append(row)
                page += 1
            require(received == total, '総件数と取得件数が一致しません。')
    return sorted(result, key=lambda r: (r['date'], r['startTime'], r['classroomName'], r['courseName']))


def main():
    token = os.environ.get('HACK_RESERVATION_API_TOKEN', '').strip()
    require(token and not re.search(r'[\x00-\x1f\x7f]', token), 'APIキーをGitHub Secretsへ登録してください。')
    rooms = [r.strip() for r in os.environ.get('LESSON_CLASSROOM_IDS', '').split(',') if r.strip()]
    require(rooms and len(rooms) <= 10 and len(set(rooms)) == len(rooms)
        and all(re.fullmatch(r'[A-Za-z0-9_-]{1,64}', r) for r in rooms), '教室IDを重複なくカンマ区切りで設定してください。')
    now = dt.datetime.now(JST)
    next_month = (now.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
    months = [now.strftime('%Y-%m'), next_month.strftime('%Y-%m')]
    rows = collect(token, rooms, months)
    snapshot = {'schemaVersion': 1, 'status': 'ready', 'timezone': 'Asia/Tokyo',
        'updatedAt': now.isoformat(), 'validUntil': (now + dt.timedelta(hours=24)).isoformat(),
        'period': {'from': months[0] + '-01', 'to': f'{months[1]}-{calendar.monthrange(next_month.year, next_month.month)[1]:02}'},
        'lessons': rows}
    target = Path('public/data/lessons.json')
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(target)
    print(f'取得・検証成功：{len(rooms)}教室、{len(rows)}件。公開用JSONを生成しました。')


if __name__ == '__main__':
    try:
        main()
    except InvalidData as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except Exception:
        print('取得処理に失敗しました。公開内容は更新しません。', file=sys.stderr)
        sys.exit(1)
