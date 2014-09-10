from distutils.core import setup

setup(name="PyPDEVS",
      version="2.2.3",
      description="Python Parallel DEVS simulator",
      author="Yentl Van Tendeloo",
      author_email="yentl.vantendeloo@student.uantwerpen.be",
      url="http://msdl.cs.mcgill.ca/people/yentl",
      packages=['pypdevs'],
      package_dir={'pypdevs': './'},
      package_data={'pypdevs': ['../docs/generated/']}
)
