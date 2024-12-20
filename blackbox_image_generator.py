from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import requests


# Define custom exceptions
class BlackboxAPIError(Exception):
    """Custom exception for errors related to the Blackbox API."""
    pass


class ImageDownloadError(BlackboxAPIError):
    """Custom exception for errors during image download."""
    pass


class ImageGenerationError(BlackboxAPIError):
    """Custom exception for errors during image generation."""
    pass


class StatusCodeError(BlackboxAPIError):
    """Custom exception for unexpected status codes."""
    pass


# Enum for Image Generation Status
class ImageGenerationStatus(Enum):
    SUCCESS = "Image Generated Successfully"
    ERROR_NO_URL = "No Image download URL found"
    ERROR_EXCEPTION = "An exception occurred"


# Abstract Base Class for Image Generation
class ImageGenerator(ABC):
    """Abstract base class for image generation services."""

    @abstractmethod
    def generate_image(self, prompt: str, output_image_path: str) -> str:
        """Generates an image based on a provided prompt."""
        pass


@dataclass
class BlackboxImageGenerator(ImageGenerator):
    """Concrete class that implements image generation using the Blackbox API."""
    
    api_url: str = "https://www.blackbox.ai/api/chat"
    headers: Dict[str, str] = None

    def __post_init__(self):
        if self.headers is None:
            self.headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.7',
                'content-type': 'application/json',
                'origin': 'https://www.blackbox.ai',
                'priority': 'u=1, i',
                'referer': 'https://www.blackbox.ai/',
                'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }
    def generate_image(self, prompt: str, output_image_path: str = "blackbox_generated_image.jpg", prints: bool = True) -> str:
        """
        Initiates the process of generating an image based on a given prompt using the Blackbox API and saves the image to a specified file path.

        Args:
            prompt (str): The text-based prompt that serves as the basis for the image generation.
            output_image_path (str, optional): The file path where the generated image will be saved. Defaults to "blackbox_generated_image.jpg".
            prints (bool, optional): A flag indicating whether to print the extracted image URL. Defaults to True.

        Returns:
            str: A status message indicating the outcome of the image generation process, including success or failure.
        """
        json_data = {
            'messages': [
                {
                    'id': '',
                    'content': prompt,
                    'role': 'user',
                },
            ],
            'id': '',
            'previewToken': None,
            'userId': None,
            'codeModelMode': True,
            'agentMode': {},
            'trendingAgentMode': {},
            'isMicMode': False,
            'userSystemPrompt': None,
            'maxTokens': 1024,
            'playgroundTopP': None,
            'playgroundTemperature': None,
            'isChromeExt': False,
            'githubToken': '',
            'clickedAnswer2': False,
            'clickedAnswer3': False,
            'clickedForceWebSearch': False,
            'visitFromDelta': False,
            'mobileClient': False,
            'userSelectedModel': None,
            'validated': '00f37b34-a166-4efb-bce5-1312d87f2f94',
            'imageGenerationMode': True,
            'webSearchModePrompt': False,
            'deepSearchMode': False,
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=json_data)
            response.raise_for_status()
            image_url = response.content.decode('utf-8')[4:-1]
            if image_url and image_url.startswith('https://'):
                if prints:print(f"Image URL: {image_url}")
                self._download_image(image_url, output_image_path)
                return ImageGenerationStatus.SUCCESS.value
            else:
                raise ImageGenerationError("No Image URL found.")
        
        except requests.exceptions.RequestException as e:
            raise StatusCodeError(f"Request failed: {e}")
        except ImageGenerationError as e:
            raise e
        except Exception as e:
            raise ImageGenerationError(f"An unexpected error occurred: {e}")

    def _download_image(self, image_url: str, output_image_path: str) -> None:
        """
        Downloads an image from the given URL and saves it to the specified file path.
        
        Args:
            image_url (str): The URL of the image to be downloaded.
            output_image_path (str): The file path where the image will be saved.
        
        Raises:
            ImageDownloadError: If there is an error downloading the image.
        """
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(output_image_path, "wb") as file:
                    file.write(response.content)
            else:
                raise ImageDownloadError("Failed to download the image.")

        except requests.exceptions.RequestException as e:
            raise ImageDownloadError(f"Error downloading image: {e}")

# Example usage
if __name__ == "__main__":
    prompt = "a beautiful girl"
    image_generator = BlackboxImageGenerator()

    try:
        result = image_generator.generate_image(prompt)
        print(result)
    except BlackboxAPIError as e:
        print(f"Error: {e}")
