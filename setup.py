from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(name="stockscan",
      description="Simple stock scanner",
      long_description=readme(),
      author=["Tsai-Wei Chiu", "Wei-Yi Cheng"],
      author_email=["hidy0503@gmail.com", "ninpy.weiyi@gmail.com"],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3.6"
      ],
      packages=find_packages(),
      install_requires=[
          "numpy",
          "requests"
      ],
      # extras_require={"test": ["nose", "nose-parameterized>=0.5", "mock"]},
      entry_points={
          "console_scripts": [
              "scan-stocks=stockscan.scan_stocks:main",
          ],
      },
      include_package_data=True,
      zip_safe=False)
