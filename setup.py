import setuptools


setuptools.setup(
    name="tmux-projector",
    version="0.0.2",
    author_email="avjves@gmail.com",
    description="Tool to start tmux projects more easily",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    entry_points={
        'console_scripts': ['ts=tmux_projector.run:main']
    }
)
