const user = require('../components/user');
const auth = require('../components/auth');
const meals = require('../components/meals')
const rfid = require('../components/rfid')

module.exports = app => {
  const components = [
    auth,
    user,
    meals,
    rfid
  ];
  components.forEach(component => {
    component(app);
  });
};
