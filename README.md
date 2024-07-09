# Video Editing Microservice

## Setup

### Prerequisites
- Docker
- Docker Compose

### Build and Run
1. Clone the repository:
   ```bash
   git clone https://github.com/alaamohammad04/video_editing.git
   cd video-editing

2. Create a .env file with the following content:

    . Copy the content from .env-example and fill in the required values



3. Build and start the containers:
    docker-compose up --build

The application should be running at http://localhost:8000.

## API Endpoints
1. Upload Video:
    - URL: /api/upload/
    - Method: POST
    - Parameters: 
      - file : The video file to be uploaded.


2. Add Text to Video:
    - URL: /api/add-text/
    - Method: POST
    - Parameters: video_name, text, x, y, t, d, s
       - video_name: The name of the video file.
       - text: The text to be added.
       - x: The x-coordinate for the text position.
       - y: The y-coordinate for the text position.
       - t: The start time in seconds when the text should appear.
       - d: The duration in seconds for which the text should appear.
       - s: The font size of the text

3. Download Video:
    - URL: /api/download/<task_id>/
    - Method: GET

## For Testing
python mange.py test