from setuptools import find_packages, setup

package_name = 'my_robot_sdk'

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
    maintainer='nman',
    maintainer_email='naman.agg.aps@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'test_move = my_robot_sdk.test_move:main',
            'test_moveit = my_robot_sdk.test_moveit:main',
            'task_demo = my_robot_sdk.task_demo:main',
        ],
    },
)
