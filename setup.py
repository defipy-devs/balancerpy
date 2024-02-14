from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='BalancerPy',
      version='0.0.8',
      description='Balancer Analytics with Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/defipy-devs/balancerpy',
      author = "icmoore",
      author_email = "defipy.devs@gmail.com",
      license='MIT',
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
          'balancerpy.utils.data'     
      ],
      zip_safe=False)
