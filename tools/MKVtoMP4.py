import subprocess

# Define the source and destination file paths
source_path = "D:/Bambi Videos/Refined/2023/Bambi Model 69 (Perfectly Perfect).mkv"
destination_path = "D:/Bambi Videos/Refined/2024/April/Bambi Model 69 NFT.mp4"

# Command to convert video without losing quality
command = [
    "ffmpeg",
    "-i", source_path,  # Input file
    "-c:v", "copy",  # Copy the video stream
    "-c:a", "copy",  # Copy the audio stream
    destination_path  # Output file
]

# Execute the command
subprocess.run(command)
