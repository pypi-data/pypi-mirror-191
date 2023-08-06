from setuptools import setup, find_packages

setup(
    name='google_drive_oauth',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'google-auth',
        'google-api-python-client',
        'google-auth-oauthlib'
    ],
    entry_points={
        'console_scripts': [
            'drive_reader = google_drive_oauth.drive_reader:main'
            'drive_writer = google_drive_oauth.drive_writer:main'
        ]
    }
)
