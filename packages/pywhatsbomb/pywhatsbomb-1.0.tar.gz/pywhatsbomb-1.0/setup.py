from setuptools import setup, find_packages


def readme() -> str:
    with open(r"README.md") as f:
        README = f.read()
    return README


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pywhatsbomb',
    version='1.0',
    description='A powerful tool for WhatsApp prank',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/Raguggg/pywhatsbomb',
    author='Ragu G',
    author_email='ragu19062002@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='whatsapp, prank, bot, automation, spamming, mass messaging, flooding, joke',
    packages=find_packages(),
    install_requires=['PyAutoGUI']
)
