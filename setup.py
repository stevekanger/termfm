from setuptools import setup, find_packages

setup(
    name="termfm",                # Name of your package
    version="0.0.1",              # Version of your package
    packages=find_packages(),     # Automatically finds the packages in your directory
    install_requires=[],          # Dependencies
    entry_points={                # Optional: If you want to create CLI commands
        'console_scripts': [
            'termfm = termfm.__main__:main',  # Entry point for CLI tool
        ],
    },
    classifiers=[                 # Optional: Classifiers for your project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
)
