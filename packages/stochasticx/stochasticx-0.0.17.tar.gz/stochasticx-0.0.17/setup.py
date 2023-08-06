import setuptools
from pathlib import Path


def add_alias_command(source_command, alias):
    bashrc_path = Path("~/.bashrc").resolve()

    if bashrc_path.exists():
        with open(str(bashrc_path), "a") as bashrc_file:
            bashrc_file.write("\n\n{}={}\n\n".format(source_command, alias))


# add_alias_command("stochasticx", "x")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
   "requests==2.28.1",
   "jwt==1.3.1",
   "Click==8.1.3",
   "tqdm==4.64.1",
   "ipywidgets==8.0.2",
   "tritonclient[all]==2.27.0",
   "docker==6.0.1",
   "numpy==1.23.4",
   "Pillow==9.3.0",
   "diffusers==0.11.1",
   "transformers==4.25.1",
   "rich==12.6.0",
   #"psutil==5.9.4",
   "accelerate==0.14.0",
   "pydantic==1.10.2",
   "pandas==1.5.1"
]

extras_require = {"dev": ["pre-commit==2.20.0"]}

"""scripts=[
   "bin/stochasticx"
]"""

setuptools.setup(
   name='stochasticx',
   version='0.0.17',
   author='Marcos Rivera Martínez, Sarthak Langde, Glenn Ko, Subhash G N, Jolina Li',
   author_email='marcos.rm@stochastic.ai, sarthak.langde@stochastic.ai, glenn@stochastic.ai, subhash.gn@stochastic.ai, jolina.li@mail.utoronto.ca',
   description='Stochastic client library',
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/stochasticai/stochasticx",
   classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points="""
      [console_scripts]
      stochasticx=stochasticx.scripts.stochasticx:cli
   """,
)
