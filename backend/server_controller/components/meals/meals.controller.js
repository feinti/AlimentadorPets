const md5 = require('md5');
const MealsService = require('./meals.service');
const CommonUtils = require('../../utils/common');
const { HOST, LISTEN_PORT, JOBS_PORT } = require('../../config/pi.sockets.js');
const axios = require('axios').default;
const { registrationValidator } = require('../auth/auth.service');

class Meal {
  static async createMeal(req, res) {
    // const { meal_id } = req.params;
    const { hours, minutes, user_id, meal_size_grams } = req.body;
    try {
      const calls = []
      const results = []
      hours.forEach((value, i) => {
        let hour = hours[i]
        let minute = minutes[i]
        calls.push(MealsService.createMeal({ user_id, hour, minute, meal_size_grams }));
        let result = {
          meal_size_grams: meal_size_grams,
          hora: hour,
          minuto: minute
        }
        results.push(result)
      });
      await Promise.all(calls)

      // Comunicate rasppy --------------------
      const pi_socket = "http://" + HOST + ":" + JOBS_PORT;
      const response = await axios({
        method: 'post',
        url: pi_socket,
        data: {
          user_id: user_id,
          action_requested: 'fetch_meals',
          meals: results
        }
      });

      if (response.data.error) {
        throw new Error('Request failed: ' + response.data.error);
      }

      console.log("\n\n THIS IS THE RESPONSE \n", response, "\n=================\n\n\n")
      // ----------------------------------------

      return res.status(200).json({ success: true });
    } catch (err) {
      return CommonUtils.catchError(res, err);
    }
  }

  static async fetchMeals(req, res) {
    const { user_id } = req.body;
    try {
      const meals = await MealsService.getMeals({ user_id })
      const results = []
      meals.forEach(meal => {
        let result = {
          meal_size_grams: meal.dataValues.meal_size_grams,
          hora: meal.dataValues.hora,
          minuto: meal.dataValues.minuto
        }
        results.push(result)
      })

      // Comunicate rasppy --------------------
      const pi_socket = "http://" + HOST + ":" + JOBS_PORT;
      const response = await axios({
        method: 'post',
        url: pi_socket,
        data: {
          user_id: user_id,
          action_requested: 'fetch_meals',
          meals: results
        }
      });

      if (response.data.error) {
        throw new Error('Request failed: ' + response.data.error);
      }

      console.log("\n\n THIS IS THE RESPONSE \n", response, "\n=================\n\n\n")
      // ----------------------------------------

      return res.status(200).json({ meals: results });
    } catch (err) {
      return CommonUtils.catchError(res, err);
    }
  }

  static async manualTrigger(req, res) {
    // const { meal_id } = req.params;
    const { user_id, meal_size_grams } = req.body;
    try {
      const pi_socket = "http://" + HOST + ":" + LISTEN_PORT;
      const response = await axios({
        method: 'post',
        url: pi_socket,
        data: {
          user_id: user_id,
          action_requested: 'meal_manual_trigger',
          meal_size_grams: meal_size_grams
        }
      });

      if (response.data.error) {
        throw new Error('Request failed: ' + response.data.error);
      }

      console.log("\n\n THIS IS THE RESPONSE \n", response, "\n=================\n\n\n")

      return res.status(200).json({ success: true });
    } catch (err) {
      return CommonUtils.catchError(res, err);
    }
  }


  // static async deleteMeal(req, res) {
  //   const { id } = req.params;
  //   try {
  //     await MealsService.deleteUser(id);

  //     return res.status(204).send();
  //   } catch (err) {
  //     return CommonUtils.catchError(res, err);
  //   }
  // }

  // static async cupdateMeal(req, res) {
  //   const { id } = req.params;
  //   const { name, email, role } = req.body;
  //   try {
  //     await MealsService.checkExistingEmail(id, email);
  //     const user = await MealsService.updateUser(id, { name, email, role });

  //     return res.status(200).json({ user });
  //   } catch (err) {
  //     return CommonUtils.catchError(res, err);
  //   }
  // }

  // static async getList(req, res) {

  //   try {
  //     const users = await MealsService.getUsers(req.query.offset, req.query.limit);
  //     return res.status(200).json({ users });
  //   } catch (err) {
  //     return CommonUtils.catchError(res, err);
  //   }
  // }

}

module.exports = Meal;
