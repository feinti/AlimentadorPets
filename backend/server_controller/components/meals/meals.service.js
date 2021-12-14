const md5 = require('md5');
const MealsModel = require('../models/meals.model');
const { NotFoundError, BadRequestError } = require('./../../utils/erros.model.js');
const { v4: uuidv4 } = require('uuid');
const meals = require('.');
// uuidv4(); // ⇨ '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'

class MealsService {
  static async createMeal(data) {
    const current = await MealsModel.findAll({
      where: {
        user_id: data.user_id,
        deletedAt: null
      }
    })
    if (current[0]) {
      console.log('LOOOVE LVOE    ', current[0].dataValues)
      const updates = []
      current.forEach(data => {
        data.update({ isActive: false })
        data.destroy()
      });
      await Promise.all(updates)
    }

    console.log('start')
    const meals_id = uuidv4()
    console.log('Adding meals ' + JSON.stringify({
      user_id: data.user_id,
      meal_id: meals_id,
      meal_size_grams: data.meal_size_grams,
      hora: data.hour,
      minuto: data.minute,
      isActive: true
    }))
    return await MealsModel.create({
      user_id: data.user_id,
      meal_id: meals_id,
      meal_size_grams: data.meal_size_grams,
      hora: data.hour,
      minuto: data.minute,
      isActive: true
    });
  }

  static async getMeals({ user_id }) {
    const meals = await MealsModel.findAll({
      where: {
        user_id: user_id,
        isActive: true,
        deletedAt: null
      }
    })

    return meals
  }

}

module.exports = MealsService;
