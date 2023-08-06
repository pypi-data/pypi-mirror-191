from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='speechinput',
    version='0.0.1',
    description='Speech input provides a simple function to get an input from speech. It works like the buildin input function.',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='https://github.com/VicoShortman/speech-input',
    author='Vico Shortman',
    author_email='vico.shortman@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='speechrecognition speech input',
    packages=find_packages(),
    install_requires=['speechrecognition', 'pyaudio']
)
