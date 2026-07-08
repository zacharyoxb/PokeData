""" Db cache """
import os
import sqlite3
import json
from typing import Optional, Dict, Any

CACHE_DIR = "cache"
DB_NAME = os.path.join(CACHE_DIR, "cache.db")


class Cache:
    """ Cache that uses sqlite3 """

    def __init__(self):
        """
        Initialize the cache and create the pokemon table if it doesn't exist.
        """
        self._init_database()

    def _init_database(self):
        """Create the pokemon table with 'name' as primary key if it doesn't exist."""
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pokemon (
                    name TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            conn.commit()

    def cache_pokemon(self, pokemon_data: Dict[str, Any]) -> bool:
        """
        Cache a Pokemon dictionary in the database.

        Args:
            pokemon_data (Dict[str, Any]): Dictionary containing Pokemon data.
                Must have a 'name' key.

        Returns:
            bool: True if cached successfully, False otherwise.
        """

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()

                data_json = json.dumps(pokemon_data)

                cursor.execute("""
                    INSERT OR REPLACE INTO pokemon (name, data)
                    VALUES (?, ?)
                """, (pokemon_data['name'].lower(), data_json))

                conn.commit()
                return True

        except sqlite3.Error as e:
            print(f"Database error while caching: {e}")
            return False

    def search_pokemon(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a Pokemon by name in the cache.

        Args:
            name (str): Name of the Pokemon to search for.

        Returns:
            Optional[Dict[str, Any]]: The Pokemon data dict if found, None otherwise.
        """
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT data FROM pokemon WHERE name = ?
                """, (name.lower(),))

                result = cursor.fetchone()

                if result:
                    return json.loads(result[0])
                return None

        except sqlite3.Error as e:
            print(f"Database error while searching: {e}")
            return None
