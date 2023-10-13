from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='BalancerPy',
      version='0.0.4',
      description='Balancer for Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/icmoore/balancerpy',
      author = "icmoore",
      author_email = "imoore@syscoin.org",
      license='MIT',
      package_dir = {"balancerpy": "python/prod"},
      packages=[
          'balancerpy.cwpt.exchg',
          'balancerpy.cwpt.exchg.result',
          'balancerpy.cwpt.factory',
          'balancerpy.erc',
          'balancerpy.group',
          'python.prod.cwpt.exchg',
          'python.prod.cwpt.exchg.result',
          'python.prod.cwpt.factory',
          'python.prod.erc',
          'python.prod.group'
      ],
      zip_safe=False)
