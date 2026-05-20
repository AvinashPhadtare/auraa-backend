import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)

def upload_image(file) -> str:
    result = cloudinary.uploader.upload(
        file,
        folder="auraa-dishes",
    )
    return result["secure_url"]