import rclpy
from rclpy.node import Node
from std_msgs.msg import String


#node created using template in Writing a simple publisher and subscriber (Python) at https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html
class directCommand(Node):
    def __init__(self):
        super().__init__("direct_command")
        self.publisher_ = self.create_publisher(String, 'direct_command', 10)
        time = 0.5
        self.timer = self.create_timer(time, self.timer_callback)
        self.msg = String()

    def timer_callback(self):
        self.msg.data = input("Enter command: ")
        self.publisher_.publish(self.msg)
        
    
    #def listener_callback(self, sample):
        #text = String()
        #text.data = self.asr.transcribe(sample.data)
        #with open("text.txt", "w") as file: #safe way to open file
         #   file.write(text.data)
        #self.publisher_.publish(text)
        #self.get_logger().info(text.data)



def main(args=None):
    rclpy.init(args=args)

    direct_command = directCommand()

    rclpy.spin(direct_command)

    direct_command.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()





