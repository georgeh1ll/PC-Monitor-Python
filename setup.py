from setuptools import setup, find_packages

setup(
    name="system_monitor",
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
    description="A GUI Windows system monitor application using Python.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="George Hill",
    author_email="your.email@example.com",
    url="https://github.com/georgeh1ll/PC-Monitor-Python",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    python_requires='>=3.6',
)
