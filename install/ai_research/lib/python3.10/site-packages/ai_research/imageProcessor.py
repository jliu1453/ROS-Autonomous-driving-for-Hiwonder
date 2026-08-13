import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ai_research_interfaces.msg import CommandMsg
from cv_bridge import CvBridge #last 2 referenced by hiwonder's code
from sensor_msgs.msg import Image
from ai_research.vlm.moonDream import Detector


class ImageProcessor(Node):
    def __init__(self):
        super().__init__("locate_object")
        self.publisher_ = self.create_publisher(String, 'text', 10)
        self.inputSubscription = self.create_subscription(
            CommandMsg,
            'command',
            self.input_callback,
            10)
        
        self.image_subscription = self.create_subscription(
            Image, 
            '/depth_cam/rgb0/image_raw', 
            self.image_callback, 
            1
            )
        self.depth_subscription = self.create_subscription(
            Image,
            '/depth_cam/depth0/image_raw', 
            self.depth_callback,
            1
            )
            
        self.detector = Detector()
        self.command = CommandMsg()
        self.newImg = None
        self.DepthImg = None
        self.bridge = CvBridge()
        self.i = 1
        self.pixelLength = 640
        self.pixelHeight = 400 
    
    def input_callback(self, msg):
        self.command = msg
        self.get_logger().info("recieved command...")
        coordinate = String()
        if self.newImg is None:
             self.get_logger().info("Waiting for image...")
             return
        coordinate.data = self.detector.detect(self.newImg, self.command.object)
        
        if coordinate.data != "":
            x, y = map(float, coordinate.data.split(","))
            x = x * self.pixelLength
            y = y * self.pixelHeight
            x = int(x)
            y = int(y)
            depth = self.depthImg[y, x]
            self.get_logger().info(str(depth))
            with open("coordinates.txt", "w") as file: #safe way to open file
                file.write(coordinate.data)
            self.publisher_.publish(coordinate)
            self.get_logger().info(coordinate.data)
        else:
            self.get_logger().info("not detected!")
        
        
        
    def image_callback(self, ros_image):
        if self.i < 2:
            print("img recieved!")
            self.i += 1
        self.newImg =self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        

        #self.get_logger().info(
        #f"Image received: {self.newImg.shape}"
    #)
    
    def depth_callback(self, ros_image):
        self.depthImg = self.bridge.imgmsg_to_cv2(ros_image, "passthrough")
        
        


def main(args=None):
    rclpy.init(args=args)

    image_processor = ImageProcessor()

    rclpy.spin(image_processor)

    image_processor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

