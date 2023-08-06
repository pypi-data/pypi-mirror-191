from setuptools import setup
from setuptools.command.install import install

name = f"shapely-stubs"

description = f"A dummy placeholder for the `{name}` package"
error_msg = f"{name} is not ready yet. Once it is ready it will be available here."

readme = f"""
{name} package
{'='*len(name)}========
{description}

{error_msg}
"""
readme_type = "text/x-rst"


class PostInstallCommand(install):
    def run(self):
        raise Exception(error_msg)


cmdclass = dict(install=PostInstallCommand)

setup(
    name=name,
    description=description,
    long_description=readme,
    license="MIT",
    long_description_content_type=readme_type,
    version="0.0.a0",
    cmdclass=cmdclass,
)
