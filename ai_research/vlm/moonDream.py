from transformers import AutoModelForCausalLM
from PIL import Image
import torch

#copied from moonDream.ai at https://moondream.ai/skills/point
class Detector:
    def __init__(self):
    # Load the model
        self.model = AutoModelForCausalLM.from_pretrained(
        "vikhyatk/moondream2",
        revision="2025-06-21",
        trust_remote_code=True,
        device_map={"": "cuda"}  # ...or 'mps', on Apple Silicon
        )

    def detect(self, frame,objectName):
        # Load your image
        image = Image.fromarray(frame)

        # Optional sampling settings
        settings = {
            "max_objects": 50,
            "variant": None
        }

        # Run Moondream 
        object_name = objectName
        print(object_name)
        answer = self.model.query(image, f"do you see {object_name} in the image? Answer only use yes and no")
        print(answer)
        if answer["answer"].lower() == "no":
            return ""        
        result = self.model.point(image, objectName, settings=settings)
        #print(result)
        point = result["points"][0]
        return f"{point['x']}, {point['y']}"
    

#copied from moondream.ai
