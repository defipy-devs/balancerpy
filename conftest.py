import sys, os, types

_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _root)

_prod = os.path.join(_root, "python", "prod")

# Pre-register python.prod as a namespace package so that
# 'from python.prod.erc import ERC20' works without triggering
# python/prod/__init__.py (which imports from the installed package).
for _ns in ("python", "python.prod"):
    if _ns not in sys.modules:
        _m = types.ModuleType(_ns)
        _m.__path__ = [os.path.join(_root, *_ns.split("."))]
        _m.__package__ = _ns
        sys.modules[_ns] = _m

# The editable install maps 'balancerpy' -> 'python/prod'.  When
# modules are first imported via 'python.prod.*', the relative imports
# inside production code resolve through the 'python.prod' namespace,
# and Python registers submodule files (e.g. BalancerExchange.py) as
# modules that shadow the class exports from __init__.py.
#
# Fix: after all python.prod.* modules are loaded, patch the factory
# module so its BalancerExchange reference points to the class.
import python.prod.cwpt.factory.BalancerFactory as _factory_mod  # noqa: E402
from python.prod.cwpt.exchg.BalancerExchange import BalancerExchange as _BE_cls  # noqa: E402
_factory_mod.BalancerExchange = _BE_cls
