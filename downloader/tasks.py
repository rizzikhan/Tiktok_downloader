

# tasks.py
import yt_dlp
import cloudinary.uploader
import os
from celery import shared_task

@shared_task
def download_tiktok_video(url):
    print(f"Task: Starting download for URL: {url}")
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)

        print(f"Task: Download complete. Uploading {filename} to Cloudinary.")
        upload_result = cloudinary.uploader.upload(filename, resource_type="video")

        print(f"Task: Uploaded to Cloudinary. Public ID: {upload_result.get('public_id')}.")
        os.remove(filename)
        print(f"Task: Deleted local file {filename}.")

        return upload_result.get('secure_url'), upload_result.get('public_id')

@shared_task
def delete_video_from_cloudinary(public_id):
    print(f"Task: Deleting video with Public ID: {public_id} from Cloudinary.")
    cloudinary.uploader.destroy(public_id, resource_type="video")
    print(f"Task: Video with Public ID: {public_id} deleted from Cloudinary.")