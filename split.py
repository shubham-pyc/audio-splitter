import os
import subprocess
import re
import hashlib

def split_audio_into_chunks(input_file, output_dir, chunk_size_mb=5):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory '{output_dir}' created.")
    # Get the file size of the audio
    file_size = os.path.getsize(input_file)  # in bytes
    chunk_size_bytes = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    
    # Get the bitrate of the audio file using ffmpeg
    command = ['ffmpeg', '-i', input_file, '-f', 'ffmetadata', '-']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    metadata = result.stderr.decode()
    # print(metadata)
    
    # Extract the bitrate from metadata
    bitrate = None
    pattern = r"bitrate:\s*(\d+)"
    match = re.search(pattern, metadata)
    if match:
        bitrate = int(match.group(1))

        print(f"Extracted bitrate: {bitrate}")

    # for line in metadata.splitlines():
    #     if 'bitrate' in line:
    #         bitrate = int(line.split(":")[1].strip().split(" ")[0])  # Extract bitrate in kbps
    #         break
    if bitrate is None:
        print("Could not determine bitrate.")
        return
    
    # Calculate the duration for each chunk based on bitrate and desired chunk size
    duration_per_chunk = (chunk_size_bytes * 8) / (bitrate * 1000)  # in seconds
    
    # Split the file into chunks using ffmpeg
    total_duration_command = ['ffmpeg', '-i', input_file]
    result = subprocess.run(total_duration_command, stderr=subprocess.PIPE)
    total_duration_output = result.stderr.decode()
    pattern = r"Duration:\s*([\d]{2}):([\d]{2}):([\d]{2})\.([\d]+),"
    match = re.search(pattern, total_duration_output)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        milliseconds = int(match.group(4))
        print(f"Extracted Duration: {hours}:{minutes}:{seconds}.{milliseconds}")
    
    
   
    total_seconds = int(hours * 3600 + minutes * 60 + seconds)
    
    # Split the audio into chunks of the calculated duration
    num_chunks = (total_seconds // duration_per_chunk) + 1
    
    for i in range(int(num_chunks)):
        start_time = i * duration_per_chunk
        output_file = os.path.join(output_dir, f"chunk_{i+1}.mp3")
        command = [
            'ffmpeg', '-i', input_file, '-ss', str(start_time), '-t', str(duration_per_chunk),
            '-acodec', 'copy', output_file
        ]
        subprocess.run(command)
        print(f"Created chunk {i+1}: {output_file}")


def combine_audio_chunks(chunks_dir, output_file):
    # Get a list of all chunk files in the specified directory
    chunk_files = sorted([f for f in os.listdir(chunks_dir) if f.startswith("chunk_")])
    # Check if there are no chunks found
    if not chunk_files:
        print("No chunk files found in the specified directory.")
        return
    
    # Create a temporary text file listing the chunks
    concat_file = os.path.join(chunks_dir, 'filelist.txt')
    with open(concat_file, 'w') as f:
        for chunk in chunk_files:
            # chunk_path = os.path.join(chunks_dir, chunk)
            f.write(f"file '{chunk}'\n")

    # Use ffmpeg to concatenate the chunks
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output_file]
    
    try:

        subprocess.run(command, check=True)
        print(f"Successfully combined chunks into {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining audio chunks: {e}")
    finally:
        # Clean up the temporary file list
        os.remove(concat_file)

# Usage example
input_audio = 'sample.mp3'
output_directory = 'output_chunks'
split_audio_into_chunks(input_audio, output_directory)


chunks_directory = 'output_chunks'  # Directory containing chunk files
output_audio = 'combined_audio.mp3'  # Output file name
combine_audio_chunks(chunks_directory, output_audio)


