from setuptools import setup, find_packages



long_description = 'Create user bots for amino, as well as scripts for various purposes.'
link = 'https://github.com/xXxCLOTIxXx/AminoXZ/archive/refs/heads/main.zip'
ver = '1.1.8.6'

setup(
    name = "AminoXZ",
    version = ver,
    url = "https://github.com/xXxCLOTIxXx/AminoXZ",
    download_url = link,
    license = "MIT",
    author = "Xsarz",
    author_email = "xsarzy@gmail.com",
    description = "Library for creating amino bots and scripts.",
    long_description = long_description,
    keywords = [
        "aminoapps",
        "aminoxz",
        "amino",
        "amino-bot",
        "narvii",
        "api",
        "python",
        "python3",
        "python3.x",
        "xsarz",
        "official"
    ],
    install_requires = [
        "colored",
        "requests",
        "websocket-client==1.3.1",   
        "websockets"

    ],
    packages = find_packages()
)
