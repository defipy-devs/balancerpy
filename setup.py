from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='BalancerPy',
      version='0.0.5',
      description='Balancer for Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/icmoore/balancerpy',
      author = "icmoore",
      author_email = "utiliwire@gmail.com",
      license='MIT',
      package_dir = {"balancerpy": "python/prod"},
      packages=[
          'balancerpy',
          'balancerpy.cwpt.exchg',
          'balancerpy.cwpt.exchg.result',
          'balancerpy.cwpt.factory',
          'balancerpy.erc',
          'balancerpy.vault'
      ],
      zip_safe=False)
