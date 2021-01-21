from setuptools import setup, find_packages

setup(
    name='pairless',  # 包名
    version='0.0.7',  # 版本号
    description=
    ('use >> replace pair ,such as `group_by_slice(lst,2)  lst>>group_by_slice(2)`'
     ),  # 简介
    long_description='My Custom Pipe Tool ',
    author='hexmagic',  # 作者名
    author_email='191440042@qq.com',  # 作者邮箱
    maintainer='hexmagic',  # 维护者名    
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    include_package_data=True,
    url='https://github.com/Hexmagic/pairless.git',  # 包主页显示的链接
    classifiers=[
        'Development Status :: 4 - Beta', 'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]),