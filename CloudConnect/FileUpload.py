import cloudinary
import cloudinary.uploader
import os

def upload_file_to_drive(file, candidate_id):
    cloudinary.config(
        cloud_name= os.getenv("CLOUD_NAME"),
        api_key = os.getenv("API_KEY"),
        api_secret = os.getenv("API_SECRET")
    )
    result = cloudinary.uploader.upload (
        file,
        folder = "recruit_agent_resumes",
        public_id = f"{candidate_id}_resume",
        resource_type = "raw"
    )
    return result.get("secure_url")