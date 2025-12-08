import whisper
import json
import os
model = whisper.load_model("large-v2") 
# Load a model that fits in 4GB VRAM

audios = os.listdir("mp3_audio")

for audio in audios:
    if ("_" in audio):
        number = audio.split("_")[0]
        title = audio.split("_")[1][:-4]
        print(number, title)

        result = model.transcribe(audio=f"mp3_audio/{audio}",
                                language="en",
                                task="translate",
                                word_timestamps=False)
        
        chunks = []
        for segment in result["segments"]:
            chunks.append({
                "number": number,
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            })
            chunks_with_metadata = {"chunks": chunks, "text": result["text"]}

        with open(f"jsons/{audio}.json", "w") as f:
            json.dump(chunks_with_metadata,f)
