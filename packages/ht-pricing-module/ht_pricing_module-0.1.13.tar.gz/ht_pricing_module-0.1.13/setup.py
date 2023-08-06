from setuptools import setup, find_packages


def filter_package():
    packages = []
    packages_all = find_packages()
    for i in packages_all:
        if i.split(".")[0] == 'ht_pricing_module':
            packages.append(i)
    return packages


version = "0.1.13"

setup(name="ht_pricing_module",
      version=version,
      author="wangjun",
      readme="README.md",
      description="huatai option pricing module",
      author_email="wangjun@htgwfzb.com",
      url='http://10.17.75.129:9002/wangjun/ht_pricing_server/-/tree/main/ht_pricing_module',
      requires_python=">=3.6",

      packages=filter_package(),
      include_package_data=True,
      platforms="any",
      install_requires=['numpy', 'scipy', 'pandas']
      )

# py -m build
# python .\setup.py bdist_egg
# py -m twine upload .\dist\*
# py -m twine upload --repository testpypi dist/*
# pip install ht-pricing-module -i https://pypi.python.org/simple
# pip install ht-pricing-module -i https://test.pypi.org/simple/
