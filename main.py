import subprocess

# Define the paths to the scripts
audio_transcriber_script = 'audio_transcriber.py'
detect_speaker_script = 'detect_speaker.py'

# Define the Python interpreter to use, for example, 'python', 'python3', or a full path to a Python executable
python_interpreter = 'python'

def run_script(script_name):
    """Runs a Python script using the subprocess module."""
    try:
        result = subprocess.run([python_interpreter, script_name], check=True, capture_output=True, text=True)
        print(f"Successfully ran {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")


def main():
    # Run the audio transcriber script
    run_script(audio_transcriber_script)

    # Then, run the detect speaker script
    run_script(detect_speaker_script)


if __name__ == '__main__':
    main()
