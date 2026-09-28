import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class MoverTortuga(Node):

    def __init__(self):
        super().__init__('mover_tortuga')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.timer = self.create_timer(0.1, self.mover)

    def mover(self):
        mensaje = Twist()

        mensaje.linear.x = 1.0
        mensaje.angular.z = 0.5

        self.publisher.publish(mensaje)


def main(args=None):
    rclpy.init(args=args)

    nodo = MoverTortuga()

    rclpy.spin(nodo)

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
