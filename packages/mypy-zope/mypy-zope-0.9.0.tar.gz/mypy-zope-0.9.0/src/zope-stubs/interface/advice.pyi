# Stubs for zope.interface.advice (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

def getFrameInfo(frame: Any): ...
def addClassAdvisor(callback: Any, depth: int = ...): ...
def isClassAdvisor(ob: Any): ...
def determineMetaclass(bases: Any, explicit_mc: Optional[Any] = ...): ...
def minimalBases(classes: Any): ...
