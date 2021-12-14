const Sequelize = require('sequelize');
const db = require('../../config/db');

module.exports = db.define('tags', {
  user_id: {
    type: Sequelize.STRING
  },
  tag_id: {
    type: Sequelize.STRING
  },
  pet_name: {
    type: Sequelize.STRING
  },
  pet_type: {
    type: Sequelize.STRING
  }
}, { paranoid: true });
