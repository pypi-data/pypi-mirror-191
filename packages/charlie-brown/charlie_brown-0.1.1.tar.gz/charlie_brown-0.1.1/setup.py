import setuptools, ast

with open('README.rst', 'r') as o:
    long_description = o.read()

with open('charlie_brown/_version.py', 'r') as o:
    version = ast.literal_eval(ast.parse(o.read()).body[0].value)

setuptools.setup(
    name = 'charlie_brown',
    version = version,
    author = 'Kodi B. Arfer',
    description = 'Check your email with IMAP IDLE and preview messages',
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    project_urls = {
        'Source Code': 'https://github.com/Kodiologist/Charlie-Brown'},
    install_requires = [
        'hy >= 0.26.*',
        'hyrule >= 0.3.*',
        'imapclient',
        'metadict',
        'humanize',
        'setproctitle'],
    packages = setuptools.find_packages(),
    package_data = {
        'charlie_brown': ['*.hy', '__pycache__/*']},
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent'])
