import os, sys, inspect
import requests
from transform import transform_in_model

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.models.pokemon import PokemonCreate

headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
url = 'https://pokeapi.co/api/v2/pokemon/?offset=0&limit=30'
url_post = 'http://localhost:8080/pokemons/many'

while True:
    print(f'requesting {url}')
    request = requests.get(url)
    results = request.json()['results']
    pokemon_list = []

    for pokemon in results:
        request_pokemon = requests.get(pokemon['url'])
        poke = PokemonCreate(**transform_in_model(request_pokemon.json()))
        poke_dict = poke.dict(by_alias=True)
        poke_dict.pop('_id')
        pokemon_list.append(poke_dict)
    
    r = requests.post(url_post, headers=headers, json=pokemon_list)

    if request.json()['next']:
        url = request.json()['next']
    else:
        break

print('==='*11)
print(f'{"==="*5}END{"==="*5}')
print('==='*11)
