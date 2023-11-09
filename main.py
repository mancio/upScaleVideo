import os
import sys
import subprocess

one_k = ["1280", "720p"]
two_k = ["2048", "2K"]
four_k = ["3840", "4K"]

very_sharp = "unsharp=7:7:2.0:5:5:1.0"
sharp = "unsharp=5:5:0.8:3:3:0.4"
smooth = "unsharp=7:7:-2.0"


def upscale_video_to_4k(input_path, output_path):
    # command = [
    #     'ffmpeg',
    #     '-i', input_path,        # Input file
    #     "-vf", "scale=3840:-1",  # Scaling
    #     "-vcodec", "h264_nvenc",
    #     output_path,             # Output file
    #     "-y"
    # ]

    command = [
        'ffmpeg',
        # '-hwaccel', 'cuda',                # Enable CUDA hardware acceleration
        '-i', input_path,  # Input file path
        '-vf', f'deblock=1,scale={one_k[0]}:-2:flags=lanczos',  # Use NPP scaling with Lanczos.
               # f'gblur=sigma=2.0',  # increase blur effect
        # f'{smooth}',  # -2 maintains aspect ratio
        '-c:v', 'h264_nvenc',  # Specify Nvidia's hardware-accelerated H.264 video codec
        '-preset', 'slow',  # Preset for the encoder speed/quality tradeoff
        '-profile:v', 'high',  # Specify H.264 profile level
        '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
        # '-rc', 'vbr',  # Rate control method: Variable Bit Rate
        # '-cq', '19',  # Constant Quality for VBR mode
        # '-qmin', '18',  # Minimum quantizer scale
        # '-qmax', '23',  # Maximum quantizer scale
        # '-maxrate', '50M',  # Maximum bitrate
        # '-bufsize', '100M',  # Buffer size
        '-acodec', 'copy',  # Copy audio stream without re-encoding
        output_path,  # Output file path
        '-y',  # Overwrite output file without asking
        '-loglevel', 'error',  # This will make ffmpeg not verbose
    ]

    # Print the entire command as a single string
    full_command = ' '.join(command)
    print("Executing command:", full_command)

    subprocess.run(command)


def process_directory(directory):
    # Create an "upscaled" subdirectory
    output_directory = os.path.join(directory, "upscaled")
    os.makedirs(output_directory, exist_ok=True)

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}-{one_k[1]}.mp4")
            print(f"Processing {filename}...")
            upscale_video_to_4k(input_path, output_path)
            print(f"Saved upscaled video to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <directory_path>")
        sys.exit(1)

    process_directory(sys.argv[1])
