use('traffic_control_test');
 
db.camera_footages.insertMany([
    {
        "camera_id": "CAM001",
        "location": "Main Street Intersection",
        "camera_feed_url": "https://sprint-awsbucket.s3.us-east-2.amazonaws.com/video1.mp4",
        "last_updated": new Date(),
        "violation_images": [
            "https://sprint-awsbucket.s3.us-east-2.amazonaws.com/DALL%C2%B7E-2024-12-22-18.15.jpg"
        ],
        "violation_videos": [
            "https://sprint-awsbucket.s3.us-east-2.amazonaws.com/video1.mp4"
        ],
        "tags": ["red_light_violation", "speeding"]
    },
    {
        "camera_id": "CAM002",
        "location": "Airport Road",
        "camera_feed_url": "https://sprint-awsbucket.s3.us-east-2.amazonaws.com/video2.mp4",
        "last_updated": new Date(),
        "violation_images": [
            "https://sprint-awsbucket.s3.us-east-2.amazonaws.com/DALL%C2%B7E-2024-12-22-18.23.jpg"
        ],
        "violation_videos": [
            "https://sprint-awsbucket.s3.us-east-2.amazonaws.com/video2.mp4"
        ],
        "tags": ["illegal_lane_change"]
    },
    {
        "camera_id": "CAM003",
        "location": "Downtown Square",
        "camera_feed_url": "https://sprint-awsbucket.s3.us-east-2.amazonaws.com/video3.mp4",
        "last_updated": new Date(),
        "violation_images": [],
        "violation_videos": [],
        "tags": ["no_violations"]
    }
]);