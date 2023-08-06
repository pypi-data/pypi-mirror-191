from setuptools import setup, find_packages

setup(
    name='Flet_StoryBoard',
    version='0.2.3',
    description='A UI-Tools to build a powerful flet front-end without coding it.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SKbarbon/Flet_StoryBoard',
    author='SKBarbon',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        'flet',
    ],
    include_package_data=True,
    python_requires=">=3.8"
)