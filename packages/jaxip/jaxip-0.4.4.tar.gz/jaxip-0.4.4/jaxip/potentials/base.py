# from abc import ABCMeta, abstractmethod
# from typing import Dict

# from jaxip.structure import Structure
# from jaxip.types import Array, Element


# class Potential(metaclass=ABCMeta):
#     """
#     A base potential class.
#     """

#     @abstractmethod
#     def init_atomic_potential(self) -> None:
#         pass

#     @abstractmethod
#     def __call__(self, structure: Structure) -> Array:
#         """
#         Compute total energy.
#         """
#         pass

#     @abstractmethod
#     def compute_force(self, structure: Structure) -> Dict[Element, Array]:
#         pass

#     @abstractmethod
#     def fit(self) -> None:
#         """
#         This method provides a user-friendly interface to fit both descriptor and model in one step.
#         """
#         pass
