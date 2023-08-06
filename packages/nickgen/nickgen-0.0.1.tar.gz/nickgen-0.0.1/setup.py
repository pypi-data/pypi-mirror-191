from setuptools import setup, find_packages
setup(
    name='nickgen',
    version='0.0.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # package_data={"nickgen.data": ["*.json"]}
    include_package_data=True
)
