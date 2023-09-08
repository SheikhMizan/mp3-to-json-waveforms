import requests
import json
import numpy as np
from pydub import AudioSegment
import io

# Function to convert audio to waveform JSON
def audio_to_waveform_json(audio_link, output_file):
    # Download the audio file
    audio_response = requests.get(audio_link)
    if audio_response.status_code != 200:
        print("Failed to download the audio file.")
        return

    # Loads
    audio = AudioSegment.from_file(io.BytesIO(audio_response.content))

    # Converts
    audio_data = np.array(audio.get_array_of_samples())

    # Normalize audio data to a range of -1 to 1
    audio_data = audio_data / np.max(np.abs(audio_data))

    # Prepare
    waveform_data = {
        "sample_rate": audio.frame_rate,
        "channels": audio.channels,
        "duration_seconds": len(audio_data) / audio.frame_rate,
        "data": audio_data.tolist(),
    }

    # Save waveform data
    with open(output_file, "w") as json_file:
        json.dump(waveform_data, json_file)

if __name__ == "__main__":
    audio_link = "https://example.com/audio.mp3"  #example link
    output_file = "waveform.json" 

    audio_to_waveform_json(audio_link, output_file)
