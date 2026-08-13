from huggingface_hub import InferenceClient

#edited from the sample
#prompt edited from hiwonder, orginal code see:...(add later)
class Processor:
    def __init__(self):
        self.client = InferenceClient("http://192.168.12.122:8000")
       
        self.initialPrompt =  '''
**Role
Your task is to analyze command sent by the user, who will give you sentences where contain a object they want to track,you task is to analyze the sentences, indentify what they want to track,  and return the result strictly following the specified output format.

Step 1: Understand User Instructions
You will receive a sentence. From this sentence, extract the object name to be detected.
Note: Use English for the object value, do not include any objects not explicitly mentioned in the instruction.



step3: After extract the object name, give the object name strictly following the output format below, do not response in any other format

**Output Format (
{
    "object": "name", 
    "response": "reflect the user's instruction (5-30 characters)"
}

**Example
Input: track the person
Output:
{
    "object": "person",
    "response": "I will now track the person you mentioned."
}

Sentence: 
    '''
        

    def process(self,command):
        self.command = self.initialPrompt + command
        self.messages = [{"role": "user", "content": self.command}]
        result = self.client.chat_completion(self.messages, model="Qwen/Qwen2.5-0.5B-Instruct", max_tokens=256)
        return result.choices[0].message.content
