'use strict';

function selectLessons(data, now = Date.now()) {
  if (!data || data.schemaVersion !== 1) throw new Error('schema');
  if (data.status === 'unconfigured') return { state: 'unconfigured', rows: [] };
  const updated = Date.parse(data.updatedAt);
  const until = Date.parse(data.validUntil);
  if (data.status !== 'ready' || data.timezone !== 'Asia/Tokyo' || !Number.isFinite(updated)
      || !Number.isFinite(until) || updated > now + 60000 || until <= updated || !Array.isArray(data.lessons)) throw new Error('schema');
  if (now >= until) return { state: 'expired', updated, rows: [] };
  const rows = data.lessons.map(row => {
    if (!row || !/^\d{4}-\d{2}-\d{2}$/.test(row.date) || !/^([01]\d|2[0-3]):[0-5]\d$/.test(row.startTime)
        || !/^([01]\d|2[0-3]):[0-5]\d$/.test(row.endTime) || typeof row.courseName !== 'string'
        || typeof row.classroomName !== 'string') throw new Error('lesson');
    const start = Date.parse(`${row.date}T${row.startTime}:00+09:00`);
    const end = Date.parse(`${row.date}T${row.endTime}:00+09:00`);
    if (!Number.isFinite(start) || !Number.isFinite(end) || start >= end) throw new Error('time');
    return { ...row, start, end };
  }).sort((a, b) => a.start - b.start);
  const active = rows.filter(row => row.start <= now && now < row.end);
  const future = rows.filter(row => row.start > now);
  const next = future.length ? future.filter(row => row.start === future[0].start) : [];
  return { state: 'ready', updated, rows: [
    ...active.map(row => ({ ...row, label: 'ただいま' })),
    ...next.map(row => ({ ...row, label: 'つぎのレッスン' }))
  ] };
}

if (typeof module !== 'undefined') module.exports = { selectLessons };

if (typeof document !== 'undefined') {
  const content = document.getElementById('lesson-content');
  const updatedNode = document.getElementById('lesson-updated');
  const dateFormat = new Intl.DateTimeFormat('ja-JP', { timeZone: 'Asia/Tokyo', month: 'numeric', day: 'numeric', weekday: 'short' });
  const updateFormat = new Intl.DateTimeFormat('ja-JP', { timeZone: 'Asia/Tokyo', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  let snapshot = null;
  function message(text) {
    content.replaceChildren();
    const p = document.createElement('p'); p.textContent = text; content.append(p);
  }
  function render() {
    try {
      const view = selectLessons(snapshot);
      updatedNode.textContent = view.updated ? `最終更新 ${updateFormat.format(view.updated)}` : '';
      if (view.state === 'unconfigured') return message('レッスン予定は準備中です。教材ボタンはそのまま使えます。');
      if (view.state === 'expired') return message('予定の更新を確認できません。先生に確認してください。');
      if (!view.rows.length) return message('取得した期間に、これからのレッスンはありません。');
      content.replaceChildren();
      for (const row of view.rows) {
        const line = document.createElement('div'); line.className = 'lesson-row';
        for (const [className, text] of [ ['lesson-badge', row.label],
          ['lesson-time', `${dateFormat.format(row.start)} ${row.startTime}〜${row.endTime}`],
          ['lesson-name', row.courseName] ]) {
          const span = document.createElement('span'); span.className = className; span.textContent = text; line.append(span);
        }
        content.append(line);
      }
    } catch { message('現在、予定を確認できません。教材ボタンはそのまま使えます。'); }
  }
  async function refresh() {
    try {
      const response = await fetch('data/lessons.json', { cache: 'no-store', signal: AbortSignal.timeout(10000) });
      if (!response.ok) throw new Error('network');
      snapshot = await response.json(); render();
    } catch {
      snapshot = null; updatedNode.textContent = '';
      message('現在、予定を確認できません。教材ボタンはそのまま使えます。');
    }
  }
  refresh();
  setInterval(refresh, 5 * 60 * 1000);
  setInterval(() => { if (snapshot) render(); }, 30000);
}
