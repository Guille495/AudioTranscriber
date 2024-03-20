from pydub import AudioSegment
import os

directory_path = 'C:/Users/guillermo.pereira/Desktop/interviews_datapop'

def split_and_save_audio(file_path):
    # Load the audio file
    audio = AudioSegment.from_wav(file_path)

    # Calculate the length of each split
    split_length = len(audio) // 10

    # Split and save each part
    for i in range(10):
        start = i * split_length
        end = (i + 1) * split_length if i < 9 else len(audio)
        part = audio[start:end]
        part_path = f"{file_path[:-4]}_part{i + 1}.wav"
        part.export(part_path, format="wav")
        print(f"Part {i + 1} saved to {part_path}")

# Iterate through each file in the directory
for filename in ["Audio_Cary_UNICEF_BA.wav"]:
    if filename.endswith(".wav"):
        full_path = os.path.join(directory_path, filename)
        print(f"Processing {filename}...")
        split_and_save_audio(full_path)
