import setuptools

setuptools.setup(
    name="cyberfame-tools",
    version="2023.02.10-3",
    description="helper tools for cyberfame project",
    long_description=open("README.md").read().strip(),
    author="Cyberfame Team",
    author_email="contact@morphysm.com",
    # TODO: Open-source
    # url="https://github.com/kittyandrew/telethon-tgcrypto",
    url=None,
    packages=setuptools.find_packages(),
    install_requires=[],
    # TODO: Open-source
    # license="MIT License",
    license=None,
    keywords="cyberfame tools",
    classifiers=[
        "Development Status :: 4 - Beta",
        # TODO: Open-source
        # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
