import numpy as np
import torch
from threading import Thread

from transformers import (
    AutoModelForRNNT,
    AutoProcessor,
    TextIteratorStreamer,
)

#original code from nvidia's sample code see https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b
#edited use chatgpt, prompt: edit the code provided so it take numpy array from mic as audio, send to nemotron and print
class ASR:
    def __init__(self):
        self.model_id = "nvidia/nemotron-3.5-asr-streaming-0.6b"

        self.processor = AutoProcessor.from_pretrained(self.model_id)

        self.model = AutoModelForRNNT.from_pretrained(
            self.model_id,
            device_map="auto",
        )

        self.processor.set_num_lookahead_tokens(6)

        print(
            f"Streaming latency: "
            f"{self.processor.streaming_latency_ms} ms"
        )

        self.language = "en-US"

        self.sampling_rate = (
            self.processor.feature_extractor.sampling_rate
        )

        print("Expected sample rate:", self.sampling_rate)

    def transcribe(self, audio: np.ndarray):

        # Make sure NumPy audio is float32
        audio = np.asarray(audio, dtype=np.float32)

        # First chunk
        first_chunk_inputs = self.processor(
            audio,
            sampling_rate=self.sampling_rate,
            is_streaming=True,
            is_first_audio_chunk=True,
            language=self.language,
            return_tensors="pt",
        )

        first_chunk_inputs = first_chunk_inputs.to(
            self.model.device,
            dtype=self.model.dtype,
        )

        streamer = TextIteratorStreamer(
            self.processor.tokenizer,
            skip_special_tokens=True,
        )

        generate_kwargs = {
            **first_chunk_inputs,
            "streamer": streamer,
        }

        thread = Thread(
            target=self.model.generate,
            kwargs=generate_kwargs,
        )

        thread.start()

        print("Model output: ", end="", flush=True)

        for text_chunk in streamer:
            print(text_chunk, end="", flush=True)

        print()

        thread.join()

