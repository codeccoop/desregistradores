module.exports = {
  routes: [
    {
      method: "GET",
      path: "/districtes",
      handler: "districtes.findAll",
      config: {
        auth: false,
      },
    },
    {
      method: "GET",
      path: "/districtes/:id",
      handler: "districtes.findById",
      config: {
        auth: false,
      },
    },
    {
      method: "POST",
      path: "/districtes",
      handler: "districtes.findByBbox",
      config: {
        auth: false,
      },
    },
  ],
};
