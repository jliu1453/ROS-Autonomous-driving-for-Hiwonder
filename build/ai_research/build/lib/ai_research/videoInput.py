import rclpy
import queue
import cv2
import numpy
from rclpy.node import Node
from std_msgs.msg import String #ros way to wrapp msg in to data
from cv_bridge import CvBridge #last 2 referenced by hiwonder's code
from sensor_msgs.msg import Image


class VideoInput(Node):
     def __init__(self):
          super().__init__('input_camera')
          self.create_subscription(Image, '/depth_cam/rgb0/image_raw', self.image_callback, 1)
          self.publisher_ = self.create_publisher(Image, 'frame', 10)
          self.image_queue = queue.Queue(2)
          self.bridge = CvBridge()

     def image_callback(self, ros_image): #from hiwonder
         cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
         print("Received image:", cv_image.shape)
         if self.image_queue.full():
             old_image = self.image_queue.get()
             print("Queue full. Removed old image:", old_image.shape)
        
        
         self.image_queue.put(cv_image)
         print("Queue size:", self.image_queue.qsize())
         self.publisher_.publish(old_image)
    



def main(args=None):
    rclpy.init(args=args)

    video_Input = VideoInput()

    rclpy.spin(video_Input)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    video_Input.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

