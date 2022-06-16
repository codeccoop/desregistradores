const sqlite = require('spatialite');

module.exports = {
    findAll: function findAll(ctx, next) {
        fetch("http://localhost:1338/api/parceles")
            .then(res => res.json())
            .then(data => ctx.body = data);
        // const db = new sqlite.Database(".tmp/data.db");
        // const query = "SELECT AsGeoJSON(Geometry) AS geom FROM parceles";
        // return new Promise((res, rej) => {
        //     db.spatialite(function(err) {
        //         if (err) rej();
        //         db.all(query, function(err, rows) {
        //             if (err) rej();
        //             const response = '{"data": [' + rows.join(",") + ']}';
        //             ctx.body = response;
        //             ctx.set("Content-Type", "application/json");
        //             next().then(() => res());
        //         });
        //     });
        // });
    },
    findById: function (ctx) {
        console.log(ctx);
        ctx.body = "Find one parcela by id";
    },
    findByCoordinates: function (ctx) {
        console.log(ctx);
        ctx.body = "Find one parceles by coordinates";
    }
}