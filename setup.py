from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='redshift_tool',
      version='0.3',
      description='Elegant data load from Pandas to Redshift',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.0',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='Pandas,DataFrame,S3,Redshift,Append,Copy,Upsert,Incremetal Load',        
      url='http://github.com/mkgiitr/redshift_tool',
      author='Manish Kumar',
      author_email='manish.kumar535@gmail.com',
      license='MIT',
      packages=['redshift_tool'],
      install_requires=[
          'psycopg2','pandas','numpy','boto3',
      ],
      include_package_data=True,        
      zip_safe=False)
