module.exports = {
  routes: [
    {
      method: "GET",
      path: "/barris",
      handler: "barris.findAll",
      config: {
        auth: false,
      },
    },
    {
      method: "GET",
      path: "/barris/:id",
      handler: "barris.findById",
      config: {
        auth: false,
      },
    },
    {
      method: "POST",
      path: "/barris",
      handler: "barris.findByBbox",
      config: {
        auth: false,
      },
    },
  ],
};
