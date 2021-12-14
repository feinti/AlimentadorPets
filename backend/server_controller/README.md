# BACKEND SERVICE

Back-end responsavel pelo controle de todas as rotas implementadas, bem como autenticacao e OAuth2.0
 
### Install dependencies:
`npm i`

### Start development mode:
`npm start`

### Staging build: 
`npm run build:stage`

### Production build:
`npm run build:prod`

### Creating a postgres container
`docker run --name main-postgres --network=postgres-network -e "POSTGRES_PASSWORD=postgres" -p 5432:5432 -v /home/titi/Documents/projetos/dbs/PostgreSQL:/var/lib/postgresql/data -d postgres`


# Postman Collection: API-Alimentador de pets
# 📁 Collection: rfid/nfc module 


## End-point: register tag rfid
### Method: POST
>```
>localhost:3000/rfid/registerPet
>```
### Headers

|Content-Type|Value|
|---|---|
|x-auth-token|auth-token


### Body (**raw**)

```json
{
    "tag_id": "atagid",
    "user_id": "tiago_teste",
    "pet_type": "dog",
    "pet_name": "astolfo_34"
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: requestWrite
### Method: POST
>```
>http://localhost:3000/rfid/requestWrite
>```
### Body (**raw**)

```json
{
    "user_id": "tiago_teste",
    "pet_type": "gato",
    "pet_name": "tito"
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃
# 📁 Collection: meals 


## End-point: create meals
### Method: POST
>```
>localhost:3000/meals/createMeal
>```
### Body (**raw**)

```json
{
    "user_id": "tiago_teste",
    "hours": [12,15,19],
    "minutes": [0,0,0],
    "meal_size_grams": 30
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: manualTrigger
### Method: POST
>```
>localhost:3000/meals/manualTrigger
>```
### Body (**raw**)

```json
{
    "user_id": "tiago_teste",
    "meal_size_grams": 50
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: fetchMeals
### Method: GET
>```
>localhost:3000/meals/fetchMeals
>```
### Body (**raw**)

```json
{
    "user_id": "tiago_teste"
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

___________________________________________
Powered By: [postman-to-markdown](https://github.com/bautistaj/postman-to-markdown/)
