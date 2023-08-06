from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="TensorPG",
    version="0.0.3",
    description="Various Deep Learning Models (tensorflow)",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Shivam-21-11/Tf-Model-Packages",
    author="Shivam Singh",
    author_email="Shivamsingh2111@gmail.com",
    keywords=["Machine Learning","Computer Vision", "Generative adversarial networks","Deep Learning","Transformer","NLP"],
    license="MIT",
    packages=["modelpg","modelpg.GAN","modelpg.Helper","modelpg.Transformer"],
    install_requires=['tensorflow','numpy','keras','matplotlib','tensorflow_text'],
    include_package_data=True,
)