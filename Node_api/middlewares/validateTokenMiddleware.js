const axios = require("axios");

// Flask validation endpoint
const FLASK_VALIDATE_URL = "http://127.0.0.1:2999/auth/validate";

/**
 * Middleware to validate the Authorization token using Flask API
 */
const validateTokenMiddleware = async (req, res, next) => {
  const authHeader = req.headers["authorization"];

  // Check if the Authorization header is missing or empty
  if (!authHeader || !authHeader.trim()) {
    return res.status(401).json({ message: "Unauthorized: Authorization token is required" });
  }

  try {
    // Send the token to the Flask validation endpoint
    const response = await axios.post(
      FLASK_VALIDATE_URL,
      {}, // Flask API does not expect a body
      {
        headers: { Authorization: authHeader },
      }
    );

    // If the Flask service validates the token successfully, move to the next middleware
    if (response.status === 200) {
      return next();
    }
  } catch (err) {
    // Handle specific Flask service responses
    if (err.response) {
      if (err.response.status === 401) {
        // Invalid or expired token
        return res.status(401).json({ message: "Unauthorized: Invalid or expired Authorization token" });
      }
      if (err.response.status === 403) {
        // Token is forbidden
        return res.status(403).json({ message: "Forbidden: Authorization token does not have the required permissions" });
      }
    }

    // Handle other errors (e.g., Flask service unavailable or unexpected errors)
    return res.status(500).json({ message: "Validation service error", error: err.message });
  }
};

module.exports = validateTokenMiddleware;
