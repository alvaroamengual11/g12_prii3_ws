# PRII3 - Sprint 1 - Grupo 12

Proyecto del Sprint 1 de la asignatura PRII3 - Robots Inteligentes.

El objetivo es controlar el simulador `turtlesim` mediante ROS 2 Humble para dibujar de forma autónoma el número 12.

El proyecto incluye también servicios ROS para detener, reanudar y reiniciar el dibujo, y un fichero `launch` que permite iniciar todo el sistema mediante un único comando.

---

## Requisitos

El proyecto ha sido desarrollado y probado con:

- Ubuntu 22.04
- ROS 2 Humble
- Python 3.10
- colcon
- rosdep
- Git

ROS 2 Humble debe estar instalado previamente en el sistema.

---

## Clonar el repositorio

Clonar el proyecto desde GitHub:

```bash
git clone git@github.com:alvaroamengual11/g12_prii3_ws.git
```

Entrar en la carpeta:

```bash
cd g12_prii3_ws
```

---

## Preparar ROS 2

Cargar ROS 2 Humble:

```bash
source /opt/ros/humble/setup.bash
```

### Inicializar rosdep

Este paso solo es necesario la primera vez que se utiliza `rosdep` en un ordenador:

```bash
sudo rosdep init
rosdep update
```

Si `rosdep` ya había sido inicializado anteriormente, no es necesario repetir `sudo rosdep init`.

---

## Instalar dependencias

Desde la carpeta raíz del repositorio:

```bash
rosdep install --from-paths src --ignore-src --rosdistro humble -r -y
```

---

## Compilar el proyecto

Desde la carpeta raíz:

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

Si la compilación es correcta aparecerá un resultado similar a:

```text
Starting >>> g12_prii3_turtlesim
Finished <<< g12_prii3_turtlesim

Summary: 1 package finished
```

Después de compilar, cargar el workspace:

```bash
source install/setup.bash
```

---

## Ejecutar el proyecto

Para iniciar simultáneamente `turtlesim` y el nodo que dibuja el número 12:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch g12_prii3_turtlesim dibujo.launch.py
```

Con este único comando se inicia:

- el simulador `turtlesim`
- el nodo `g12_dibujante`
- el dibujo automático del número 12

La tortuga comienza automáticamente el recorrido programado.

---

## Servicios de control

El nodo dispone de tres servicios ROS.

### Detener el dibujo

En otra terminal:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Ejecutar:

```bash
ros2 service call /g12/detener std_srvs/srv/Trigger "{}"
```

La tortuga se detiene y conserva lo que ya ha dibujado.

---

### Reanudar el dibujo

```bash
ros2 service call /g12/reanudar std_srvs/srv/Trigger "{}"
```

La tortuga continúa desde el punto en el que se había detenido.

---

### Reiniciar el dibujo

```bash
ros2 service call /g12/reiniciar std_srvs/srv/Trigger "{}"
```

El lienzo se limpia y el número 12 comienza a dibujarse de nuevo desde el principio.

---

## Estado del dibujo

El nodo publica su estado mediante el topic:

```text
/g12/estado
```

Puede visualizarse con:

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

---

## Comprobar los nodos

Con el proyecto en ejecución:

```bash
ros2 node list
```

Deben aparecer:

```text
/g12_dibujante
/turtlesim
```

---

## Comprobar los servicios

```bash
ros2 service list | grep g12
```

Deben aparecer:

```text
/g12/detener
/g12/reanudar
/g12/reiniciar
```

---

## Comprobar los topics

```bash
ros2 topic list | grep g12
```

Debe aparecer:

```text
/g12/estado
```

También se utilizan los topics propios de `turtlesim`:

```text
/turtle1/cmd_vel
/turtle1/pose
```

---

## Funcionamiento del nodo

`turtlesim` publica continuamente la posición de la tortuga mediante:

```text
/turtle1/pose
```

El nodo `g12_dibujante` recibe esa posición y la compara con el siguiente punto de la trayectoria programada.

Las órdenes de movimiento se envían mediante mensajes `Twist` al topic:

```text
/turtle1/cmd_vel
```

El controlador calcula:

- la distancia hasta el siguiente objetivo
- el ángulo hacia el objetivo
- el error de orientación

Si la tortuga no está correctamente orientada, primero gira.

Cuando está orientada hacia el punto objetivo, comienza a avanzar.

El proceso se repite continuamente hasta completar los puntos que forman el número 12.

---

## Movimiento y dibujo

La trayectoria está formada por una serie de puntos predefinidos.

Para desplazarse entre zonas que no deben quedar unidas, el nodo levanta el lápiz de `turtlesim`.

Cuando debe comenzar un nuevo trazo, vuelve a bajar el lápiz.

De esta forma se pueden dibujar por separado las diferentes partes del número 12.

---

## Fichero launch

El fichero:

```text
launch/dibujo.launch.py
```

inicia automáticamente:

```text
turtlesim_node
dibujar_12
```

Por tanto, no es necesario arrancar manualmente `turtlesim` antes de ejecutar el controlador.

Todo el sistema puede iniciarse mediante:

```bash
ros2 launch g12_prii3_turtlesim dibujo.launch.py
```

---

## Estructura principal

```text
g12_prii3_ws
├── README.md
├── src
│   └── g12_prii3_turtlesim
│       ├── g12_prii3_turtlesim
│       │   ├── __init__.py
│       │   ├── dibujar_12.py
│       │   └── mover_tortuga.py
│       ├── launch
│       │   └── dibujo.launch.py
│       ├── resource
│       ├── test
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
└── .gitignore
```

Las carpetas:

```text
build/
install/
log/
```

se generan al compilar y no se almacenan en GitHub.

---

## Archivos principales

### dibujar_12.py

Nodo principal del Sprint.

Se encarga de:

- leer la posición de la tortuga
- calcular el movimiento
- publicar velocidades
- dibujar el número 12
- detener el dibujo
- reanudarlo
- reiniciarlo
- publicar el estado del sistema

### mover_tortuga.py

Nodo utilizado inicialmente para comprobar el funcionamiento de la publicación de mensajes `Twist`.

### dibujo.launch.py

Fichero utilizado para iniciar conjuntamente `turtlesim` y el nodo `g12_dibujante`.

### package.xml

Contiene las dependencias ROS utilizadas por el paquete.

### setup.py

Configura el paquete Python, los ejecutables ROS y la instalación del fichero `launch`.

---

## Prueba desde una clonación limpia

El repositorio ha sido probado clonándolo en una carpeta independiente.

Procedimiento:

```bash
source /opt/ros/humble/setup.bash

git clone git@github.com:alvaroamengual11/g12_prii3_ws.git

cd g12_prii3_ws

rosdep install --from-paths src --ignore-src --rosdistro humble -r -y

colcon build --symlink-install

source install/setup.bash

ros2 launch g12_prii3_turtlesim dibujo.launch.py
```

La prueba permite comprobar que el proyecto puede descargarse, compilarse y ejecutarse sin utilizar los archivos `build`, `install` o `log` del ordenador original.

---

## Detener el programa

Para cerrar el `launch` y todos los nodos iniciados por él:

```text
Ctrl + C
```

---

## Repositorio

Repositorio GitHub:

```text
alvaroamengual11/g12_prii3_ws
```

Rama principal:

```text
main
```

El usuario `pamuobe` ha sido invitado como colaborador del repositorio.

---

## Grupo

Grupo 12

Asignatura: PRII3 - Robots Inteligentes

Sprint 1
