
from setuptools import find_packages
from setuptools import setup
import akiwi.version as version

package_data = []

setup(
    name="akiwi",
    version=version.version,
    author="djw.hope",
    author_email="djw.hope@gmail.com",
    url="https://github.com/shouxieai/tensorRT_Pro",
    description="Automatic code download tool.",
    python_requires=">=3.6",
    install_requires=["requests", "tqdm", "urllib3"],
    packages=find_packages(),
    package_data={
        "": package_data
    },
    zip_safe=False,
    platforms="linux",
    entry_points ={
        'console_scripts': [
              'kiwi = akiwi.__main__:main'
        ]
    }
)
