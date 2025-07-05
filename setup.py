from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='BalancerPy',
      version='1.0.2',
      description='Balancer Analytics with Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/defipy-devs/balancerpy',
      author = "icmoore",
      author_email = "defipy.devs@gmail.com",
      license="Apache-2.0",
      classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
      ],
      package_dir = {"balancerpy": "python/prod"},
      packages=[
          'balancerpy',
          'balancerpy.cwpt.exchg',
          'balancerpy.cwpt.exchg.result',
          'balancerpy.cwpt.factory',
          'balancerpy.erc',
          'balancerpy.vault',
          'balancerpy.quote',
          'balancerpy.constants',
          'balancerpy.utils.interfaces',
          'balancerpy.utils.data',
          'balancerpy.process.liquidity',
          'balancerpy.process.swap',
          'balancerpy.process.join',
          'balancerpy.enums'
      ],
      install_requires=[
          'uniswappy >= 1.7.2'
      ],
      zip_safe=False)
