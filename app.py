from flask import Flask, render_template, request
from moviepy.editor import VideoFileClip
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    video_file = request.files['video_file']
    output_location = request.form['output_location']
    
    # Create a temporary file for the video
    temp_video_path = tempfile.mktemp(suffix='.mp4')
    
    try:
        # Save the uploaded video file to the temporary path
        video_file.save(temp_video_path)
        
        # Extract audio from the video
        video = VideoFileClip(temp_video_path)
        audio = video.audio
        audio.write_audiofile(output_location)

    except Exception as e:
        return f'An error occurred: {str(e)}'
    
    finally:
        # Close the video and audio objects if they were opened
        if 'audio' in locals():
            audio.close()
        if 'video' in locals():
            video.close()

        # Clean up temporary video file
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
    
    return 'Audio extracted successfully!'

if __name__ == '__main__':
    app.run(debug=True)