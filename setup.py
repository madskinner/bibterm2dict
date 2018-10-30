import setuptools
from pub2sd.myclasses.myconst.therest import THIS_VERSION

setuptools.setup(
    name="bibterm2dict",
    version=THIS_VERSION,
    url="https://github.com/madskinner/pub2sd",
    author="Mark Skinner",
    author_email="mark_skinner@sil.org",
    description="Transfer language data from Paratext Biblical Terms list to Map Creator dictionary files.",
    long_description=open('README.rst').read(),
#    data_files=[('../tests', ['set_tags.json', 'default_values.json', 'hash_tag_on.json', 'idiot_tags.json', 'localized_text.json', 'read_tag.json', 'read_tag_hide_encoding.json', 'read_tag_info.json', 'trim_tag.json',]),]
#                ('', ['set_tags.json', 'default_values.json', 'hash_tag_on.json', 'idiot_tags.json', 'localized_text.json', 'read_tag.json', 'read_tag_hide_encoding.json', 'read_tag_info.json', 'trim_tag.json',]),],
    packages=setuptools.find_packages(),
#    package_data={'pub2sd': ['*.html', '*.json', '*.ico', 'images/*.png', 'images/*.jpg', 'images/*.ico']},
    package_data={'bibterm2dict': ['*.html', '*.ico', 'images/*.png', 'images/*.jpg', 'images/*.ico']},
    install_requires=["lxml","psutil","unidecode"],
    license='MIT',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: End Users/Desktop',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6'],
    keywords='map creator dictionary annotated graphics',
    include_package_data=True
)
