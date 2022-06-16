module.exports = {
    routes: [
        {
            method: "GET",
            path: "/parceles",
            handler: "parceles.findAll",
            config: {
                auth: false,     
            }
        },
        {
            method: "GET",
            path: "/parceles/:id",
            handler: "parceles.findById",
            config: {
                auth: false,     
            }
        },
        {
            method: "GET",
            path: "/parceles/:lat/:lng/:zoom",
            handler: "parceles.findByCoordinates",
            config: {
                auth: false,     
            }
        },
    ]
}