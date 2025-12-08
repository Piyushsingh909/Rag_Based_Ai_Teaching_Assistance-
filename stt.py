import whisper
import json
# Load a model that fits in 4GB VRAM
model = whisper.load_model("large-v2")   # large-v2 is too big for 4GB

audio_path = r"D:\Rag_Based_Ai\mp3_audio\sample.mp3"

result = model.transcribe(
    audio_path,
    language="en",
    task="translate",
    word_timestamps=False
)


chunks = []
for segment in result["segments"]:
    chunks.append({
        "start": segment["start"],
        "end": segment["end"],
        "text": segment["text"].strip()
    })

print(chunks)

with open("output.json", "w") as f:
    json.dump(chunks,f)