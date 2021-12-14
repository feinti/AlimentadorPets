const rfidApp = require('./rfid.routes');
const AuthController = require('./../auth/auth.controller.js');
const { USER_ROLE, ADMIN_ROLE } = require('../../config/role.constatnts.js');

module.exports = app => {
  app.use('/rfid', rfidApp);
  // app.use('', AuthController.authValidator(USER_ROLE), UserApp);
  // app.use('/admin', AuthController.authValidator(ADMIN_ROLE), AdminApp);
};
