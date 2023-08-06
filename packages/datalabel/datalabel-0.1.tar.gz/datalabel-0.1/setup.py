from setuptools import setup

setup(
    name='datalabel',
    version='0.1',
    packages=['labeler'],
    author='TitanLabs',
    author_email='product@titanlabs.co',
    description='quickly and effortlessly edit your dataframes without having to write any code. Its intuitive interface makes it ideal for both experienced data professionals and those new to data editing.',
    install_requires=['pandas', 'requests', 'fastapi', 'uvicorn'],
)
