import ffmpeg


def create_video(image_folder, output_video, frame_rate, audio_path, final_output, resolution=(1920, 1080)):
    try:
        (
            ffmpeg
            .input(f'{image_folder}/*.jpg', pattern_type='glob', framerate=frame_rate)
            .filter('scale', width=resolution[0], height=resolution[1])
            .output(output_video, vcodec='libx264', pix_fmt='yuv420p')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print("Video created successfully.")
    except ffmpeg.Error as e:
        print("Error creating video:", e.stderr.decode())
        raise
    try:
        video = ffmpeg.input(output_video)
        audio = ffmpeg.input(audio_path)
        (
            ffmpeg
            .output(video, audio, final_output, vcodec='libx264', acodec='aac', strict='experimental')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print("Audio added successfully, final video created.")
    except ffmpeg.Error as e:
        print("Error adding audio:", e.stderr.decode())
        raise
resolution = (1920, 1080)
image_folder = '/home/bob/sdavsadfasdfdasf'
output_video = 'output_video.mp4'
final_output = 'final_video_with_audio.mp4'
frame_rate = 0.5  # 2 seconds per image
audio_path = '/home/bob/sdavsadfasdfdasf/vid/Maktab 1 sinf qoshigi.mp3'  # Ensure this is correct

create_video(image_folder, output_video, frame_rate, audio_path, final_output, resolution)
