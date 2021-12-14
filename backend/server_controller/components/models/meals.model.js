const Sequelize = require('sequelize');
const db = require('../../config/db');

module.exports = db.define('meals', {
  user_id: {
    type: Sequelize.STRING
  },
  meal_id: {
    type: Sequelize.STRING
  },
  meal_size_grams: {
    type: Sequelize.INTEGER
  },
  hora: {
    type: Sequelize.INTEGER
  },
  minuto: {
    type: Sequelize.INTEGER
  },
  isActive: {
    type: Sequelize.BOOLEAN,
    defaultValue: false
  }
}, { paranoid: true });
