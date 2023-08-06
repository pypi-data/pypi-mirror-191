from distutils.core import setup

__version__ = '0.2.1'

reqstring = '''
joblib==1.2.0
numpy==1.24.2
pandas==1.5.3
python-dateutil==2.8.2
pytz==2022.7.1
scikit-learn==1.2.1
scipy==1.10.0
six==1.16.0
threadpoolctl==3.1.0
'''

if __name__ == '__main__':
    setup(
        name='pec',
        version=__version__,
        description='Progressive Ensemble Clustering',
        url='https://aware-diag-sapienza.github.io/pec',
        author='AWARE Research Group - Sapienza Università di Roma',
        author_email='blasilli@diag.uniroma1.it',
        license='GNU General Public License v3.0',
        platforms=['Linux', 'Mac OS-X', 'Solaris', 'Unix', 'Windows'],
        #install_requires=open('requirements.txt').read().strip().split('\n'),
        install_requires=reqstring.strip().split('\n'),
        include_package_data=True,
        zip_safe=True,
        download_url=f'https://github.com/aware-diag-sapienza/pec/archive/refs/tags/v{__version__}.tar.gz',
        classifiers=[
            'Development Status :: 3 - Alpha',
            # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',  # Define that your audience are developers
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',  # Again, pick a license
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],
    )
