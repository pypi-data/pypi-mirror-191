import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="FastAAI",
	version="0.1.20",
	author="Kenji Gerhardt",
	author_email="kenji.gerhardt@gmail.com",
	description="A rapid estimator for amino acid identity between genomes.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	#py_modules=["fastaai"],
	include_package_data=True,
	python_requires='>=3',
	install_requires=[
		'numpy',
		'pyrodigal==1.0.2',
		'pyhmmer',
	],
	entry_points={
		"console_scripts": [
			"fastaai=fastaai.fastaai:main",
		]
	}
)

