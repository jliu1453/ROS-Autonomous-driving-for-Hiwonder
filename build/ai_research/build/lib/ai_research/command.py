import rclpy
from rclpy.node import Node
from ai_research_interfaces.msg import CommandMsg



class enterCommand(Node):
    def __init__(self):
        super().__init__("command")
        self.publisher_ = self.create_publisher(CommandMsg, 'command', 10)
        time = 0.5
        self.timer = self.create_timer(time, self.timer_callback)
        self.msg = CommandMsg()

    def timer_callback(self):
        self.msg.command = input("Enter command(start or stop, case sensitive): ")
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

    enter_command = enterCommand()

    rclpy.spin(enter_command)

    enter_command.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()





