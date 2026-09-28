# PRII3 - Sprint 1 - Grupo 12

Proyecto del Sprint 1 de la asignatura PRII3 - Robots Inteligentes.

El objetivo de este proyecto es controlar el simulador `turtlesim` mediante ROS 2 Humble para dibujar de forma autónoma el número 12.

## Requisitos

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- colcon

## Estructura del proyecto

El workspace contiene el paquete:

```text
g12_prii3_turtlesim
```

El nodo principal es:

```text
dibujar_12
```

El fichero launch es:

```text
dibujo.launch.py
```

## Compilar el proyecto

Desde la carpeta raíz del repositorio:

```bash
source /opt/ros/humble/setup.bash

rosdep install --from-paths src --ignore-src --rosdistro humble -r -y

colcon build --symlink-install

source install/setup.bash
```

## Ejecutar el proyecto

Para iniciar `turtlesim` y el nodo que dibuja automáticamente el número 12:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch g12_prii3_turtlesim dibujo.launch.py
```

Con este único comando se inicia:

- el simulador `turtlesim`
- el nodo `g12_dibujante`
- el dibujo automático del número 12

## Servicios

El nodo dispone de tres servicios para controlar el dibujo.

### Detener el dibujo

```bash
ros2 service call /g12/detener std_srvs/srv/Trigger "{}"
```

La tortuga se detiene y conserva el dibujo realizado hasta ese momento.

### Reanudar el dibujo

```bash
ros2 service call /g12/reanudar std_srvs/srv/Trigger "{}"
```

La tortuga continúa desde el punto donde se había detenido.

### Reiniciar el dibujo

```bash
ros2 service call /g12/reiniciar std_srvs/srv/Trigger "{}"
```

El lienzo se limpia y el número 12 comienza a dibujarse de nuevo desde el principio.

## Estado del dibujo

El estado del nodo se publica en el topic:

```text
/g12/estado
```

Puede consultarse mediante:

```bash
ros2 topic echo /g12/estado
```

Los estados principales son:

```text
PREPARANDO
DIBUJANDO
PAUSADO
FINALIZADO
```

## Comprobaciones

Para comprobar los nodos activos:

```bash
ros2 node list
```

Deben aparecer:

```text
/g12_dibujante
/turtlesim
```

Para comprobar los servicios del proyecto:

```bash
ros2 service list | grep g12
```

Deben aparecer:

```text
/g12/detener
/g12/reanudar
/g12/reiniciar
```

Para comprobar los topics del proyecto:

```bash
ros2 topic list | grep g12
```

Debe aparecer:

```text
/g12/estado
```

## Funcionamiento del nodo

`turtlesim` publica la posición de la tortuga mediante:

```text
/turtle1/pose
```

El nodo `g12_dibujante` utiliza esa posición para calcular hacia dónde debe desplazarse.

Las órdenes de movimiento se publican mediante mensajes `Twist` en:

```text
/turtle1/cmd_vel
```

El nodo calcula continuamente la distancia y el ángulo hasta el siguiente punto de la trayectoria.

Si la tortuga no está orientada correctamente, primero gira.

Cuando está orientada hacia el objetivo, avanza.

De esta manera se recorren automáticamente los puntos que forman el número 12.

## Archivos principales

```text
src/g12_prii3_turtlesim/
├── g12_prii3_turtlesim/
│   ├── __init__.py
│   ├── mover_tortuga.py
│   └── dibujar_12.py
├── launch/
│   └── dibujo.launch.py
├── package.xml
├── setup.cfg
└── setup.py
```

`mover_tortuga.py` se utilizó como primera prueba de publicación de velocidades.

`dibujar_12.py` contiene el nodo principal del Sprint.

`dibujo.launch.py` permite iniciar el simulador y el nodo mediante un único comando.

## Grupo

Grupo 12

Asignatura: PRII3 - Robots Inteligentes
