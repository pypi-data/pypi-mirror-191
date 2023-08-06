import os

from setuptools import setup, find_packages

from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

long_description_md = """# datarobot-drfaster (Python)
## Usage
Optimizations to the predictions process and mainly used as a dependency for other Datarobot libraries such as [datarobot-mlops-stats-aggregator](https://pypi.org/project/datarobot-mlops-stats-aggregator/)
"""

os.environ['CC'] = 'gcc'
os.environ['CXX'] = 'g++'

lang = 'c++'
compile_args = ['-std=c++0x', '-O3', '-funroll-loops']
link_args = ['-std=c++0x', '-O3']

extensions = [
    Extension('drfaster.dateToInt.date_to_int_wrapper',
              ['drfaster/dateToInt/date_to_int_wrapper.pyx'],
              language=lang,
              extra_compile_args=compile_args,
              include_dirs=['drfaster/dateToInt'],
              extra_link_args=link_args),

    Extension('drfaster.intToTime.int2time_wrapper',
              ['drfaster/intToTime/int2time_wrapper.pyx'],
              language=lang,
              extra_compile_args=compile_args,
              extra_link_args=link_args),

    Extension('drfaster.centroid_histogram.histogram_wrapper',
              ['drfaster/centroid_histogram/histogram_wrapper.pyx'],
              language=lang,
              extra_compile_args=compile_args,
              extra_link_args=link_args),
]

setup(
    name='datarobot-drfaster',
    version='9.0.0',
    description='python library to make performance improvements to the DataRobot repo',
    long_description=long_description_md,
    long_description_content_type="text/markdown",
    author='DataRobot',
    author_email='info@datarobot.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(extensions),
)
