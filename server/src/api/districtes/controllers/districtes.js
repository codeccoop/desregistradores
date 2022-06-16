const http = require("http");

const host = "localhost";
const port = 1338;
const path = "/districtes";

module.exports = {
  findAll: function findAll(ctx) {
    return new Promise((res, rej) => {
      const request = http.request(
        {
          host: host,
          port: port,
          path: path,
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        },
        (resp) => {
          if (resp.statusCode !== 200) {
            resp.resume();
            rej();
          } else {
            let data = "";
            resp.on("data", (chunk) => (data += chunk));
            resp.on("close", () => {
              ctx.set("Content-Type", "application/json; charset=utf-8");
              ctx.body = data;
              res();
            });
          }
        }
      );

      request.on("erro", rej);
      request.end();
    });
  },
  findById: function findById(ctx) {
    return new Promise((res, rej) => {
      const request = http.request(
        {
          host: host,
          port: port,
          path: `${path}/${ctx.params.id}`,
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        },
        (resp) => {
          if (resp.statusCode !== 200) {
            resp.resume();
            rej();
          } else {
            let data = "";
            resp.on("data", (chunk) => (data += chunk));
            resp.on("close", () => {
              ctx.set("Content-Type", "application/json; charset=utf-8");
              ctx.body = data;
              res();
            });
          }
        }
      );

      request.on("error", rej);
      request.end();
    });
  },
  findByBbox: function findByBbox(ctx) {
    return new Promise((res, rej) => {
      const request = http.request(
        {
          host: host,
          port: port,
          path: path,
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        },
        (resp) => {
          if (resp.statusCode !== 200) {
            resp.resume();
            rej();
          } else {
            let data = "";
            resp.on("data", (chunk) => (data += chunk));
            resp.on("close", () => {
              ctx.set("Content-Type", "application/json; charset=utf-8");
              ctx.body = data;
              res();
            });
          }
        }
      );

      request.write(JSON.stringify(ctx.request.body));
      request.on("error", rej);
      request.end();
    });
  },
};
