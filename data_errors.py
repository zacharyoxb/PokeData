""" Errors for pokemon request """


class PokemonRequestError(Exception):
    """ Base Exception for all Pokemon request errors. """


class InvalidNameError(PokemonRequestError):
    """ Raised when an invalid pokemon name is provided. """

    def __init__(self, pokemon_name, message="Invalid pokemon name provided"):
        self.name = pokemon_name
        self.message = f"{message}: '{pokemon_name}'"
        super().__init__(self.message)


class NotFoundError(PokemonRequestError):
    """ Raised when a Pokemon does not exist in the api database. """

    def __init__(self, pokemon_name, message="Pokemon does not exist"):
        self.pokemon_name = pokemon_name
        self.message = f"{message}: '{pokemon_name}'"
        super().__init__(self.message)


class InvalidResponseRecieved(PokemonRequestError):
    """ Raised when the response is empty or is invalid. """

    def __init__(self, pokemon_name, message="Could not get data, server sent invalid response"):
        self.pokemon_name = pokemon_name
        self.message = f"{message}: '{pokemon_name}'"
        super().__init__(self.message)
