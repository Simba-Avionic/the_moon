from setuptools import find_packages, setup

package_name = 'the_moon'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='patrickthemoon',
    maintainer_email='patrickthemoon@gmail.com',
    description='nowy node ROS2 do obsługi radia 433 MHz z protokołem mavlink - by patrickthemoon',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'radio433_node = the_moon.radio433_node:main'
        ],
    },
)
