from huggingface_hub import InferenceClient

#edited from the sample

class Processor:
    def __init__(self):
        self.client = InferenceClient("http://192.168.12.122:8000")
       
        self.initialPrompt =  '''
rules: 
1.extract the objects the prompt want to ask about
2.using a single word if possible, and no longer than a short phrase
3.no extra letters, symbols, speical characters or spaces before or after the ouput

examples:
prompt: "where is my bag", output: bag
prompt: "find the animal that just ran into my room", output: animal
prompt: "can you check if the meat is cooked", output: cooked meat
    '''


    def process(self,command):
        self.command = self.initialPrompt + command
        self.messages = [{"role": "user", "content": self.command}]
        result = self.client.chat_completion(self.messages, model="Qwen/Qwen2.5-1.5B-Instruct", max_tokens=256)
        return result.choices[0].message.content
        
      
