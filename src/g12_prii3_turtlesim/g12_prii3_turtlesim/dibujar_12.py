import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_srvs.srv import Trigger, Empty
from turtlesim.msg import Pose
from turtlesim.srv import SetPen


class Dibujar12(Node):

    def __init__(self):
        super().__init__('g12_dibujante')

        # Publicamos órdenes de movimiento
        self.publisher_vel = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Publicamos el estado del dibujo
        self.publisher_estado = self.create_publisher(
            String,
            '/g12/estado',
            10
        )

        # Leemos la posición real de la tortuga
        self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Servicios propios del grupo
        self.create_service(
            Trigger,
            '/g12/detener',
            self.detener_callback
        )

        self.create_service(
            Trigger,
            '/g12/reanudar',
            self.reanudar_callback
        )

        self.create_service(
            Trigger,
            '/g12/reiniciar',
            self.reiniciar_callback
        )

        # Servicios internos de turtlesim
        self.cliente_lapiz = self.create_client(
            SetPen,
            '/turtle1/set_pen'
        )

        self.cliente_reset = self.create_client(
            Empty,
            '/reset'
        )

        self.pose = None
        self.pausado = False
        self.finalizado = False

        self.indice = 0
        self.lapiz_actual = None
        self.futuro_lapiz = None
        self.futuro_reset = None

        # Cada elemento es:
        # (x, y, dibujar)
        #
        # False = mover con el lápiz levantado
        # True  = mover dibujando

        self.recorrido = [
            # Ir al comienzo del 1
            (2.5, 8.5, False),

            # Dibujar el 1
            (3.3, 9.2, True),
            (3.3, 3.0, True),
            (4.2, 3.0, True),

            # Ir al comienzo del 2
            (5.2, 8.4, False),

            # Dibujar el 2
            (5.8, 9.2, True),
            (7.2, 9.2, True),
            (8.0, 8.5, True),
            (8.0, 7.5, True),
            (5.2, 3.0, True),
            (8.1, 3.0, True),
        ]

        self.timer = self.create_timer(
            0.05,
            self.control
        )

        self.publicar_estado('PREPARANDO')

    def pose_callback(self, msg):
        self.pose = msg

    def publicar_estado(self, texto):
        msg = String()
        msg.data = texto
        self.publisher_estado.publish(msg)

    def parar(self):
        msg = Twist()
        self.publisher_vel.publish(msg)

    def normalizar_angulo(self, angulo):
        while angulo > math.pi:
            angulo -= 2.0 * math.pi

        while angulo < -math.pi:
            angulo += 2.0 * math.pi

        return angulo

    def cambiar_lapiz(self, dibujar):
        if not self.cliente_lapiz.service_is_ready():
            return

        peticion = SetPen.Request()

        if dibujar:
            peticion.r = 255
            peticion.g = 255
            peticion.b = 255
            peticion.width = 3
            peticion.off = 0
        else:
            peticion.r = 255
            peticion.g = 255
            peticion.b = 255
            peticion.width = 3
            peticion.off = 1

        self.futuro_lapiz = self.cliente_lapiz.call_async(
            peticion
        )

        self.lapiz_actual = dibujar

    def control(self):

        # Esperar a tener posición
        if self.pose is None:
            return

        # Esperar a que termine un cambio de lápiz
        if self.futuro_lapiz is not None:
            if not self.futuro_lapiz.done():
                self.parar()
                return

            self.futuro_lapiz = None

        # Esperar a que termine un reset
        if self.futuro_reset is not None:
            if not self.futuro_reset.done():
                self.parar()
                return

            self.futuro_reset = None
            self.pose = None
            self.lapiz_actual = None
            return

        if self.pausado:
            self.parar()
            return

        if self.finalizado:
            self.parar()
            return

        if self.indice >= len(self.recorrido):
            self.finalizado = True
            self.parar()
            self.publicar_estado('FINALIZADO')
            return

        objetivo_x, objetivo_y, dibujar = self.recorrido[
            self.indice
        ]

        # Antes de moverse, comprobar el estado del lápiz
        if self.lapiz_actual != dibujar:
            self.cambiar_lapiz(dibujar)
            self.parar()
            return

        dx = objetivo_x - self.pose.x
        dy = objetivo_y - self.pose.y

        distancia = math.sqrt(dx * dx + dy * dy)

        # Hemos llegado al punto
        if distancia < 0.08:
            self.parar()
            self.indice += 1
            return

        angulo_objetivo = math.atan2(dy, dx)

        error_angulo = self.normalizar_angulo(
            angulo_objetivo - self.pose.theta
        )

        mensaje = Twist()

        # Si no mira hacia el objetivo, primero gira
        if abs(error_angulo) > 0.15:
            mensaje.linear.x = 0.0
            mensaje.angular.z = max(
                -2.5,
                min(2.5, 2.0 * error_angulo)
            )

        # Cuando está orientada, avanza
        else:
            mensaje.linear.x = min(
                1.4,
                1.5 * distancia
            )

            mensaje.angular.z = max(
                -1.5,
                min(1.5, 2.0 * error_angulo)
            )

        self.publisher_vel.publish(mensaje)
        self.publicar_estado('DIBUJANDO')

    def detener_callback(self, request, response):
        self.pausado = True
        self.parar()
        self.publicar_estado('PAUSADO')

        response.success = True
        response.message = 'Dibujo detenido'

        return response

    def reanudar_callback(self, request, response):

        if self.finalizado:
            response.success = False
            response.message = (
                'El dibujo ya ha terminado. Usa reiniciar.'
            )
            return response

        self.pausado = False
        self.publicar_estado('DIBUJANDO')

        response.success = True
        response.message = 'Dibujo reanudado'

        return response

    def reiniciar_callback(self, request, response):

        if not self.cliente_reset.service_is_ready():
            response.success = False
            response.message = 'Servicio reset no disponible'
            return response

        self.parar()

        self.indice = 0
        self.pausado = False
        self.finalizado = False
        self.lapiz_actual = None

        peticion = Empty.Request()

        self.futuro_reset = self.cliente_reset.call_async(
            peticion
        )

        self.publicar_estado('PREPARANDO')

        response.success = True
        response.message = 'Reinicio solicitado'

        return response


def main(args=None):

    rclpy.init(args=args)

    nodo = Dibujar12()

    rclpy.spin(nodo)

    nodo.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
