# File: MJPEGstreamer_node.py

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from mjpeg_streamer import MjpegServer, Stream

class ImageStreamer(Node):
    def __init__(self):
        super().__init__('image_streamer')  # Initialize the ROS 2 node with the name 'image_streamer'
        self.bridge = CvBridge()  # Bridge to convert between ROS Image messages and OpenCV images

        topic = '/tita3233224/perception/camera/image/right'  # ROS topic to subscribe to (right stereo camera)

        # Set up subscription to the image topic using a sensor data QoS profile
        self.subscription = self.create_subscription(Image, topic, self.image_callback, qos_profile_sensor_data)

        # Initialize MJPEG stream with stream name, quality, and frame rate
        self.stream = Stream("my_camera", quality=50, fps=30)

        # Set the IP address to bind the MJPEG server
        self.server_ip = "192.168.101.135"  # Could also be 0.0.0.0 to bind to all interfaces

        # Create the MJPEG server on port 8080 and attach the stream
        self.server = MjpegServer(self.server_ip, 8080)
        self.server.add_stream(self.stream)
        self.server.start()

        # Log the URL where the MJPEG stream is accessible
        self.get_logger().info(f"MJPEG streaming at: http://{self.server_ip}:8080/my_camera")

    def image_callback(self, msg):
        """
        Callback function that is triggered every time an Image message is received.
        Converts the image to OpenCV format and feeds it to the MJPEG stream.
        """
        # self.get_logger().info(f"Got image: {msg.width}x{msg.height}, encoding={msg.encoding}") ## Uncomment to debug, this is to view if succesful communicate is made
        try:
            # Convert ROS Image message to OpenCV image (BGR format)
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Uncomment these lines to debug with a live OpenCV window (only works if a display is available)
            # cv2.imshow("Debug Image", cv_image)
            # cv2.waitKey(1)

            if cv_image is None:
                self.get_logger().warn("cv_image is None!")
                return

            # Optional: Calculate and log mean pixel value for debugging
            # mean_value = cv_image.mean()
            # self.get_logger().info(f"Mean pixel value: {mean_value}") ## Uncomment to debug, this is to view Image style

            # Set the current OpenCV frame for MJPEG streaming
            self.stream.set_frame(cv_image)

        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ImageStreamer()
    try:
        rclpy.spin(node)  # Keep the node running to process callbacks
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the MJPEG server and clean up the node
        node.server.stop()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
