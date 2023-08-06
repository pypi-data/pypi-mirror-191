from setuptools import setup, find_namespace_packages

__version__ = "0.0.5"

requirements = [
    "odd-models>=2.0.12",
]

setup(
    name="odd-airflow-2",
    version=__version__,
    description="ODD integration with Airflow",
    long_description_content_type="text/markdown",
    author="Open Data Discovery <pypi@opendatadiscovery.org>",
    include_package_data=True,
    packages=find_namespace_packages(include=['odd_airflow_integration.*', 'odd_airflow_integration']),
    install_requires=requirements,
    python_requires=">=3.9",
    zip_safe=False,
    keywords="opendatadiscovery",
    entry_points={
        "airflow.plugins": ["OddPlugin = odd_airflow_integration.plugin:OddPlugin"]
    }
)
