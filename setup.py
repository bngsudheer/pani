from setuptools import setup, find_packages

setup(
    name='Pani',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'SQLAlchemy',
        'wtforms-recaptcha',
        'Flask',
        'Flask-Login',
        'Flask-Mail',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-Principal',
        'flask-paginate',
    ]
)
