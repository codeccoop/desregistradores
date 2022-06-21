"use strict";

const http = require("http");
const url = require("url");

/**
 *  nota-simple controller
 */

const { createCoreController } = require("@strapi/strapi").factories;

module.exports = createCoreController(
  "api::nota-simple.nota-simple",
  ({ strapi }) => ({
    create(ctx) {
      console.log("Enter notes-simples.controller.create");
      return new Promise((res, rej) => {
        console.log("Execute super.create()");
        super
          .create(ctx)
          .then((response) => {
            console.log("super.create.then(response)");
            const request = http.request(
              {
                host: "localhost",
                port: 1338,
                path: `/parceles/${response.data.attributes.refcat}`,
                method: "PUT",
                headers: {
                  Accpet: "application/json; charset=UTF-8",
                  "Content-Type": "application/json; charset=UTF-8",
                },
              },
              (resp) => {
                console.log("http.request => response");
                console.log(resp);
                if (resp.statusCode !== 200) {
                  resp.resume();
                  rej();
                } else {
                  res(response);
                }
              }
            );

            request.write(JSON.stringify({ note_id: response.data.id }));
            request.on("error", rej);
            request.end();
          })
          .catch(rej);
      });
    },
  })
);
