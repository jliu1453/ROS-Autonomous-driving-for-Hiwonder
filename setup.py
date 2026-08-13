from setuptools import find_packages, setup

package_name = 'ai_research'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools',
                      'transformers',
                        'torch',],
    zip_safe=True,
    maintainer='jiashuo liu',
    maintainer_email='jliu12@seattleu.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'video_Input = ai_research.videoInput:main',
        'command_Input = ai_research.command:main',
        'image_Processor = ai_research.imageProcessor:main',
        'audio_Input = ai_research.audio_input:main',
        'logic_Processor = ai_research.logicProcessor:main',
        'direct_Command = ai_research.directCommand:main',
        ],
    },
)
