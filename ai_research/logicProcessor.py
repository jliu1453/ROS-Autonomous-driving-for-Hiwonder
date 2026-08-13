import rclpy
import json
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray
from ai_research.llm.logic import Processor


class LogicProcessor(Node):
    def __init__(self):
        super().__init__("logic_process")
        self.publisher_ = self.create_publisher(String, 'ai_command', 10)
        self.inputSubscription = self.create_subscription(
            String,
            'direct_command',
            self.input_callback,
            10)
        
        #self.vlmSubscription = self.create_subscription(
         #   Float32MultiArray,
          #  'coordinate',
           # self.vlm_callback,
            #10)
            
        self.processor = Processor()
        self.coordinate = Float32MultiArray
        self.i = 1 
        self.ai_response = String()
        self.objectName = String()
    
    def input_callback(self, direct_command):
        self.command = direct_command
        self.get_logger().info("recieved command...")
        if self.command is not None:
            self.get_logger().info("Sent to ai...")
            self.ai_response = self.processor.process(self.command.data)
            self.ai_response = self.ai_response.removeprefix("```json")
            self.ai_response = self.ai_response.removesuffix("```")
            self.ai_response = self.ai_response.strip()
            print(repr(self.ai_response))
            data = json.loads(self.ai_response)
            text = data["object"]
            self.objectName.data = str(text)
            self.publisher.publish(self.objectName)
            self.get_logger(self.objectName) #delete later
        else:
            print("command cannot be none")
        

        
        


def main(args=None):
    rclpy.init(args=args)

    logic_processor = LogicProcessor()

    rclpy.spin(logic_processor)

    logic_processor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

