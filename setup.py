from setuptools import setup, find_packages


setup(
    name="pubsub-split",
    version="1.0.0",
    description=(
        "split gcp pub/sub messages so that data can ingest happily into Bigquery "
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="pubsub-split",
    author="Kristen Carros",
    author_email="kvcarros0@gmail.com",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["google-cloud-pubsub", "python-dateutil"],
    test_suite="tests",
)
