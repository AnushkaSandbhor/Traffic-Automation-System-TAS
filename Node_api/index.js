const express= require("express");
require("dotenv").config();
const database =require("./Database")
const bodyParser= require("body-parser")
const Controller = require("./Controller/UserController")
const port = process.env.PORT;
const { uploadImage, upload } = require('./Controller/UploadController');

let middleware = (request,response,next) =>{
    database.connectMongoDb().then((arg) =>{
        console.log('Connection Status : ' + arg);
    }).catch((error) =>{
        console.log(error);
    });

    next();
}

const app = express();

app.use(express.json());
app.use(middleware);
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json());

app.use("/", Controller)

app.get("/connect",middleware,(req,res) =>{
    res.send("request recieved")
})
app.post('/upload', upload, uploadImage);

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
  });
