""" Main python file. """
import sys
import requests

from cache.cache import Cache
from utils.data_errors import InvalidNameError, InvalidResponseRecieved, NotFoundError


def get_poke_data(pokemon_name: str) -> dict:
    """ Fetches id, name, height and weight of pokemon.

    Args:
        pokemon_name (str): Name of Pokemon.

    Raises:
        PokemonInvalidNameError: Error thrown when input is empty or only made of 
            invalid characters.
        PokemonNotFoundError: Error thrown when Pokemon was not found in database.

    Returns:
        PokeData: pydantic type containing id, name, height and weight fields.
    """

    safe_pkmon_name = ''.join(char for char in pokemon_name if char.isalpha())
    if not safe_pkmon_name:
        raise InvalidNameError(pokemon_name)

    cache = Cache()
    cache_data = cache.search_pokemon(safe_pkmon_name)

    if cache_data:
        return cache_data

    response = requests.get(
        f'https://pokeapi.co/api/v2/pokemon/{safe_pkmon_name}', timeout=10)

    if response.status_code == 404:
        raise NotFoundError(safe_pkmon_name)

    try:
        raw_data = response.json()

        data = {
            'id': raw_data['id'],
            'name': raw_data['name'],
            'height': raw_data['height'],
            'weight': raw_data['weight']
        }
    except requests.JSONDecodeError as e:
        raise InvalidResponseRecieved(pokemon_name) from e
    except KeyError as e:
        raise InvalidResponseRecieved(pokemon_name) from e

    for _ in range(1, 4):
        success = cache.cache_pokemon(data)
        if success:
            break

    return data


def main():
    """ Main function."""
    user_input = " ".join(sys.argv[1:])
    data = get_poke_data(user_input)

    print(data)


if __name__ == "__main__":
    main()
