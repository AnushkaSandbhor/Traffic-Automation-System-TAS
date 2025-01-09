const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const { v4: uuidv4 } = require('uuid');
const multer = require('multer');
const Camera = require('../Model/UserModel');

// AWS S3 Configuration
const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

// Multer Middleware
const storage = multer.memoryStorage();
const upload = multer({ storage }).single('image'); // Accept a single file with the key 'image'

// Image Upload Controller Function
const uploadImage = async (req, res) => {
  const { camera_id, violation_type } = req.body; // Extract fields from body
  const file = req.file; // Extract file from Multer middleware

  // Validate the required fields
  if (!camera_id || !violation_type || !file) {
    return res.status(400).json({ error: 'Missing required fields: camera_id, violation_type, or image file.' });
  }

  try {
    // Generate a unique file name using UUID
    const fileKey = `${uuidv4()}-${file.originalname}`;

    // Prepare S3 upload parameters
    const params = {
      Bucket: process.env.AWS_S3_BUCKET_NAME,
      Key: fileKey,
      Body: file.buffer,
      ContentType: file.mimetype,
    };

    // Upload the file to S3 using the PutObjectCommand
    const command = new PutObjectCommand(params);
    await s3Client.send(command);

    // Construct the file URL manually
    const fileUrl = `https://${process.env.AWS_S3_BUCKET_NAME}.s3.${process.env.AWS_REGION}.amazonaws.com/${fileKey}`;

    // Find the camera document in MongoDB
    const camera = await Camera.findOne({ camera_id });
    if (!camera) {
      return res.status(404).json({ error: 'Camera not found.' });
    }

    // Update the camera document with the new image URL and violation type
    camera.violation_images.push(fileUrl);
    camera.tags.push(violation_type);
    camera.last_updated = new Date();
    await camera.save();

    // Send a success response
    res.status(200).json({
      message: 'Image uploaded successfully',
      imageUrl: fileUrl,
    });
  } catch (error) {
    console.error('Error uploading image:', error);
    res.status(500).json({ error: 'An error occurred while uploading the image.' });
  }
};

// Export the middleware and the controller function
module.exports = {
  upload,
  uploadImage,
};
