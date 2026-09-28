from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'g12_prii3_turtlesim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),   

    data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'),
        glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alvaro',
    maintainer_email='alvaro@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    

    entry_points={
    'console_scripts': [
        'mover_tortuga = g12_prii3_turtlesim.mover_tortuga:main',
        'dibujar_12 = g12_prii3_turtlesim.dibujar_12:main',
    ],
},
)
