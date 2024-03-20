import os
import csv
from pydub import AudioSegment
import speech_recognition as sr
from tqdm import tqdm

# Directory containing your .m4a files
directory_path = 'C:/Users/guillermo.pereira/Desktop/interviews_datapop'

AUDIO_PORTIONS = 300

# Initialize the recognizer
r = sr.Recognizer()


# Function to split audio file into chunks
def split_audio(audio, chunks=50):
    length = len(audio)
    chunk_length = length // chunks
    return [audio[i:i + chunk_length] for i in range(0, length, chunk_length)]


# Function to generate a new filename if the original exists
def generate_new_filename(original_path):
    base, extension = os.path.splitext(original_path)
    version = 1
    new_path = f"{base}_version_{version}{extension}"
    while os.path.exists(new_path):
        version += 1
        new_path = f"{base}_version_{version}{extension}"
    return new_path


# Open a CSV file to log unsuccessful portions
error_log_path = os.path.join(directory_path, "transcription_errors.csv")
with open(error_log_path, "w", newline='', encoding='utf-8') as log_file:
    csv_writer = csv.writer(log_file, delimiter='|')
    csv_writer.writerow(["Source Audio File", "Unsuccessful Portion", "Start Timestamp", "End Timestamp", "Duration",
                         "Error Description"])

filenames = os.listdir(directory_path)

for filename in filenames:
    if filename.endswith(".wav"):
        full_path = os.path.join(directory_path, filename)
        print(f"Processing {filename}...")

        # Load the audio file with pydub
        audio = AudioSegment.from_wav(full_path)

        # Split the audio file into portions
        portions = split_audio(audio, AUDIO_PORTIONS)

        full_text = []

        # Process each portion with progress bar
        for i in tqdm(range(len(portions)), desc=f"Transcribing {filename}"):
            portion = portions[i]
            portion_duration = len(portion) / 1000.0  # Duration in seconds
            start_timestamp = i * portion_duration
            end_timestamp = start_timestamp + portion_duration

            # Export portion to a temporary WAV file
            portion_path = f"temp_portion_{i}.wav"
            portion.export(portion_path, format="wav")

            # Recognize the portion
            with sr.AudioFile(portion_path) as source:
                audio_data = r.record(source)
                try:
                    # Transcribe the audio
                    text = r.recognize_google(audio_data)
                    full_text.append(text)
                except Exception as e:
                    # Log the error
                    csv_writer.writerow([filename, i + 1, start_timestamp, end_timestamp, portion_duration, str(e)])
                    print(f"Error processing portion {i + 1} of {filename}: {e}")

            # Clean up the temporary file
            os.remove(portion_path)

        # Join and save the transcribed text
        joined_text = " ".join(full_text)
        text_filename = os.path.join(directory_path, filename.replace(".wav", ".txt"))

        # Check if the file exists and generate a new filename if necessary
        if os.path.exists(text_filename):
            text_filename = generate_new_filename(text_filename)

        with open(text_filename, "w") as text_file:
            text_file.write(joined_text)

        print(f"Transcription for {filename} saved to {text_filename}")

print("All processing complete.")