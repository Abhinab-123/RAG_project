import whisper
import json
import torch
import os
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
model=whisper.load_model("small",device=device)
audios=os.listdir("audios")

for audio in audios:
    if("_"in audio):
        number=audio.split("_")[0]
        title=audio.split("_")[1]
        print(number   ,   title)
        result=model.transcribe(audio=f"audios/{audio}",
                        language="hi",
                        task="translate",
                        word_timestamps=False)

        chunk=[]
        for segment in result["segments"]:
            chunk.append({"number":number,"title":title,"start":segment["start"],"end":segment["end"],"text":segment["text"]})
        chunks_with_metadata={"chunks":chunk,"text":result["text"]}
        with open(f"jsons/{audio}","w") as f:
            json.dump(chunks_with_metadata,f)
