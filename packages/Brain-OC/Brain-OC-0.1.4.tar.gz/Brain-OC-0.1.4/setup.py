from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='Brain-OC',
	version='0.1.4',
	description='Brain contains a service to run users and permissions',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://ouroboroscoding.com/body/brain',
	project_urls={
		'Documentation': 'https://ouroboroscoding.com/body/brain',
		'Source': 'https://github.com/ouroboroscoding/brain',
		'Tracker': 'https://github.com/ouroboroscoding/brain/issues'
	},
	keywords=['rest','microservices'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='Custom',
	packages=['brain'],
	package_data={'brain': ['definitions/*.json']},
	python_requires='>=3.10',
	install_requires=[
		'Rest-OC>=1.0.3',
		'Body-OC>=0.1.2'
	],
	entry_points={
		'console_scripts': ['brain=brain.__main__:cli']
	},
	zip_safe=True
)
