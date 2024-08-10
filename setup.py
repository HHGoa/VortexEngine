from setuptools import setup, find_packages

setup(
    name="vortex-engine",
    version="0.1.0",
    author="Manikandan05",
    author_email="manicdon7@gmail.com",
    description="Vortex Engine is a game engine built with Ursina for creating on-chain 2D and 3D games. It integrates with the Aptos blockchain, with plans to support Polygon, offering seamless blockchain features like transaction history within the game.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/HHGoa/VortexEngine.git",
    packages=find_packages(),
    install_requires=[
        'ursina',
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
