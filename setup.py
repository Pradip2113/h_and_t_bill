from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in h_and_t_bill/__init__.py
from h_and_t_bill import __version__ as version

setup(
	name="h_and_t_bill",
	version=version,
	description="This is H and T Billing App",
	author="Abhishek",
	author_email="abhishekshinde9503@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
