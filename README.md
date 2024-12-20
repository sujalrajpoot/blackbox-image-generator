# Blackbox Image Generator

A Python library that provides a clean, object-oriented interface for generating images using the Blackbox AI API. This library encapsulates the complexity of API interactions and provides robust error handling for a seamless image generation experience.

## Features

- Object-oriented design with clean separation of concerns
- Comprehensive error handling with custom exceptions
- Type hints for better code maintainability and IDE support
- Flexible configuration options for API endpoints and headers
- Automatic image downloading and saving
- Status tracking through enumerated states

## Installation

1. Clone this repository:
```bash
git clone https://github.com/sujalrajpoot/blackbox-image-generator.git
cd blackbox-image-generator
```

2. Install the required dependencies:
```bash
pip install requests
```

## Usage

Here's a simple example of how to use the BlackboxImageGenerator:

```python
from blackbox_image_generator import BlackboxImageGenerator

# Initialize the generator
image_generator = BlackboxImageGenerator()

# Generate an image
try:
    prompt = "a beautiful mountain landscape at sunset"
    result = image_generator.generate_image(
        prompt=prompt,
        output_image_path="landscape.jpg"
    )
    print(result)  # Will print "Image Generated Successfully" on success
except BlackboxAPIError as e:
    print(f"Error: {e}")
```

## Architecture

The library is built with the following components:

1. **Custom Exceptions**:
   - `BlackboxAPIError`: Base exception for all API-related errors
   - `ImageDownloadError`: Specific to image download failures
   - `ImageGenerationError`: Handles image generation failures
   - `StatusCodeError`: Manages unexpected HTTP status codes

2. **Status Tracking**:
   - `ImageGenerationStatus`: Enum class for tracking generation status
   - Provides clear status messages for different outcomes

3. **Abstract Base Class**:
   - `ImageGenerator`: Defines the interface for image generation
   - Allows for easy implementation of alternative image generation services

4. **Concrete Implementation**:
   - `BlackboxImageGenerator`: Implements the Blackbox API integration
   - Handles API communication, image downloading, and error management

## Error Handling

The library implements a comprehensive error handling system:

```python
try:
    result = image_generator.generate_image(prompt)
except ImageDownloadError as e:
    print(f"Failed to download image: {e}")
except ImageGenerationError as e:
    print(f"Failed to generate image: {e}")
except StatusCodeError as e:
    print(f"API request failed: {e}")
except BlackboxAPIError as e:
    print(f"General API error: {e}")
```

## Disclaimer

⚠️ **Important Notice**: This code is provided strictly for educational purposes only. It is designed to demonstrate object-oriented programming principles, API integration patterns, and error handling techniques in Python. The use of this code to harm, disrupt, or disrespect Blackbox.ai or its services is strictly prohibited. Users are responsible for ensuring their use of this code complies with Blackbox.ai's terms of service and API usage guidelines.

---

Created with ❤️ by **Sujal Rajpoot**

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
