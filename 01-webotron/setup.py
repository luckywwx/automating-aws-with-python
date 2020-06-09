from setuptools import setup

setup(
    name='webotron-90',
    version='0.1',
    author='Shawn Wong',
    author_email='luckywwx@gmail.com',
    description='Webotron 90 is a tool to deploy static websites to AWS.',
    license='GPLv3+',
    packages=['webotron'],
    url='https://github.com/luckywwx/automating-aws-with-python/tree/master/01-webotron/webotron',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''
)
