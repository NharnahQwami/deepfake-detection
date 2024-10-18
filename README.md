# Deepfake Detection

A web-based application that uses the Hugging Face Vision Transformer (ViT) model to detect potential deepfake images. This tool provides a user-friendly interface for uploading images and receiving real-time analysis of whether an image is likely to be real or fake.

## Features

- 🖼️ Real-time image preview
- 🔍 Deep learning-based image analysis
- 📊 Detailed probability scores
- 📱 Responsive user interface
- ⚡ Fast processing using Hugging Face API
- 🔒 Secure file handling

## Prerequisites

Before running this application, make sure you have:

- Python 3.7 or higher installed
- A Hugging Face account and API key
- `pip` (Python package installer)

## Installation

Clone the repository or download the source code:

```bash
git clone https://github.com/NharnahQwami/deepfake-detection.git
cd deepfake-detector
```
````

Create a virtual environment (recommended):

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install flask requests Pillow
```

Set up your Hugging Face API key:

1. Sign up at Hugging Face
2. Go to Settings → Access Tokens
3. Create a new token with READ access
4. Replace `YOUR_API_KEY_HERE` in `app.py` with your actual API key

## Project Structure

```plaintext
deepfake_detector/
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   └── index.html     # Main user interface
├── uploads/           # Temporary file storage (created automatically)
└── README.md          # Project documentation
```

## Usage

Start the Flask application:

```bash
python app.py
```

Open your web browser and navigate to:

```plaintext
http://localhost:5000
```

Use the application:

1. Click "Choose File" to select an image
2. Preview the selected image
3. Click "Analyze Image" to detect if it's a deepfake
4. View the results with confidence scores

## API Integration

The application uses the Hugging Face API endpoint:

```python
API_URL = "https://api-inference.huggingface.co/models/Wvolf/ViT_Deepfake_Detection"
```

The model used is `Wvolf/ViT_Deepfake_Detection`, which is specifically trained for deepfake detection.

## Results Interpretation

The tool provides:

- Binary classification (Real/Fake)
- Confidence score for the prediction
- Detailed probability breakdown for each class
- Visual representation of confidence using a progress bar

## Security Features

- Secure file handling with `werkzeug.utils.secure_filename`
- Automatic file cleanup after processing
- File size limits (16MB max)
- Allowed file extensions: `.png`, `.jpg`, `.jpeg`

## Rate Limits

Please note that the free tier of Hugging Face API has rate limits:

- Requests per day are limited
- The first request might be slower as the model loads
- Consider upgrading to a paid plan for production use

## Error Handling

The application includes comprehensive error handling for:

- Invalid file types
- API connection issues
- Processing errors
- File handling errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Future Improvements

Potential enhancements that could be added:

- Batch processing of multiple images
- Support for video analysis
- Additional AI models for comparison
- Result history storage
- User authentication
- API documentation for external integration

## Acknowledgments

- Vision Transformer model by Wvolf on Hugging Face
- Flask framework for web application
- Hugging Face for AI model hosting

## Support

If you encounter any issues or have questions:

- Check the error messages in the console
- Verify your API key is correct
- Ensure all dependencies are installed
- Check your internet connection
- Create an issue in the repository

**Note:** This tool is for educational and research purposes. While it can help identify potential deepfakes, it should not be the sole determining factor in verifying image authenticity.
```
