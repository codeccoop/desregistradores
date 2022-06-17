const http = require("http");
const url = require("url");

const host = "localhost";
const port = 1338;
const path = "/parceles";

module.exports = {
  findAll: function findAll(ctx) {
    return new Promise((res, rej) => {
      const { query } = ctx;
      const requestURL = url.parse(
        url.format({
          protocol: "http",
          hostname: host,
          port: port,
          pathname: path,
          query: query,
        })
      );

      const request = http.request(
        {
          host: requestURL.hostname,
          port: requestURL.port,
          path: requestURL.path,
          method: "GET",
          headers: {
            Accept: "application/json; charset=UTF-8",
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
              ctx.set("Content-Type", "application/json; charset=UTF-8");
              ctx.body = `{"data":${data}}`;
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
      const { query } = ctx;
      const requestURL = url.parse(
        url.format({
          protocol: "http",
          hostname: host,
          port: port,
          pathname: `${path}/${ctx.params.id}`,
          query: query,
        })
      );

      const request = http.request(
        {
          host: requestURL.hostname,
          port: requestURL.port,
          path: requestURL.path,
          method: "GET",
          headers: {
            Accept: "application/json; charset=UTF-8",
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
              ctx.set("Content-Type", "application/json; charset=UTF-8");
              ctx.body = `{"data":${data}}`;
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
      const { query } = ctx;
      const requestURL = url.parse(
        url.format({
          protocol: "http",
          hostname: host,
          port: port,
          pathname: path,
          query: query,
        })
      );

      const request = http.request(
        {
          host: requestURL.hostname,
          port: requestURL.port,
          path: requestURL.path,
          method: "POST",
          headers: {
            Accept: "application/json; charset=UTF-8",
            "Content-Type": "application/json; charset=UTF-8",
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
              ctx.set("Content-Type", "application/json; charset=UTF-8");
              ctx.body = `{"data":${data}}`;
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
