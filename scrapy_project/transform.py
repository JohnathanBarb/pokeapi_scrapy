from typing import Dict
def transform_in_model(poke_dict: Dict) -> Dict:
    poke_dict['types'] = [
        poke_type['type']['name']
        for poke_type in poke_dict['types']
    ]
    
    poke_dict['stats'] = [
        {
            'name': poke_stat['stat']['name'],
            'base_stat': poke_stat['base_stat']
        } for poke_stat in poke_dict['stats']
    ]

    poke_dict['moves'] = [
        poke_move['move']['name']
        for poke_move in poke_dict['moves']
    ]

    return poke_dict
