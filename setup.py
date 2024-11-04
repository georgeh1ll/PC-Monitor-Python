from setuptools import setup, find_packages

setup(
    name="system_monitor_python_gui_windows",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "pycaw",
        "comtypes",
        "pythoncom",  # Make sure to include all required packages
    ],
    entry_points={
        'console_scripts': [
            'system_monitor=system_monitor.monitor:main',  # Entry point to your app
        ],
    },
    description="A simple system monitor application using Tkinter.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/system_monitor",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",  # Change this line
        "Natural Language :: English",  # You can add more if applicable
    ],
    python_requires='>=3.6',
)
