from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from .models import ProcessingTasks


def process_video(task_id, video_path, output_path, text, x, y, t, d, s):
    try:
        # Get the processing task
        task = ProcessingTasks.objects.get(uid=task_id)
    except ProcessingTasks.DoesNotExist:
        print(f"Processing task {task_id} does not exist.")
        return
    try:
        # Load the video
        video = VideoFileClip(video_path)

        # Create a text image using PIL
        img = Image.new("RGBA", (video.w, video.h), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", s)
        draw.text((x, y), text, font=font, fill="white")

        # Convert the PIL image to a moviepy ImageClip
        txt_clip = ImageClip(np.array(img)).set_duration(d).set_start(t).set_pos((x, y))

        # Overlay the text clip on the video
        video = CompositeVideoClip([video, txt_clip])

        # Write the result to a file
        video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Update the processing task status
        task.status = "Completed"
        task.save()

    except Exception as e:
        print(f"Error processing video: {e}")
        # Update the processing task status
        task.status = "Failed"
        task.save()
