const md5 = require('md5');
const rfidService = require('./rfid.service');
const CommonUtils = require('../../utils/common');
const { HOST, LISTEN_PORT } = require('../../config/pi.sockets.js');
const axios = require('axios').default;

class Meal {
  static async registerPet(req, res) {
    // const { meal_id } = req.params;
    const { pet_type, user_id, pet_name, tag_id } = req.body;
    try {
      await rfidService.registerPet({ pet_type, user_id, pet_name, tag_id })

      return res.status(200).json({ success: true });
    } catch (err) {
      return CommonUtils.catchError(res, err);
    }
  }

  static async requestWrite(req, res) {
    // const { meal_id } = req.params;
    const { user_id, pet_name, pet_type } = req.body;
    try {
      const pi_socket = "http://" + HOST + ":" + LISTEN_PORT;
      const response = await axios({
        method: 'post',
        url: pi_socket,
        data: {
          user_id: user_id,
          action_requested: 'rfid_write',
          text: pet_name + '.' + pet_type
        }
      });

      if (response.data.error) {
        throw new Error('Request failed: ' + response.data.error);
      }

      console.log("\n\n THIS IS THE RESPONSE \n", response, "\n=================\n\n\n")

      // await rfidService.registerPet({ pet_type, user_id, pet_name, tag_id })

      return res.status(200).json({ success: true });
    } catch (err) {
      return CommonUtils.catchError(res, err);
    }
  }

  // static async deleteMeal(req, res) {
  //   const { id } = req.params;
  //   try {
  //     await rfidService.deleteUser(id);

  //     return res.status(204).send();
  //   } catch (err) {
  //     return CommonUtils.catchError(res, err);
  //   }
  // }

  // static async cupdateMeal(req, res) {
  //   const { id } = req.params;
  //   const { name, email, role } = req.body;
  //   try {
  //     await rfidService.checkExistingEmail(id, email);
  //     const user = await rfidService.updateUser(id, { name, email, role });

  //     return res.status(200).json({ user });
  //   } catch (err) {
  //     return CommonUtils.catchError(res, err);
  //   }
  // }

  // static async getList(req, res) {

  //   try {
  //     const users = await rfidService.getUsers(req.query.offset, req.query.limit);
  //     return res.status(200).json({ users });
  //   } catch (err) {
  //     return CommonUtils.catchError(res, err);
  //   }
  // }

}

module.exports = Meal;
