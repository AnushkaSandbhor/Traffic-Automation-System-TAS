const mongoose = require("mongoose");

const cameraSchema = mongoose.Schema({
    camera_id:{
        type:String,
        required:true,
        unique:true
    },
    location:{
        type:String,
        required:true
    },
    camera_feed_url:{
        type:String,
        required:true
    },
    last_updated:{
        type:Date,
        default:Date.now()
    },
    violation_images:{
        type: Array
    },
    violation_videos:{
        type:Array
    },
    tags:{
        type:Array
    }
});

mongoose.model("camera_footage",cameraSchema);

module.exports=mongoose.model("camera_footage")