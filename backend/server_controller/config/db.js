const Sequelize = require('sequelize');
// const sequelizeInst = new Sequelize('postgres', 'postgres', 'postgres', {
//   host: 'localhost:5432',
//   dialect: 'postgres'
// });
const sequelizeInst = new Sequelize('postgres://postgres:postgres@localhost:5432/postgres');

sequelizeInst
  .authenticate()
  .then(() => {
    console.log('Connection has been established successfully.');
  })
  .catch((err) => {
    console.log('Unable to connect to the database:', err);
  });

module.exports = sequelizeInst;
