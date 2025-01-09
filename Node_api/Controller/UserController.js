const router= require("express").Router();
const Camera= require('../Model/UserModel')
const validateTokenMiddleware = require("../middlewares/validateTokenMiddleware");
const axios= require('axios')

router.post("/signin", async (req, res) => {
    const { email_id, password } = req.body;
  
    // Validate input
    if (!email_id || !password) {
      return res.status(400).json({ message: "Email and password are required." });
    }
  
    const SIGNIN_URL = "http://127.0.0.1:2999/signin";
  
    try {
      // Send request to Flask's /signin endpoint
      const flaskResponse = await axios.post(SIGNIN_URL, { email_id, password });
  
      if (flaskResponse.data.message === "success") {
        // Return successful response with user credentials
        return res.status(201).json({
          message: "Signin successful",
          credentials: flaskResponse.data.credentials,
        });
      } else {
        // Handle Flask failure response
        return res.status(flaskResponse.status).json(flaskResponse.data);
      }
    } catch (error) {
      // Handle errors from Flask API
      return res.status(error.response?.status || 500).json({
        message: error.response?.data?.message || "Internal Server Error",
        error: error.message,
      });
    }
  });
  
router.get("/cameras/:camera_id/feed",validateTokenMiddleware, async (req, res) => {
   const { camera_id } = req.params;
    // Validate input
   if (!camera_id) {
    return res.status(400).json({ message: "camera_id is required." });
    }
  
   try {
      // Fetch camera details from MongoDB
   const camera = await Camera.findOne({ camera_id: camera_id });
  
     if (!camera) {
        return res.status(404).json({
          message: "Camera not found",
        });
      }
  
      // Return the camera feed URL
    return res.status(200).json({
        camera_feed_url: camera.camera_feed_url,
      });
    } catch (error) {
      // Handle errors
      return res.status(500).json({
        message: "Internal Server Error",
        error: error.message,
      });
    }
  });
  
module.exports = router;