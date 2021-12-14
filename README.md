# Projeto PCS3858 - Grupo 8 - Alimentador automatico

O objetivo deste projeto e realizar a implementacao de uma prova de conceito de um alimentador de pets automatizado, que seja capaz de repor a racao do animal em tempos definidos pelo usuario, bem como volume em gramas. Tambem deve ser capaz de repor a agua na vazilha e ativar circulador. 

Biblioteca para controle de mfc: 
```
sudo pip3 install mfrc522
```

Repositorios utilizados para o controle do sensor de carga HX711: https://github.com/tatobari/hx711py

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
