from setuptools import setup

setup(
        name='openapi-trimmer',
        version='0.1.0',
        packages=['openapi_trimmer'],
        include_package_data=True,
        install_requires=[
            'setuptools',
            'pyyaml>=6'
        ],
        entry_points={
            'console_scripts': [
                'openapi-trimmer=openapi_trimmer.main:main',
            ],
        },
        author='Ivan Dachev',
        author_email='i_dachev@yahoo.co.uk',
        description='Tool to trim OpenAPI YAML file to '
                    'include only desired paths and components.',
        license='MIT',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        url='https://github.com/idachev/openapi-trimmer',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.10',
)
