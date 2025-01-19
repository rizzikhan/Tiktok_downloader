
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import download_tiktok_video, delete_video_from_cloudinary



class DownloadVideoView(APIView):
    def post(self, request):
        url = request.data.get('url')
        print("Views: Received download request for URL:", url)

        if not url:
            return Response({'error': 'No URL provided'}, status=400)

        try:
            # Process video download
            video_url, public_id = download_tiktok_video(url)
            print("Views: Video downloaded and uploaded to Cloudinary. Public ID:", public_id)

            # Schedule video deletion
            delete_video_from_cloudinary.apply_async((public_id,), countdown=60)  # 60 seconds
            print("Views: Video deletion scheduled for Public ID:", public_id)

            return Response({
                'message': 'Download ready!',
                'download_url': video_url,
                'public_id': public_id
            })
        except Exception as e:
            print("Views: Error during video processing:", e)
            return Response({'error': str(e)}, status=500)


class DeleteVideoView(APIView):
    def post(self, request):
        public_id = request.data.get('public_id')
        print(f"View: Received request to delete video with Public ID: {public_id}")

        if not public_id:
            print("View: No Public ID provided in request.")
            return Response({'error': 'No Public ID provided'}, status=400)

        delete_video_from_cloudinary(public_id)
        return Response({'message': 'Video deleted from Cloudinary'})


class HomePageView(TemplateView):
    template_name = "downloader/index.html"
