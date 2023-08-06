import setuptools
with open(r'C:\Users\ruden\Desktop\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='Lossesofrussia',
	version='1.0',
	author='nazar.rudenok',
	author_email='nazarrudenok1@gmail.com',
	description='The lossesofrussia library returns information about russia losses in the war with Ukraine',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['lossesofrussia'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)