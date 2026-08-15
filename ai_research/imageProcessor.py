import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ai_research_interfaces.msg import CommandMsg
from cv_bridge import CvBridge 
from sensor_msgs.msg import Image
from ai_research.vlm.moonDream import Detector

#The ROS 2 publisher and subscriber node was adapted from the ROS 2 minimal publisher& subscriber tutorial (Open Robotics, n.d.).
class ImageProcessor(Node):
    def __init__(self):
        super().__init__("locate_object")
        self.publisher_ = self.create_publisher(String, 'text', 10) #publish coordinate to be recieved and used for driving
        self.logic_subscription = self.create_subscription( #subscribe to command that carry extracted object name
            String,
            'ai_command',
            self.command_callback,
            10)
        
        self.image_subscription = self.create_subscription( #found in https://wiki.hiwonder.com/projects/rosorin-pro/en/latest/docs/6_ROS%2BOpenCV_Course.html, hiwonder
            Image, 
            '/depth_cam/rgb0/image_raw',  #rgb img
            self.image_callback, 
            1
            )
        self.depth_subscription = self.create_subscription( #found in https://wiki.hiwonder.com/projects/rosorin-pro/en/latest/docs/6_ROS%2BOpenCV_Course.html, hiwonder
            Image,
            '/depth_cam/depth0/image_raw',  #depth img
            self.depth_callback,
            1
            )
            
        self.detector = Detector() #moonDream
        self.command = String()
        self.newImg = None
        self.DepthImg = None
        self.bridge = CvBridge() # #found in https://wiki.hiwonder.com/projects/rosorin-pro/en/latest/docs/6_ROS%2BOpenCV_Course.html, hiwonder
        self.i = 1
        self.pixelLength = 640 
        self.pixelHeight = 400 
    
    def command_callback(self, msg):
    #get coordinate of x and y using moondream, z using depth and combine into one
        self.command = msg
        self.get_logger().info("recieved command for object detection from ai...")
        coordinate = String()
        if self.newImg is None:
             self.get_logger().info("Waiting for image...")
             return
        coordinate.data = self.detector.detect(self.newImg, self.command.data)
        
        if coordinate.data != "":
            x, y = map(float, coordinate.data.split(","))
            x = x * self.pixelLength
            y = y * self.pixelHeight
            x = int(x)
            y = int(y)
            depth = self.depthImg[y, x]
            self.get_logger().info(str(depth))
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

