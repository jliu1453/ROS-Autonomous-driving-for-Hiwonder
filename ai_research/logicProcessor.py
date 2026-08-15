import rclpy
from rclpy.node import Node
from std_msgs.msg import String #ros string
from ai_research.llm.logic import Processor #program that handles llm

#node created using template in Writing a simple publisher and subscriber (Python) at https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html

class LogicProcessor(Node):
#logic Processor: recieve natural language command, send command to be processed by qwen 1.5B llm, then send extracted object name to image Processor to get its coordinate
    def __init__(self):
        super().__init__("logic_process")
        self.publisher_ = self.create_publisher(String, 'ai_command', 10) #publish extracted oject name
        self.inputSubscription = self.create_subscription(
            String,
            'direct_command',
            self.input_callback,
            10)
        
        self.vlmSubscription = self.create_subscription( #listen to coordinate from moondream
            String,
            'coordinate',
            self.vlm_callback,
            10)
            
        #vars to hold values from subscriptions or func call backs
        self.processor = Processor() #llm
        self.coordinate = String()
        self.i = 1 
        self.ai_response = String()
        self.objectName = String()
    
    def input_callback(self, direct_command):
    #llm
        self.command = direct_command
        self.get_logger().info("recieved command...")
        if self.command is not None:
            self.get_logger().info("Sent to ai...")
            self.ai_response.data = self.processor.process(direct_command.data)
            self.publisher_.publish(self.ai_response)
            self.get_logger().info(self.ai_response.data) #delete later
        else:
            print("please enter a vaild, non empty command")
            
    def vlm_callback(self, coordinate):
    #moonDream
        if coordinate.data == None:
            self.get_logger().info("object not detected")
            return
        self.coordinate = coordinate
        self.get_logger().info("the "+ self.objectName.data + " is at " + self.coordinate.data)
           
        

        
        


def main(args=None):
    rclpy.init(args=args)

    logic_processor = LogicProcessor()

    rclpy.spin(logic_processor)

    logic_processor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

