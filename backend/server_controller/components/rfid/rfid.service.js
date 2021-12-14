const md5 = require('md5');
const rfidModel = require('../models/rfid.model');
const { NotFoundError, BadRequestError } = require('./../../utils/erros.model.js');
const { v4: uuidv4 } = require('uuid');
const rfid = require('.');
// uuidv4(); // ⇨ '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'

class rfidService {
  static async registerPet(data) {
    const current = await rfidModel.findAll({
      where: {
        tag_id: data.tag_id,
        deletedAt: null
      }
    })
    console.log(current)
    if (current[0]) {
      console.log('LOOOVE LVOE    ', current[0].dataValues)
      const updates = []
      current.forEach(data => {
        data.destroy()
      });
      await Promise.all(updates)
    }


    console.log('start')
    const rfid_id = uuidv4()

    return await rfidModel.create({
      user_id: data.user_id,
      tag_id: data.tag_id,
      pet_type: data.pet_type,
      pet_name: data.pet_name
    });
  }

}

module.exports = rfidService;
