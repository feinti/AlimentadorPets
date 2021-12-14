const MealsController = require('./meals.controller');
const Validator = require('../../utils/validator.js');
const app = require('express')();

/**
 * @api {get} /me Get my profile
 * @apiName GetMyProfile
 * @apiGroup User
 * @apiPermission user
 *
 * @apiHeader {String} X-Auth-Token User auth token.
 *
 * @apiSuccess {Object} user User.
 * @apiSuccess {Int} user.id Id.
 * @apiSuccess {String} user.name Name.
 * @apiSuccess {String} user.email Email.
 * @apiSuccess {Int} user.role Role.
 *
 * @apiSuccessExample Success-Response:
 *  HTTP/1.1 200 OK
 *  {
 *   user: user
 *  }
 *
 * @apiError {String} reason Error reason.
 *
 * @apiErrorExample Error-Response:
 *  HTTP/1.1 400 Bad Request
 *  {
 *    "reason": "DB error."
 *  }
 *
 *  @apiSampleReques
 */
app.post('/createMeal', MealsController.createMeal);

app.post('/manualTrigger', MealsController.manualTrigger);

app.get('/fetchMeals', MealsController.fetchMeals);

// app.get('/updateMeal', MealsController.updateMeal);

// app.get('/deleteMeal', MealsController.deleteMeal);

module.exports = app;
