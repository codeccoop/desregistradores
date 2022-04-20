'use strict';

/**
 * nota-simple service.
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::nota-simple.nota-simple');
