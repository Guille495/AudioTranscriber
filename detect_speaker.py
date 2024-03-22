import os
import spacy
spacy.cli.download("en_core_web_sm")

# Load the English model for spaCy
nlp = spacy.load("en_core_web_sm")

directory_path = 'C:/Users/evelin.lasarga/Desktop/interviews_datapop'

def segment_text(text):
    # Use spaCy for basic sentence segmentation, may not be perfect
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

def assign_speakers(sentences):
    # Alternately assign sentences to Speaker 1 and Speaker 2
    dialogue = []
    # speaker = 1
    for i,sentence in enumerate(sentences):
        dialogue.append(f"Sentence {i+1}: {sentence}")
        # speaker = 1 if speaker == 2 else 2  # Alternate speaker
    return dialogue

for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):
        full_path = os.path.join(directory_path, filename)
        with open(full_path, "r", encoding="utf-8") as file:
            transcript = file.read()

        # Segment the transcript into sentences/phrases
        sentences = segment_text(transcript)

        # Assign sentences to speakers
        dialogue = assign_speakers(sentences)

        # Write the separated dialogue to a new file
        new_filename = os.path.join(directory_path, f"with_speaker_attempted_detection-{filename}")
        with open(new_filename, "w", encoding="utf-8") as file:
            for line in dialogue:
                file.write(line + "\n")

print("Processing complete.")
