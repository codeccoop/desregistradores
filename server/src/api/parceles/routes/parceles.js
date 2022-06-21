module.exports = {
  routes: [
    {
      method: "GET",
      path: "/parceles",
      handler: "parceles.findAll",
      config: {
        auth: false,
      },
    },
    {
      method: "GET",
      path: "/parceles/:refcat",
      handler: "parceles.findByRefcat",
      config: {
        auth: false,
      },
    },
    {
      method: "POST",
      path: "/parceles",
      handler: "parceles.findByBbox",
      config: {
        auth: false,
      },
    },
  ],
};
