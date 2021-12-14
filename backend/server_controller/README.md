# LOGIN BACKEND SERVICE

Login back-end service responsible for registering, updating user accounts and route authentication.
 
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
