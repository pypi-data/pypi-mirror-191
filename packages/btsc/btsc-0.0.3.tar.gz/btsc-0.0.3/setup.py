from setuptools import setup, find_packages
from os.path import join, dirname


def list_requirements():
    deps = []
    requirements_file = "requirements.txt"
    with open(requirements_file) as f:
        for line in f.readlines():
            if "twine" in line:
                continue
                deps.append(line.strip())
    return deps


setup(
        name="btsc",
        version="0.0.3",
        author="preposing",
        author_email="sebdevpy@gmail.com",
        description="transfer.sh client",
        url="https://github.com/preposing/btsc.git",
        keywords="transfer.sh client tool utility cli CLI",
        license="MIT",
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5'
        ],
        packages=find_packages(),
        long_description=open(join(dirname(__file__), "README.rst")).read(),
        long_description_content_type="text/x-rst",
        install_requires=list_requirements(),
        entry_points={
                "console_scripts":
                ['btsc = btsc.app:main'],
            },
    )
