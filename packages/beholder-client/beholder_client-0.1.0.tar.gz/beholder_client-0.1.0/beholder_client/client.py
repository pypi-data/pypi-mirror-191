from io import BytesIO
from PIL import Image

from beholder_client.ops import capture


class BeholderClient:
    """
    Beholder API client.
    """
    
    def __init__(self, base_url: str, x_api_key: str):
        """
        Args:
            base_url: Base URL of the Beholder server.
            x_api_key: Beholder API key.
        """
        self._base_url = base_url.rstrip('/')
        self._x_api_key = x_api_key
        
    def capture_raw(self, video_url: str, elapsed_time_millis: int) -> bytes:
        """
        Capture a frame from a video and return the raw bytes.
        
        Args:
            video_url: URL of the video to capture a frame from.
            elapsed_time_millis: Time in milliseconds since the start of the video.
        
        Returns:
            Raw bytes of the image.
        """
        return capture(self._base_url, video_url, elapsed_time_millis, self._x_api_key)
    
    def capture(self, video_url: str, elapsed_time_millis: int) -> Image.Image:
        """
        Capture a frame from a video and parse it into a PIL Image.
        
        Args:
            video_url: URL of the video to capture a frame from.
            elapsed_time_millis: Time in milliseconds since the start of the video.
        
        Returns:
            Parsed image.
        """
        image_bytes = self.capture_raw(video_url, elapsed_time_millis)
        return Image.open(BytesIO(image_bytes))
