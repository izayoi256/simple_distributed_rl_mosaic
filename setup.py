import os

from setuptools import find_packages, setup

package_name = "srl"

# read version
version_path = os.path.join(os.path.dirname(__file__), package_name, "version.py")
exec(open(version_path).read())


setup(
    name=package_name,
    packages=[package for package in find_packages() if package.startswith(package_name)],
    version=VERSION,  # noqa F821
    license="MIT",
    author="poco",
    author_email="pocopococpp198@gmail.com",
    url="https://github.com/pocokhc/simple_rl",
    description="simple reinforcement learning framework",
    long_description="simple reinforcement learning framework",
    install_requires=[
        "numpy",
        "gym",
        "pygame",  # gym
        "tensorflow",
        "tensorflow-addons",
    ],
    extras_require={
        "image": ["matplotlib", "opencv-python", "pillow"],
        "notebook": ["matplotlib", "opencv-python", "pillow", "ipython"],
        "kaggle": ["kaggle_environments"],
        "spec": [
            "psutil",  # CPU info
            "pynvml",  # GPU info
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
