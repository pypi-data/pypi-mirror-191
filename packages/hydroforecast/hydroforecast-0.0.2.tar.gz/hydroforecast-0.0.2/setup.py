from setuptools import setup, find_packages

setup(
    name='hydroforecast',
    version='0.0.2',
    description="hydrology forecast (Concept model, ML model)",
    long_description=open('README.md',encoding='gbk',errors='ignore').read(),
    include_package_data=True,
    author='jingx',
    author_email='jingxin0107@qq.com',
    maintainer='jingx',
    maintainer_email='jingxin0107@qq.com',
    license='MIT License',
    url='https://github.com/chooron',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.7',
    install_requires=[''],
    entry_points={
        'console_scripts': [''],
    },

)