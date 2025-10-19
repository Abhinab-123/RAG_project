import whisper
import json
import os

model = whisper.load_model("large-v2")
result=model.transcribe(audio="audios/simple_trimmed.mp3",
                        language="hi",
                        task="translate",
                        word_timestamps=False)

chunk=[]
for segment in result["segments"]:
    chunk.append({"start":segment["start"],"end":segment["end"],"text":segment["text"]})
print(chunk)
with open("output.json","w") as f:
    json.dump(chunk,f)

