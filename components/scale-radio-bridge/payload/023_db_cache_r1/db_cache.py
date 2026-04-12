#!/usr/bin/env python3
import json
import os
import sqlite3
import sys
import time
from pathlib import Path


def read_payload():
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)


def connect(db_path: str):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')
    conn.execute('PRAGMA temp_store=MEMORY')
    return conn


def init_schema(conn: sqlite3.Connection):
    conn.executescript(
        '''
        CREATE TABLE IF NOT EXISTS meta (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS lyrics_cache (
          key TEXT PRIMARY KEY,
          artist TEXT,
          title TEXT,
          station TEXT,
          source TEXT,
          has_synced INTEGER NOT NULL DEFAULT 0,
          payload_json TEXT NOT NULL,
          created_at INTEGER NOT NULL,
          expires_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS spotify_match_cache (
          key TEXT PRIMARY KEY,
          artist TEXT,
          title TEXT,
          station TEXT,
          confidence INTEGER NOT NULL DEFAULT 0,
          match_track_id TEXT,
          match_uri TEXT,
          albumart_url TEXT,
          external_url TEXT,
          payload_json TEXT NOT NULL,
          created_at INTEGER NOT NULL,
          expires_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS negative_cache (
          kind TEXT NOT NULL,
          key TEXT NOT NULL,
          reason TEXT,
          created_at INTEGER NOT NULL,
          expires_at INTEGER NOT NULL,
          PRIMARY KEY(kind, key)
        );
        CREATE TABLE IF NOT EXISTS playlist_presence (
          playlist_id TEXT NOT NULL,
          track_id TEXT NOT NULL,
          present INTEGER NOT NULL DEFAULT 1,
          created_at INTEGER NOT NULL,
          updated_at INTEGER NOT NULL,
          expires_at INTEGER NOT NULL,
          PRIMARY KEY(playlist_id, track_id)
        );
        CREATE TABLE IF NOT EXISTS artwork_refs (
          owner_kind TEXT NOT NULL,
          owner_key TEXT NOT NULL,
          image_url TEXT NOT NULL,
          thumb_url TEXT,
          width INTEGER,
          height INTEGER,
          created_at INTEGER NOT NULL,
          PRIMARY KEY(owner_kind, owner_key, image_url)
        );
        CREATE INDEX IF NOT EXISTS idx_negative_expiry ON negative_cache(expires_at);
        CREATE INDEX IF NOT EXISTS idx_lyrics_expiry ON lyrics_cache(expires_at);
        CREATE INDEX IF NOT EXISTS idx_spotify_expiry ON spotify_match_cache(expires_at);
        CREATE INDEX IF NOT EXISTS idx_playlist_expiry ON playlist_presence(expires_at);
        '''
    )
    conn.commit()


def now_ms() -> int:
    return int(time.time() * 1000)


def cleanup(conn: sqlite3.Connection, now: int | None = None):
    now = now or now_ms()
    conn.execute('DELETE FROM lyrics_cache WHERE expires_at <= ?', (now,))
    conn.execute('DELETE FROM spotify_match_cache WHERE expires_at <= ?', (now,))
    conn.execute('DELETE FROM negative_cache WHERE expires_at <= ?', (now,))
    conn.execute('DELETE FROM playlist_presence WHERE expires_at <= ?', (now,))
    conn.commit()


def counts(conn: sqlite3.Connection):
    out = {}
    for table in ('lyrics_cache', 'spotify_match_cache', 'negative_cache', 'playlist_presence', 'artwork_refs'):
        out[table] = int(conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0])
    return out


def set_meta(conn, key, value):
    conn.execute('INSERT INTO meta(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, str(value)))
    conn.commit()


def action_init(conn, payload):
    init_schema(conn)
    cleanup(conn)
    if payload.get('pluginVersion'):
        set_meta(conn, 'plugin_version', payload.get('pluginVersion'))
    return {'ok': True, 'dbPath': payload.get('dbPath'), 'counts': counts(conn)}


def action_status(conn, payload):
    init_schema(conn)
    cleanup(conn)
    return {'ok': True, 'dbPath': payload.get('dbPath'), 'counts': counts(conn)}


def action_clear(conn, payload):
    init_schema(conn)
    for table in ('lyrics_cache', 'spotify_match_cache', 'negative_cache', 'playlist_presence', 'artwork_refs'):
        conn.execute(f'DELETE FROM {table}')
    conn.commit()
    return {'ok': True, 'counts': counts(conn)}


def action_get_lyrics(conn, payload):
    init_schema(conn)
    cleanup(conn)
    row = conn.execute('SELECT payload_json FROM lyrics_cache WHERE key = ?', (payload['key'],)).fetchone()
    if not row:
        return {'ok': True, 'found': False}
    return {'ok': True, 'found': True, 'value': json.loads(row['payload_json'])}


def action_set_lyrics(conn, payload):
    init_schema(conn)
    now = now_ms()
    expires = now + int(float(payload.get('ttl_days', 14)) * 86400 * 1000)
    payload_json = json.dumps(payload['payload'], ensure_ascii=False)
    has_synced = 1 if (payload.get('payload') or {}).get('mode') == 'synced' else 0
    conn.execute(
        '''INSERT INTO lyrics_cache(key, artist, title, station, source, has_synced, payload_json, created_at, expires_at)
           VALUES(?,?,?,?,?,?,?,?,?)
           ON CONFLICT(key) DO UPDATE SET
             artist=excluded.artist,
             title=excluded.title,
             station=excluded.station,
             source=excluded.source,
             has_synced=excluded.has_synced,
             payload_json=excluded.payload_json,
             created_at=excluded.created_at,
             expires_at=excluded.expires_at''',
        (payload['key'], payload.get('artist', ''), payload.get('title', ''), payload.get('station', ''), payload.get('source', 'lrclib'), has_synced, payload_json, now, expires)
    )
    conn.execute('DELETE FROM negative_cache WHERE kind = ? AND key = ?', ('lyrics', payload['key']))
    conn.commit()
    return {'ok': True}


def action_get_spotify_match(conn, payload):
    init_schema(conn)
    cleanup(conn)
    row = conn.execute('SELECT payload_json FROM spotify_match_cache WHERE key = ?', (payload['key'],)).fetchone()
    if not row:
        return {'ok': True, 'found': False}
    return {'ok': True, 'found': True, 'value': json.loads(row['payload_json'])}


def action_set_spotify_match(conn, payload):
    init_schema(conn)
    now = now_ms()
    expires = now + int(float(payload.get('ttl_days', 45)) * 86400 * 1000)
    match = payload.get('payload') or {}
    payload_json = json.dumps(match, ensure_ascii=False)
    conn.execute(
        '''INSERT INTO spotify_match_cache(key, artist, title, station, confidence, match_track_id, match_uri, albumart_url, external_url, payload_json, created_at, expires_at)
           VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(key) DO UPDATE SET
             artist=excluded.artist,
             title=excluded.title,
             station=excluded.station,
             confidence=excluded.confidence,
             match_track_id=excluded.match_track_id,
             match_uri=excluded.match_uri,
             albumart_url=excluded.albumart_url,
             external_url=excluded.external_url,
             payload_json=excluded.payload_json,
             created_at=excluded.created_at,
             expires_at=excluded.expires_at''',
        (
            payload['key'], payload.get('artist', ''), payload.get('title', ''), payload.get('station', ''),
            int(match.get('confidence') or payload.get('confidence') or 0), match.get('id', ''), match.get('uri', ''),
            match.get('albumart', ''), match.get('externalUrl', ''), payload_json, now, expires,
        )
    )
    if match.get('albumart'):
        conn.execute(
            '''INSERT OR REPLACE INTO artwork_refs(owner_kind, owner_key, image_url, thumb_url, width, height, created_at)
               VALUES(?,?,?,?,?,?,?)''',
            ('spotify_match', payload['key'], match.get('albumart', ''), match.get('albumart', ''), None, None, now)
        )
    conn.execute('DELETE FROM negative_cache WHERE kind = ? AND key = ?', ('spotify_match', payload['key']))
    conn.commit()
    return {'ok': True}


def action_get_negative(conn, payload):
    init_schema(conn)
    cleanup(conn)
    row = conn.execute('SELECT reason, expires_at FROM negative_cache WHERE kind = ? AND key = ?', (payload['kind'], payload['key'])).fetchone()
    if not row:
        return {'ok': True, 'found': False}
    return {'ok': True, 'found': True, 'reason': row['reason'], 'expiresAt': row['expires_at']}


def action_set_negative(conn, payload):
    init_schema(conn)
    now = now_ms()
    expires = now + int(float(payload.get('ttl_hours', 6)) * 3600 * 1000)
    conn.execute(
        '''INSERT INTO negative_cache(kind, key, reason, created_at, expires_at)
           VALUES(?,?,?,?,?)
           ON CONFLICT(kind, key) DO UPDATE SET
             reason=excluded.reason,
             created_at=excluded.created_at,
             expires_at=excluded.expires_at''',
        (payload['kind'], payload['key'], payload.get('reason', ''), now, expires)
    )
    conn.commit()
    return {'ok': True}


def action_get_playlist_presence(conn, payload):
    init_schema(conn)
    cleanup(conn)
    row = conn.execute('SELECT present FROM playlist_presence WHERE playlist_id = ? AND track_id = ?', (payload['playlist_id'], payload['track_id'])).fetchone()
    return {'ok': True, 'present': bool(row and int(row['present']) == 1)}


def action_set_playlist_presence(conn, payload):
    init_schema(conn)
    now = now_ms()
    expires = now + int(float(payload.get('ttl_days', 120)) * 86400 * 1000)
    conn.execute(
        '''INSERT INTO playlist_presence(playlist_id, track_id, present, created_at, updated_at, expires_at)
           VALUES(?,?,?,?,?,?)
           ON CONFLICT(playlist_id, track_id) DO UPDATE SET
             present=excluded.present,
             updated_at=excluded.updated_at,
             expires_at=excluded.expires_at''',
        (payload['playlist_id'], payload['track_id'], 1 if payload.get('present', True) else 0, now, now, expires)
    )
    conn.commit()
    return {'ok': True}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'ok': False, 'error': 'Missing action'}))
        return 1
    action = sys.argv[1]
    payload = read_payload()
    db_path = payload.get('dbPath') or payload.get('db_path')
    if not db_path:
        print(json.dumps({'ok': False, 'error': 'Missing dbPath'}))
        return 1
    actions = {
        'init': action_init,
        'status': action_status,
        'clear': action_clear,
        'get_lyrics': action_get_lyrics,
        'set_lyrics': action_set_lyrics,
        'get_spotify_match': action_get_spotify_match,
        'set_spotify_match': action_set_spotify_match,
        'get_negative': action_get_negative,
        'set_negative': action_set_negative,
        'get_playlist_presence': action_get_playlist_presence,
        'set_playlist_presence': action_set_playlist_presence,
    }
    if action not in actions:
        print(json.dumps({'ok': False, 'error': f'Unknown action: {action}'}))
        return 1
    try:
        conn = connect(db_path)
        try:
            result = actions[action](conn, payload)
        finally:
            conn.close()
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
