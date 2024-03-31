import setuptools

if __name__ == "__main__":
    setuptools.setup(
        entry_points={
            "console_scripts": ["djinn=cli:app"],
        }
    )
