import os
import subprocess


def make_command_string(input_video: str, output_video: str, overlay_text: str) -> str:
    """Function to create a command string for FFmpeg."""

    #  Prepare the text filter
    text_filter = f"format=yuv420p,scale=1280:720,drawtext=text='{overlay_text}':x=if(eq(mod(n\\,108)\\,0)\\,sin(random(1))*w\\,x):y=if(eq(mod(n\\,108)\\,0)\\,sin(random(1))*h\\,y):fontsize=74:alpha=0.3:fontfile='arial.ttf':fontcolor=white"

    # Command for FFMPEG
    command = [
        "ffmpeg.exe",
        "-i", input_video.replace("&", "^&"),  # Change '&' to '^&' to avoid issues with the command line
        "-y",
        "-vf", text_filter,
        "-crf", "25.0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "veryfast",
        output_video.replace("&", "^&")
    ]

    command_string = subprocess.list2cmdline(command)
    return command_string


def watermark_adder(mapping: list, output_folder_path: str) -> None:
    """Function to add watermark to the selected videos."""
    # Initialize the command string
    command = 'cmd /k echo start & powershell -Command \"[console]::beep(600,700)\"'

    for overlay_text, input_path in mapping:
        # Prepare the input and output paths
        input_video_path = input_path

        # Prepare the output path
        output_video_name = os.path.splitext(os.path.basename(input_path))[0]
        output_video_path = os.path.join(output_folder_path, overlay_text, f"{output_video_name}.mp4")

        # Create the output directory if it does not exist
        os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

        if os.path.exists(input_video_path):
            command += " & " + make_command_string(input_video_path, output_video_path, overlay_text)
        else:
            print(f"File {input_video_path} not found!")

    try:
        command += " & powershell -Command \"[console]::beep(200,700)\" & echo Finished applying watermarks"
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

    except subprocess.CalledProcessError as e:
        print(f"Error while processing video: {e}")
