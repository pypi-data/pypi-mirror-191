################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3",
		"Topic :: System :: Monitoring",
	],
	description = "This python module provides ways to retrieve and parse technical system data of Linux computer systems.",
	include_package_data = True,
	install_requires = [
		"python-dateutil",
		"fabric",
		"pytz",
		"jk_console",
		"jk_typing",
		"jk_version",
		"jk_cachefunccalls",
		"jk_argparsing",
		"jk_etcpasswd",
		"jk_cmdoutputparsinghelper",
		"jk_json",
		"jk_flexdata",
		"jk_utils",
		"jk_logging",
	],
	keywords = [
		"monitoring",
		"os",
	],
	license = "Apache2",
	name = "jk_sysinfo",
	package_data = {
		"": [
		],
	},
	packages = [
		"jk_sysinfo",
		"jk_sysinfo.entity",
	],
	scripts = [
		"bin/sysinfo.py",
		"bin/sysinfo_json.py",
	],
	version = '0.2023.2.10',
	zip_safe = False,
	long_description = readme(),
	long_description_content_type = "text/markdown",
)
