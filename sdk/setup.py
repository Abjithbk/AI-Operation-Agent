from setuptools import setup, find_packages

setup(
    name="aiops-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    author="Abjith",
    description="AI-powered observability SDK for Python applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Abjithbk/AI-Operation-Agent", 
    project_urls={
        "Bug Tracker": "https://github.com/Abjithbk/AI-Operation-Agent/issues",
        "Source Code": "https://github.com/Abjithbk/AI-Operation-Agent",
    },
    python_requires=">=3.8",
)