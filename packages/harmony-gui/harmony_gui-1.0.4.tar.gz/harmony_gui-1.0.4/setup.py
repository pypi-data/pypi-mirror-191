import sys
import setuptools

PACKAGE_NAME = 'harmony_gui'
PROJECT_DIR_NAME = 'harmony_gui'
PACKAGE_VERSION = '1.0.4'

python_version = sys.version_info[:2]
if python_version < (3, 7):
    print("{} requires Python version 3.7 or later".format(PACKAGE_NAME))
    print("(Version {}.{} detected)".format(*python_version))
    sys.exit(1)
elif python_version >= (3, 10):
    print("{} is not compatible with Python 3.10 or above".format(PACKAGE_NAME))
    print("(Version {}.{} detected)".format(*python_version))
    sys.exit(1)

setuptools.setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author="Renyu (Robin) Li",
    author_email="rl626@cornell.edu",
    description="Harmony Programming Language GUI",
    packages=setuptools.find_packages(),
    install_requires=[
        'Pillow',
        'PyQt5',
        'numpy',
        'harmony'
    ],
    license="BSD",
    url="https://harmonylang.dev",
    include_package_data=True,
    package_data={
        PACKAGE_NAME: [
            "gui_import/*.json",
        ]
    },
    entry_points={
        'console_scripts': [
            'harmony-gui=harmony_gui.gui:main',
        ]
    },
    python_requires=">=3.7, <3.10",
)
