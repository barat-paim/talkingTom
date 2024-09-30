import json

# Read the transcript from the text file
with open('transcript_1.txt', 'r') as file:
    lines = file.readlines()

# Initialize the dialogue list
dialogue = []

# Process each line in the transcript
for line in lines:
    # Split the line into timestamp and text
    parts = line.split('\t')
    if len(parts) == 2:
        timestamp, text = parts
        # Determine the speaker based on the text content
        if text.startswith('- '):
            speaker = "Lex Fridman"
            text = text[2:].strip()
        else:
            speaker = "Perplexity CEO"
            text = text.strip()
        
        # Add the turn to the dialogue list
        dialogue.append({
            "speaker": speaker,
            "text": text
        })

# Write the dialogue to a JSON file
with open('lex_arvind.json', 'w') as json_file:
    json.dump(dialogue, json_file, indent=4)

print("Transcript has been converted to lex_arvind.json")