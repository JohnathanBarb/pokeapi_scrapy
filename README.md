# PokeAPI Scrapy

[PokeAPI](https://pokeapi.co/docs/v2) is a full RESTful API linked to an extensive database detailing everything about the Pokémon main game series.

The pokeapi_scrapy is a CRUD API that provides the data we scrapped from PokeAPI.  
Basically, we use [FastAPI Framework](https://github.com/tiangolo/fastapi) for make the API and [requests](https://github.com/psf/requests) for scrapy the PokeAPI.

The FastAPI provides a documentation about the API created using it, it's located on /docs endpoint.  
> Example:
>> If you run using the commands bellow, it is going to be on <http://localhost:8080/docs>.

## Dependency

For run this application, you gonna need docker and docker-compose.  
If you don't have one of these, follow the respective guide:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

## Development

With the previously listed dependencies installed and configurated correctly, clone the repository and start the application

```bash
# cloning the repository
git clone git@github.com:JohnathanBarb/pokeapi_scrapy.git

# going to cloned directory
cd pokeapi_scrapy

# running the application with docker-compose in detach mode
docker-compose up --build -d

# if necessary, to make a scrapy of the pokemons of PokeAPI
docker-compose exec web python scrapy_project/main.py
```

## Author

- [JohnathanBarb](https://linkedin.com/in/johnathan-barbosa/)
