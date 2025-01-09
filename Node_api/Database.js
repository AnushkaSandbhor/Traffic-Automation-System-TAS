const mongoose= require('mongoose')
const db_url= `${process.env.DB_HOST}://${process.env.DB_USERNAME}:${process.env.DB_PASS}@${process.env.DB_ENDPOINT}`

let connectMongoDb = () =>{
    return new Promise((resolve, reject) =>{
        mongoose.connect(db_url);

        mongoose.connection
            .once("open", () =>{
                console.log("Connected");
                const conn_status = mongoose.connection.readyState;
                resolve(conn_status);
            })
            .on("error", (error) =>{
                console.log("Error :" + error)
                reject("Mongo Db Connection Failed")
            });
    });
}

module.exports.connectMongoDb =connectMongoDb;
