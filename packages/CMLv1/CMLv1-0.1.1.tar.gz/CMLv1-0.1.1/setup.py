import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")
setuptools.setup(
    name = "CMLv1",
    version = "0.1.1",
    author="fyc",
    author_email="fycsfls_winter@126.com",
    description = "A support library for CheckoutMachineApplication.",
    readme = "README.md",
    python_requires = ">=3.7",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    project_urls = {
        "Documentation" : "https://you.wont.expect.me.to.give.you.a.documentation.right/"
    }
)
