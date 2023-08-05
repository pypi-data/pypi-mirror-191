from distutils.core import setup

setup(
    name='cygnusdatautils',
    version='0.2',
    license='MIT',
    author="Mustafa Qazi",
    author_email='mus.qazi999@gmail.com',
    packages=['cygnusdatautils'],
    description='Data utils for cygnus',
    url='https://github.com/CygnusAIInternal/cygnusdatautils',
    download_url='https://github.com/CygnusAIInternal/cygnusdatautils/archive/refs/tags/v_02.tar.gz',
    keywords='cygnus data utils',
    install_requires=[
            'pandas',
            'numpy',
            'psycopg2-binary'
      ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
)