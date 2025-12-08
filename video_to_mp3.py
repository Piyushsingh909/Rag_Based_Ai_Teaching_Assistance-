import os
import subprocess

# --- Configuration ---
input_dir = "videos"      # The folder where your .mp4 files are
output_dir = "mp3_audio"  # The folder where you want the .mp3 files to go
# ---------------------

# 1. Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# 2. Get the list of files from your input directory
try:
    files = os.listdir(input_dir)
except FileNotFoundError:
    print(f"Error: Input directory '{input_dir}' not found.")
    print("Please make sure your videos are in a folder named 'videos'.")
    exit()

# 3. Loop through each file
for file in files:
    # 4. Check if it's an .mp4 file (or add other video formats)
    if file.endswith(".mp4"):
        
        # This is a safer way to get the name without the extension
        lecture_name = os.path.splitext(file)[0]
        
        # Define the full path for the input and output files
        input_file = os.path.join(input_dir, file)
        output_file = os.path.join(output_dir, f"{lecture_name}.mp3")

        print(f"--- Converting: {file} ---")

        # 5. This is the FFmpeg command
        command = [
            "ffmpeg",
            "-i", input_file,    # Input file
            "-q:a", "0",         # Use high-quality VBR (Variable Bitrate)
            output_file          # Output file
        ]

        # 6. Run the command
        try:
            subprocess.run(command, check=True)
            print(f"Successfully converted to: {output_file}\n")
        except FileNotFoundError:
            print("\n*** ERROR: FFmpeg not found! ***")
            print("Please install FFmpeg and make sure it's in your system's PATH.")
            exit()
        except subprocess.CalledProcessError:
            print(f"Error during conversion of {file}. Skipping.\n")

print("--- All conversions complete! ---")