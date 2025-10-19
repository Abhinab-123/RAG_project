# from pydub import AudioSegment

# # Load audio
# audio = AudioSegment.from_file("audios/9.mp4_Id & Classes in HTML .mp3")

# # Trim from 10 seconds to 30 seconds
# start_time = 0 * 1000  # pydub uses milliseconds
# end_time = 10 * 1000
# trimmed_audio = audio[start_time:end_time]

# # Save trimmed audio
# trimmed_audio.export("audios/simple_trimmed.mp3", format="mp3")
import subprocess

# Check NVIDIA GPU
print(subprocess.getoutput("nvidia-smi"))

# Check CUDA version
print(subprocess.getoutput("nvcc --version"))

