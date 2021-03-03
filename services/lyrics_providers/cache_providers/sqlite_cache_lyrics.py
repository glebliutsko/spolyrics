import logging
import os
import sqlite3
from typing import TYPE_CHECKING, Optional

import constants
from services.lyrics_providers import CacheLyricsABC

if TYPE_CHECKING:
    from services.spotify import Track
    from sqlite3 import Connection


class SqliteCacheLyrics(CacheLyricsABC):
    def __init__(self):
        self.logger = logging.getLogger(constants.General.NAME)

        self.path_db = os.path.join(constants.Path.CACHE, 'lyrics-cache.db')
        self.db_conn: Optional['Connection'] = None

    @property
    def is_init(self) -> bool:
        return self.db_conn is not None

    def _create_structure_db(self):
        self.logger.debug('Create structure database.')

        with self.db_conn as cursor:
            cursor.execute(
                'CREATE TABLE cache_lyrics'
                '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'spotify_id VARCHAR (100),'
                'provider VARCHAR (30),'
                'lyrics TEXT)'
            )
            cursor.execute(
                'CREATE INDEX index_spotify_id '
                'ON cache_lyrics(spotify_id)'
            )
            cursor.execute(
                'CREATE TABLE metadata'
                '(id INTEGER PRIMARY KEY,'
                'key varchar(255) UNIQUE,'
                'value varchar(255))'
            )
            cursor.execute(
                'INSERT INTO metadata(key, value) '
                'VALUES (?, ?)',
                ('version', constants.General.VERSION, )
            )
            cursor.commit()

    def _recreation_db(self):
        self.db_conn.close()
        self.logger.debug(f'Remove file {self.path_db} with database')
        os.remove(self.path_db)

        self.db_conn = sqlite3.connect(self.path_db)
        self._create_structure_db()

    def init_db(self):
        self.logger.debug('Start initialization database.')

        new_db = True
        if os.path.exists(self.path_db):
            new_db = False

        self.db_conn = sqlite3.connect(self.path_db)
        if new_db:
            self.logger.debug('Create new database.')
            self._create_structure_db()
        else:
            with self.db_conn as cursor:
                version = cursor.execute(
                    'SELECT `value` '
                    'FROM metadata '
                    'WHERE key = ?',
                    ('version', )
                ).fetchone()[0]

            if version != constants.General.VERSION:
                self.logger.debug(f'Detect other version {version} (current {constants.General.VERSION}). '
                                  f'Start recreation database.')
                self._recreation_db()

    def get_lyrics(self, track: 'Track', provider: str) -> Optional[str]:
        with self.db_conn as cursor:
            lyrics = cursor.execute(
                'SELECT lyrics '
                'FROM cache_lyrics '
                'WHERE spotify_id = ? AND provider = ?',
                (track.id, provider, )
            ).fetchone()

            if lyrics is not None:
                return lyrics[0]

    def cache_lyrics(self, track: 'Track', lyrics: str, provider: str):
        with self.db_conn as cursor:
            count_cache = cursor.execute(
                'SELECT COUNT(id) '
                'FROM cache_lyrics '
                'WHERE spotify_id = ? AND provider = ?',
                (track.id, provider, )
            ).fetchone()[0]

            if count_cache == 0:
                cursor.execute(
                    'INSERT INTO cache_lyrics(spotify_id, provider, lyrics) '
                    'VALUES(?, ?, ?)',
                    (track.id, provider, lyrics,)
                )
                cursor.commit()
