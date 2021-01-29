from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, unique
from functools import reduce
from typing import Tuple, Union, List, Optional

from common import Limit, SingletonABCMeta, Direction, SteelPlate, CommonUtils, \
    ImpactEnergy, ChemicalElementValue, Thickness, YieldStrength, TensileStrength, Elongation, Temperature, \
    Specification, DeliveryCondition, PositionDirectionImpact


@unique
class LimitType(Enum):
    MAXIMUM = 1
    MINIMUM = 2
    RANGE = 3
    UNIQUE = 4
    SCOPE = 5


@dataclass
class ChemicalCompositionLimit(Limit):
    chemical_element: str
    limit_type: LimitType
    maximum: float = None,
    minimum: float = None,
    unit: str = '% by weight'

    def __post_init__(self):
        self.self_inspection()

    def self_inspection(self):
        if self.limit_type == LimitType.MAXIMUM:
            if self.maximum is None or str(type(self.maximum)) != "<class 'float'>":
                raise ValueError(
                    f"Maximum value {self.maximum} is not properly specified for chemical element "
                    f"{self.chemical_element} limit type {self.limit_type}. Current type is {str(type(self.maximum))}."
                )
        elif self.limit_type == LimitType.MINIMUM:
            if self.minimum is None or str(type(self.minimum)) != "<class 'float'>":
                raise ValueError(
                    f"Minimum value {self.minimum} is not properly specified for chemical element "
                    f"{self.chemical_element} limit type {self.limit_type}. Current type is {str(type(self.maximum))}."
                )
        elif self.limit_type == LimitType.RANGE:
            if self.maximum is None or str(type(self.maximum)) != "<class 'float'>":
                raise ValueError(
                    f"Maximum value {self.maximum} is not properly specified for chemical element "
                    f"{self.chemical_element} limit type {self.limit_type}. Current type is {str(type(self.maximum))}."
                )
            if self.minimum is None or str(type(self.minimum)) != "<class 'float'>":
                raise ValueError(
                    f"Minimum value {self.minimum} is not properly specified for chemical element "
                    f"{self.chemical_element} limit type {self.limit_type}. Current type is {str(type(self.maximum))}."
                )
        else:
            raise ValueError(
                f"The limit type {self.limit_type} is not expected in ChemicalCompositionLimit."
            )

    def verify_value(self, value: float) -> Tuple[bool, str]:
        if self.limit_type == LimitType.MAXIMUM:
            if value <= self.maximum:
                message = (
                    f"[PASS] The value of chemical element {self.chemical_element} is {value}, meets the maximum "
                    f"limit {self.maximum} {self.unit}."
                )
                print(message)
                return True, message
            else:
                message = (
                    f"[FAIL] The value of chemical element {self.chemical_element} is {value}, violates the maximum "
                    f"limit {self.maximum} {self.unit}."
                )
                print(message)
                return False, message
        elif self.limit_type == LimitType.MINIMUM:
            if value >= self.minimum:
                message = (
                    f"[PASS] The value of chemical element {self.chemical_element} is {value}, meets the minimum "
                    f"limit {self.minimum} {self.unit}."
                )
                print(message)
                return True, message
            else:
                message = (
                    f"[FAIL] The value of chemical element {self.chemical_element} is {value}, violates the minimum "
                    f"limit {self.minimum} {self.unit}."
                )
                print(message)
                return False, message
        elif self.limit_type == LimitType.RANGE:
            if self.minimum <= value <= self.maximum:
                message = (
                    f"[PASS] The value of chemical element {self.chemical_element} is {value}, meets the valid "
                    f"range [{self.minimum}, {self.maximum}] {self.unit}."
                )
                print(message)
                return True, message
            else:
                message = (
                    f"[FAIL] The value of chemical element {self.chemical_element} is {value}, violates the valid "
                    f"range [{self.minimum}, {self.maximum}]. {self.unit}"
                )
                print(message)
                return False, message

    def get_element(self, plate: SteelPlate) -> Tuple[List[ChemicalElementValue], float]:
        if self.chemical_element == 'C + 1/6 Mn':
            c = self.get_element_by_name(plate, 'C')
            mn = self.get_element_by_name(plate, 'Mn')
            return [c, mn], c.calculated_value + mn.calculated_value / 6
        elif self.chemical_element == 'Nb + V + Ti':
            nb = self.get_element_by_name(plate, 'Nb')
            v = self.get_element_by_name(plate, 'V')
            ti = self.get_element_by_name(plate, 'Ti')
            return [nb, v, ti], nb.calculated_value + v.calculated_value + ti.calculated_value
        else:
            element = self.get_element_by_name(plate, self.chemical_element)
            return [element], element.calculated_value

    @staticmethod
    def get_element_by_name(plate: SteelPlate, element_name: str) -> ChemicalElementValue:
        if element_name in plate.chemical_compositions:
            return plate.chemical_compositions[element_name]
        else:
            raise ValueError(
                f"Could not find chemical composition value for {element_name} which is required to be checked in the "
                f"{CommonUtils.ordinal(plate.serial_number.value)} steel plate."
            )

    def verify(self, plate: SteelPlate) -> bool:
        elements, value = self.get_element(plate)
        valid_flag, message = self.verify_value(value)
        for element in elements:
            element.valid_flag = valid_flag
            # element.message = message
            # element.message = message if element.message is None else (element.message + ' ' + message)
            if element.message is None:
                element.message = message
            else:
                if valid_flag:
                    element.message = element.message + ' ' + message
                else:
                    element.message = message + ' ' + element.message
        return valid_flag


@dataclass
class BaoSteelAlLimit(Limit):
    alt_limit: ChemicalCompositionLimit = ChemicalCompositionLimit(
        chemical_element='Alt',
        limit_type=LimitType.MINIMUM,
        minimum=0.015
    )
    als_limit: ChemicalCompositionLimit = ChemicalCompositionLimit(
        chemical_element='Als',
        limit_type=LimitType.MINIMUM,
        minimum=0.010
    )

    def verify_value(self, value) -> Tuple[bool, str]:
        alt_value, als_value = value
        alt_valid_flag, alt_message = self.alt_limit.verify_value(alt_value)
        als_valid_flag, als_message = self.als_limit.verify_value(als_value)
        if alt_valid_flag or als_valid_flag:
            return True, alt_message + ' ' + als_message
        else:
            return False, alt_message + ' ' + als_message

    # might be not used in the actual run, but was tested in test suites.
    def verify(self, plate: SteelPlate) -> bool:
        elements, value = self.get_element(plate)
        valid_flag, message = self.verify_value(value)
        for element in elements:
            element.valid_flag = valid_flag
            element.message = message
        return valid_flag

    def get_element(self, plate: SteelPlate):
        if 'Alt' in plate.chemical_compositions:
            alt = plate.chemical_compositions['Alt']
        else:
            raise ValueError(
                f"Could not find chemical composition value for Alt which is required to be checked in the "
                f"{CommonUtils.ordinal(plate.serial_number.value)} steel plate."
            )
        if 'Als' in plate.chemical_compositions:
            als = plate.chemical_compositions['Als']
        else:
            raise ValueError(
                f"Could not find chemical composition value for Als which is required to be checked in the "
                f"{CommonUtils.ordinal(plate.serial_number.value)} steel plate."
            )
        return [alt, als], (alt.calculated_value, als.calculated_value)


@dataclass
class FineGrainElementLimit(Limit):
    concurrent_limits: List[Union[ChemicalCompositionLimit, BaoSteelAlLimit]]

    def verify(self, plate: SteelPlate) -> bool:
        return FineGrainElementLimit.verify_limit(plate, self.concurrent_limits)

    # @staticmethod
    # def verify_limit(plate: SteelPlate, limits_to_check: List[Limit]) -> bool:
    #     if len(limits_to_check) > 1:
    #         limit = limits_to_check[0]
    #         if isinstance(limit, ChemicalCompositionLimit):
    #             elements, value = limit.get_element(plate)
    #             valid_flag, message = limit.verify_value(value)
    #             if valid_flag:
    #                 if FineGrainElementLimit.verify_limit(plate, limits_to_check[1:]):
    #                     for element in elements:
    #                         element.valid_flag = valid_flag  # True
    #                         element.message = message
    #                     return valid_flag  # True
    #             else:
    #                 return False
    #         else:
    #             raise ValueError(
    #                 f"limit {limit} is not a ChemicalCompositionLimit."
    #             )
    #     # now there should be only one limit in the list.
    #     else:
    #         limit = limits_to_check[0]
    #         if isinstance(limit, ChemicalCompositionLimit):
    #             elements, value = limit.get_element(plate)
    #             valid_flag, message = limit.verify_value(value)
    #             if valid_flag:  # True
    #                 for element in elements:
    #                     element.valid_flag = valid_flag  # True
    #                     element.message = message
    #                 return valid_flag  # True
    #         else:
    #             raise ValueError(
    #                 f"limit {limit} is not a ChemicalCompositionLimit."
    #             )

    @staticmethod
    def verify_limit(plate: SteelPlate,
                     limits_to_check: List[Union[ChemicalCompositionLimit, BaoSteelAlLimit]]) -> bool:
        limit = limits_to_check[0]
        elements, value = limit.get_element(plate)
        valid_flag, message = limit.verify_value(value)
        if valid_flag:
            if len(limits_to_check) == 1:
                for element in elements:
                    element.valid_flag = True
                    element.message = message if element.message is None else element.message + ' ' + message
                return True
            else:
                if FineGrainElementLimit.verify_limit(plate, limits_to_check[1:]):
                    for element in elements:
                        element.valid_flag = True
                        element.message = message if element.message is None else element.message + ' ' + message
                    return True
                else:
                    return False
        else:
            return False

    # DO NOT USE
    def verify_value(self, value) -> Tuple[bool, str]:
        pass

    def get_element(self, plate: SteelPlate):
        return reduce(lambda x, y: x + [element for element in y if element not in x],
                      [limit.get_element(plate)[0] for limit in self.concurrent_limits])


@dataclass
class FineGrainElementLimitCombination(Limit):
    fine_grain_element_limits: Optional[List[FineGrainElementLimit]]
    error_message: Optional[str]

    def verify(self, plate: SteelPlate) -> bool:
        if self.fine_grain_element_limits is None or len(self.fine_grain_element_limits) == 0:
            return True
        else:
            if FineGrainElementLimitCombination.verify_limit(plate, self.fine_grain_element_limits):
                return True
            else:
                for element in self.get_element(plate):
                    element.valid_flag = False
                    element.message = self.error_message
                return False

    @staticmethod
    def verify_limit(plate: SteelPlate, limits_to_check: List[FineGrainElementLimit]):
        limit = limits_to_check[0]
        if limit.verify(plate):
            return True
        else:
            if len(limits_to_check) > 1:
                return FineGrainElementLimitCombination.verify_limit(plate, limits_to_check[1:])

    # DO NOT USE
    def verify_value(self, value) -> Tuple[bool, str]:
        pass

    def get_element(self, plate: SteelPlate):
        return reduce(lambda x, y: x + [element for element in y if element not in x],
                      [limit.get_element(plate) for limit in self.fine_grain_element_limits])


# class ChemicalCompositionCombinedLimit(Limit):
#     @abstractmethod
#     def verify(self, value) -> Tuple[bool, str]:
#         pass
#
#     def get_value(self, certificate: Certificate, steel_plate_index: int) -> Dict[str, ChemicalElementValue]:
#         return certificate.steel_plates[steel_plate_index].chemical_compositions
#
#     @staticmethod
#     def get_element_value(element_name: str,
#                           chemical_composition: Dict[str, ChemicalElementValue]) -> ChemicalElementValue:
#         if element_name in chemical_composition:
#             return chemical_composition[element_name]
#         else:
#             raise ValueError(
#                 f"Element {element_name} is required but missing in this certificate."
#             )


# class CPlusMnLimit(ChemicalCompositionCombinedLimit):
#     def verify(self, value) -> Tuple[bool, str]:
#         chemical_composition: Dict[str, ChemicalElementValue] = value
#         c = self.get_element_value('C', chemical_composition)
#         mn = self.get_element_value('Mn', chemical_composition)
#         c_mn_combined_value = c.calculated_value + mn.calculated_value / 6
#         if c_mn_combined_value <= 0.40:
#             message = (
#                 f"[PASS] The value of C + 1/6 Mn is {c_mn_combined_value}, meets the maximum limit 0.40 % by weight."
#             )
#             print(message)
#             c.valid_flag = c.valid_flag and True
#             c.message = c.message + ' ' + message
#             mn.valid_flag = mn.valid_flag and True
#             mn.message = mn.message + ' ' + message
#             return True, message
#         else:
#             message = (
#                 f"[FAIL] The value of C + 1/6 Mn is {c_mn_combined_value}, violates the maximum limit 0.40 % by "
#                 f"weight."
#             )
#             print(message)
#             c.valid_flag = False
#             c.message = c.message + ' ' + message
#             mn.valid_flag = False
#             mn.message = mn.message + ' ' + message
#             return False, message


# class NormalStrengthSteelFineGrainAlLimit(ChemicalCompositionCombinedLimit):
#     def verify(self, value) -> Tuple[bool, str]:
#         chemical_composition: Dict[str, ChemicalElementValue] = value
#         alt = self.get_element_value('Alt', chemical_composition)
#         als = self.get_element_value('Als', chemical_composition)
#         alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.020).verify(alt.calculated_value)
#         als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.015).verify(als.calculated_value)
#         if alt.valid_flag and not als.valid_flag:
#             als.valid_flag = True
#         elif als.valid_flag and not alt.valid_flag:
#             alt.valid_flag = True
#
#         if alt.valid_flag and als.valid_flag:
#             return True, ''
#         else:
#             return False, ''
#
#     def __str__(self):
#         return 'Al'


# class NormalStrengthSteelFineGrainAlPlusTiLimit(ChemicalCompositionCombinedLimit):
#     def verify(self, value) -> Tuple[bool, str]:
#         chemical_composition: Dict[str, ChemicalElementValue] = value
#         alt = self.get_element_value('Alt', chemical_composition)
#         als = self.get_element_value('Als', chemical_composition)
#         ti = self.get_element_value('Ti', chemical_composition)
#         alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.015).verify(alt.calculated_value)
#         als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.010).verify(als.calculated_value)
#         ti.valid_flag, ti.message = ChemicalCompositionLimit(chemical_element='Ti', limit_type=LimitType.MINIMUM,
#                                                              minimum=0.007).verify(ti.calculated_value)
#
#         if alt.valid_flag and not als.valid_flag:
#             als.valid_flag = True
#         elif als.valid_flag and not alt.valid_flag:
#             alt.valid_flag = True
#
#         if alt.valid_flag and als.valid_flag and ti.valid_flag:
#             return True, ''
#         else:
#             return False, ''
#
#     def __str__(self):
#         return 'Al+Ti'
#
#
# class NormalStrengthSteelFineGrainAlPlusNbLimit(ChemicalCompositionCombinedLimit):
#     def verify(self, value) -> Tuple[bool, str]:
#         chemical_composition: Dict[str, ChemicalElementValue] = value
#         alt = self.get_element_value('Alt', chemical_composition)
#         als = self.get_element_value('Als', chemical_composition)
#         nb = self.get_element_value('Nb', chemical_composition)
#         alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.015).verify(alt.calculated_value)
#         als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.010).verify(als.calculated_value)
#         nb.valid_flag, nb.message = ChemicalCompositionLimit(chemical_element='Nb', limit_type=LimitType.MINIMUM,
#                                                              minimum=0.010).verify(nb.calculated_value)
#
#         if alt.valid_flag and not als.valid_flag:
#             als.valid_flag = True
#         elif als.valid_flag and not alt.valid_flag:
#             alt.valid_flag = True
#
#         if alt.valid_flag and als.valid_flag and nb.valid_flag:
#             return True, ''
#         else:
#             return False, ''
#
#     def __str__(self):
#         return 'Al+Nb'
#
#
# class NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit(ChemicalCompositionCombinedLimit):
#     def verify(self, value) -> Tuple[bool, str]:
#         chemical_composition: Dict[str, ChemicalElementValue] = value
#         alt = self.get_element_value('Alt', chemical_composition)
#         als = self.get_element_value('Als', chemical_composition)
#         nb = self.get_element_value('Nb', chemical_composition)
#         ti = self.get_element_value('Ti', chemical_composition)
#         alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.015).verify(alt.calculated_value)
#         als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.010).verify(als.calculated_value)
#         nb.valid_flag, nb.message = ChemicalCompositionLimit(chemical_element='Nb', limit_type=LimitType.MINIMUM,
#                                                              minimum=0.010).verify(nb.calculated_value)
#         ti.valid_flag, ti.message = ChemicalCompositionLimit(chemical_element='Ti', limit_type=LimitType.MINIMUM,
#                                                              minimum=0.007).verify(ti.calculated_value)
#
#         if alt.valid_flag and not als.valid_flag:
#             als.valid_flag = True
#         elif als.valid_flag and not alt.valid_flag:
#             alt.valid_flag = True
#
#         if alt.valid_flag and als.valid_flag and nb.valid_flag and ti.valid_flag:
#             return True, ''
#         else:
#             return False, ''
#
#     def __str__(self):
#         return 'Al+Nb+Ti'
#
#
# class HighStrengthSteelFineGrainAlPlusTiLimit(ChemicalCompositionCombinedLimit):
#     def verify(self, value) -> Tuple[bool, str]:
#         chemical_composition: Dict[str, ChemicalElementValue] = value
#         alt = self.get_element_value('Alt', chemical_composition)
#         als = self.get_element_value('Als', chemical_composition)
#         ti = self.get_element_value('Ti', chemical_composition)
#         alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.015).verify(alt.calculated_value)
#         als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.010).verify(als.calculated_value)
#         ti.valid_flag, ti.message = ChemicalCompositionLimit(chemical_element='Ti', limit_type=LimitType.RANGE,
#                                                              minimum=0.007, maximum=0.02).verify(ti.calculated_value)
#
#         if alt.valid_flag and not als.valid_flag:
#             als.valid_flag = True
#         elif als.valid_flag and not alt.valid_flag:
#             alt.valid_flag = True
#
#         if alt.valid_flag and als.valid_flag and ti.valid_flag:
#             return True, ''
#         else:
#             return False, ''
#
#     def __str__(self):
#         return 'Al+Ti'
#
#
# class HighStrengthSteelFineGrainAlPlusNbPlusTiLimit(ChemicalCompositionCombinedLimit):
#     def verify(self, value) -> Tuple[bool, str]:
#         chemical_composition: Dict[str, ChemicalElementValue] = value
#         alt = self.get_element_value('Alt', chemical_composition)
#         als = self.get_element_value('Als', chemical_composition)
#         nb = self.get_element_value('Nb', chemical_composition)
#         ti = self.get_element_value('Ti', chemical_composition)
#         alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.015).verify(alt.calculated_value)
#         als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.010).verify(als.calculated_value)
#         nb.valid_flag, nb.message = ChemicalCompositionLimit(chemical_element='Nb', limit_type=LimitType.RANGE,
#                                                              minimum=0.010, maximum=0.050).verify(nb.calculated_value)
#         ti.valid_flag, ti.message = ChemicalCompositionLimit(chemical_element='Ti', limit_type=LimitType.RANGE,
#                                                              minimum=0.007, maximum=0.020).verify(ti.calculated_value)
#
#         if alt.valid_flag and not als.valid_flag:
#             als.valid_flag = True
#         elif als.valid_flag and not alt.valid_flag:
#             alt.valid_flag = True
#
#         if alt.valid_flag and als.valid_flag and nb.valid_flag and ti.valid_flag:
#             return True, ''
#         else:
#             return False, ''
#
#     def __str__(self):
#         return 'Al+Nb+Ti'


# class HighStrengthSteelFineGrainAlPlusNbPlusTiPlusVLimit(ChemicalCompositionCombinedLimit):
#     def verify(self, value) -> Tuple[bool, str]:
#         chemical_composition: Dict[str, ChemicalElementValue] = value
#         alt = self.get_element_value('Alt', chemical_composition)
#         als = self.get_element_value('Als', chemical_composition)
#         nb = self.get_element_value('Nb', chemical_composition)
#         ti = self.get_element_value('Ti', chemical_composition)
#         v = self.get_element_value('V', chemical_composition)
#         alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.015).verify(alt.value)
#         als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
#                                                                minimum=0.010).verify(als.value)
#         nb.valid_flag, nb.message = ChemicalCompositionLimit(chemical_element='Nb', limit_type=LimitType.RANGE,
#                                                              minimum=0.010, maximum=0.050).verify(nb.value)
#         ti.valid_flag, ti.message = ChemicalCompositionLimit(chemical_element='Ti', limit_type=LimitType.RANGE,
#                                                              minimum=0.007, maximum=0.020).verify(ti.value)
#         v.valid_flag, v.message = ChemicalCompositionLimit(chemical_element='V', limit_type=LimitType.RANGE,
#                                                            minimum=0.03, maximum=0.10).verify(v.value)
#
#         if alt.valid_flag and not als.valid_flag:
#             als.valid_flag = True
#         elif als.valid_flag and not alt.valid_flag:
#             alt.valid_flag = True
#
#         if nb.value + v.value + ti.value <= 0.12:
#             message = (
#                 f" [PASS] The additional condition is [Nb+V+Ti <= 0.12], currently [Nb={nb.value}], [V={v.value}], "
#                 f"[Ti={ti.value}], so [Nb+V+Ti={nb.value + v.value + ti.value}] meets the limit 0.12."
#             )
#             nb.message += message
#             v.message += message
#             ti.message += message
#         else:
#             message = (
#                 f" [FAIL] The additional condition is [Nb+V+Ti <= 0.12], currently [Nb={nb.value}], [V={v.value}], "
#                 f"[Ti={ti.value}], so [Nb+V+Ti={nb.value + v.value + ti.value}] violates the limit 0.12."
#             )
#             nb.valid_flag = False
#             nb.message += message
#             v.valid_flag = False
#             v.message += message
#             ti.valid_flag = False
#             ti.message += message
#
#         if alt.valid_flag and als.valid_flag and nb.valid_flag and ti.valid_flag and v.valid_flag:
#             return True, ''
#         else:
#             return False, ''


@dataclass
class ThicknessLimit(Limit):
    maximum: Union[float, int]
    minimum: Union[float, int] = 0
    limit_type: LimitType = LimitType.RANGE
    unit: str = 'mm'

    def verify_value(self, value: float) -> Tuple[bool, str]:
        if self.minimum < value <= self.maximum:
            message = (
                f"[PASS] Thickness value is {value}, meets the valid range ({self.minimum}, {self.maximum}] "
                f"{self.unit}."
            )
            print(message)
            return True, message
        else:
            message = (
                f"[FAIL] Thickness value is {value}, violates the valid range ({self.minimum}, {self.maximum}] "
                f"{self.unit}."
            )
            print(message)
            return False, message

    def get_element(self, plate: SteelPlate) -> Thickness:
        if plate.thickness:
            return plate.thickness
        else:
            raise ValueError(
                f"Could not find value of thickness in the {CommonUtils.ordinal(plate.serial_number.value)} steel "
                f"plate."
            )

    def verify(self, plate: SteelPlate) -> bool:
        thickness = self.get_element(plate)
        thickness.valid_flag, thickness.message = self.verify_value(thickness.value)
        return thickness.valid_flag


@dataclass
class SpecificationLimit(Limit):
    scope: List[str]
    limit_type: LimitType = LimitType.SCOPE

    def verify_value(self, value: str) -> Tuple[bool, str]:
        if value in self.scope:
            message = f"[PASS] Specification value is {value}, meets the valid scope {self.scope}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Specification value is {value}, violates the valid scope {self.scope}."
            print(message)
            return False, message

    def get_element(self, plate: SteelPlate) -> Specification:
        if plate.specification:
            return plate.specification
        else:
            raise ValueError(
                f"Could not find value of specification in the {CommonUtils.ordinal(plate.serial_number.value)} steel "
                f"plate."
            )

    def verify(self, plate: SteelPlate) -> bool:
        specification = self.get_element(plate)
        specification.valid_flag, specification.message = self.verify_value(specification.value)
        return specification.valid_flag


@dataclass
class PositionDirectionImpactLimit(Limit):
    scope: Tuple[Direction] = (Direction.LONGITUDINAL, Direction.TRANSVERSE)
    limit_type: LimitType = LimitType.SCOPE

    def verify_value(self, value: Direction) -> Tuple[bool, str]:
        if value in self.scope:
            message = f"[PASS] Direction value is {value}, meets the valid scope {self.scope}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Direction value is {value}, violates the valid scope {self.scope}."
            print(message)
            return False, message

    def get_element(self, plate: SteelPlate) -> PositionDirectionImpact:
        if plate.position_direction_impact:
            return plate.position_direction_impact
        else:
            raise ValueError(
                f"Could not find value of direction in the {CommonUtils.ordinal(plate.serial_number.value)} "
                f"steel plate."
            )

    def verify(self, plate: SteelPlate) -> bool:
        direction = self.get_element(plate)
        direction.valid_flag, direction.message = self.verify_value(direction.value)
        return direction.valid_flag


@dataclass
class DeliveryConditionLimit(Limit):
    scope: List[str]
    limit_type: LimitType = LimitType.SCOPE

    def verify_value(self, value: str) -> Tuple[bool, str]:
        if value in self.scope:
            message = f"[PASS] Delivery condition value is {value}, meets the valid scope {self.scope}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Delivery condition value is {value}, violates the valid scope {self.scope}."
            print(message)
            return False, message

    def get_element(self, plate: SteelPlate) -> DeliveryCondition:
        if plate.delivery_condition:
            return plate.delivery_condition
        else:
            raise ValueError(
                f"Could not find value of delivery condition in the {CommonUtils.ordinal(plate.serial_number.value)} "
                f"steel plate."
            )

    def verify(self, plate: SteelPlate) -> bool:
        delivery_condition = self.get_element(plate)
        delivery_condition.valid_flag, delivery_condition.message = self.verify_value(delivery_condition.value)
        return delivery_condition.valid_flag


@dataclass
class YieldStrengthLimit(Limit):
    minimum: int
    limit_type: LimitType = LimitType.MINIMUM
    unit: str = 'MPa'

    def verify_value(self, value: int) -> Tuple[bool, str]:
        if value >= self.minimum:
            message = f"[PASS] Yield Strength value is {value}, meets the minimum limit {self.minimum} {self.unit}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Yield Strength value is {value}, violates the minimum limit {self.minimum} {self.unit}."
            print(message)
            return False, message

    def get_element(self, plate: SteelPlate) -> YieldStrength:
        if plate.yield_strength:
            return plate.yield_strength
        else:
            raise ValueError(
                f"Could not find value of Yield Strength in the {CommonUtils.ordinal(plate.serial_number.value)} steel "
                f"plate."
            )

    def verify(self, plate: SteelPlate) -> bool:
        yield_strength = self.get_element(plate)
        yield_strength.valid_flag, yield_strength.message = self.verify_value(yield_strength.value)
        return yield_strength.valid_flag


@dataclass
class TensileStrengthLimit(Limit):
    minimum: int
    maximum: int
    limit_type: LimitType = LimitType.RANGE
    unit: str = 'MPa'

    def verify_value(self, value: int) -> Tuple[bool, str]:
        if self.minimum <= value <= self.maximum:
            message = (
                f"[PASS] Tensile Strength value is {value}, meets the valid range {self.minimum} - {self.maximum} "
                f"{self.unit}."
            )
            print(message)
            return True, message
        else:
            message = (
                f"[FAIL] Tensile Strength value is {value}, violates the valid range {self.minimum} - {self.maximum} "
                f"{self.unit}."
            )
            print(message)
            return False, message

    def get_element(self, plate: SteelPlate) -> TensileStrength:
        if plate.tensile_strength:
            return plate.tensile_strength
        else:
            raise ValueError(
                f"Could not find value of Tensile Strength in the {CommonUtils.ordinal(plate.serial_number.value)} "
                f"steel plate."
            )

    def verify(self, plate: SteelPlate) -> bool:
        tensile_strength = self.get_element(plate)
        tensile_strength.valid_flag, tensile_strength.message = self.verify_value(tensile_strength.value)
        return tensile_strength.valid_flag


@dataclass
class ElongationLimit(Limit):
    minimum: int
    limit_type: LimitType = LimitType.MINIMUM
    unit: str = '%'

    def verify_value(self, value: int) -> Tuple[bool, str]:
        if value >= self.minimum:
            message = f"[PASS] Elongation value is {value}, meets the minimum limit {self.minimum} {self.unit}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Elongation value is {value}, violates the minimum limit {self.minimum} {self.unit}."
            print(message)
            return False, message

    def get_element(self, plate: SteelPlate) -> Elongation:
        if plate.elongation:
            return plate.elongation
        else:
            raise ValueError(
                f"Could not find value of Elongation in the {CommonUtils.ordinal(plate.serial_number.value)} "
                f"steel plate."
            )

    def verify(self, plate: SteelPlate) -> bool:
        elongation = self.get_element(plate)
        elongation.valid_flag, elongation.message = self.verify_value(elongation.value)
        return elongation.valid_flag


# @dataclass
# class TemperatureLimit(Limit):
#     unique_value: int
#     limit_type: LimitType = LimitType.UNIQUE
#     unit: str = 'Degrees Celsius'
#
#     def verify_value(self, value: int) -> Tuple[bool, str]:
#         if value == self.unique_value:
#             message = f"[PASS] Temperature value is {value}, meets the valid value {self.unique_value} {self.unit}."
#             print(message)
#             return True, message
#         else:
#             message = (
#               f"[FAIL] Temperature value is {value}, violates the valid value {self.unique_value} {self.unit}."
#             )
#             print(message)
#             return False, message
#
#     def get_element(self, plate: SteelPlate) -> Temperature:
#         if plate.temperature:
#             return plate.temperature
#         else:
#             raise ValueError(
#                 f"Could not find value of Temperature in the {CommonUtils.ordinal(plate.serial_number.value)} "
#                 f"steel plate."
#             )
#
#     def verify(self, plate: SteelPlate) -> bool:
#         temperature = self.get_element(plate)
#         temperature.valid_flag, temperature.message = self.verify_value(temperature.value)
#         return temperature.valid_flag

@dataclass
class TemperatureLimit(Limit):
    maximum: int
    limit_type: LimitType = LimitType.MAXIMUM
    unit: str = 'Degrees Celsius'

    def verify_value(self, value: int) -> Tuple[bool, str]:
        if value <= self.maximum:
            message = f"[PASS] Temperature value is {value}, meets the maximum value {self.maximum} {self.unit}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Temperature value is {value}, violates the maximum value {self.maximum} {self.unit}."
            print(message)
            return False, message

    def get_element(self, plate: SteelPlate) -> Temperature:
        if plate.temperature:
            return plate.temperature
        else:
            raise ValueError(
                f"Could not find value of Temperature in the {CommonUtils.ordinal(plate.serial_number.value)} "
                f"steel plate."
            )

    def verify(self, plate: SteelPlate) -> bool:
        temperature = self.get_element(plate)
        temperature.valid_flag, temperature.message = self.verify_value(temperature.value)
        return temperature.valid_flag


@dataclass
class ImpactEnergyLimit(Limit):
    minimum: int
    limit_type: LimitType = LimitType.MINIMUM
    unit: str = 'J'

    def verify_value(self, value: int) -> Tuple[bool, str]:
        if value >= self.minimum:
            message = (
                f"[PASS] Impact Energy value is {value}, meets the "
                f"minimum limit {self.minimum} {self.unit}."
            )
            print(message)
            return True, message
        else:
            message = (
                f"[FAIL] Impact Energy value is {value}, meets the "
                f"minimum limit {self.minimum} {self.unit}."
            )
            print(message)
            return False, message

    def get_element(self, plate: SteelPlate) -> List[ImpactEnergy]:
        if plate.impact_energy_list and len(plate.impact_energy_list) == 4:
            return plate.impact_energy_list
        else:
            raise ValueError(
                f"It is expected to have 4 values of impact energy, so far there is {len(plate.impact_energy_list)}."
            )

    def verify(self, plate: SteelPlate) -> bool:
        impact_energy_list = self.get_element(plate)
        for impact_energy in impact_energy_list:
            impact_energy.valid_flag, impact_energy.message = self.verify_value(impact_energy.value)
        return all([energy.valid_flag for energy in impact_energy_list])


class RuleMaker(metaclass=SingletonABCMeta):

    @staticmethod
    @abstractmethod
    def get_rules(plate: SteelPlate) -> List[Limit]:
        pass

    @staticmethod
    @abstractmethod
    def get_fine_grain_elements_rules(plate: SteelPlate) -> List[Limit]:
        pass

    @staticmethod
    # def get_rules(certificate: Certificate, steel_plate_index: int) -> List[Limit]:
    def get_standard_rules(plate: SteelPlate) -> List[Limit]:

        limit_list: List[Limit] = []

        # delivery_condition = plate.delivery_condition
        # thickness = plate.thickness
        # impact_test_direction = 'None' \
        #     if certificate.steel_plates[steel_plate_index].position_direction_impact is None \
        #     else CommonUtils.translate_to_vl_direction(
        #         certificate.steel_plates[steel_plate_index].position_direction_impact.value)
        # impact_test_direction = plate.position_direction_impact.value

        # Chemical Composition
        #   - Normal Strength Steel
        if plate.specification.value == 'VL A':
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C', limit_type=LimitType.MAXIMUM, maximum=0.21))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Si', limit_type=LimitType.MAXIMUM, maximum=0.50))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mn', limit_type=LimitType.MINIMUM, minimum=2.5 * 0.21))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='P', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='S', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cu', limit_type=LimitType.MAXIMUM, maximum=0.35))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cr', limit_type=LimitType.MAXIMUM, maximum=0.20))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Ni', limit_type=LimitType.MAXIMUM, maximum=0.40))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mo', limit_type=LimitType.MAXIMUM, maximum=0.08))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C + 1/6 Mn', limit_type=LimitType.MAXIMUM, maximum=0.40))
        elif plate.specification.value == 'VL B':
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C', limit_type=LimitType.MAXIMUM, maximum=0.21))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Si', limit_type=LimitType.MAXIMUM, maximum=0.35))
            # Mn: Table 5 Foot Note 6 - minimum 0.60% when the steel is impact tested
            if len(plate.impact_energy_list) > 0:
                limit_list.append(
                    ChemicalCompositionLimit(chemical_element='Mn', limit_type=LimitType.MINIMUM, minimum=0.60))
            else:
                limit_list.append(
                    ChemicalCompositionLimit(chemical_element='Mn', limit_type=LimitType.MINIMUM, minimum=0.80))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='P', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='S', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cu', limit_type=LimitType.MAXIMUM, maximum=0.35))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cr', limit_type=LimitType.MAXIMUM, maximum=0.20))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Ni', limit_type=LimitType.MAXIMUM, maximum=0.40))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mo', limit_type=LimitType.MAXIMUM, maximum=0.08))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C + 1/6 Mn', limit_type=LimitType.MAXIMUM, maximum=0.40))
        elif plate.specification.value == 'VL D':
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C', limit_type=LimitType.MAXIMUM, maximum=0.21))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Si', limit_type=LimitType.RANGE, maximum=0.35, minimum=0.10))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mn', limit_type=LimitType.MINIMUM, minimum=0.60))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='P', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='S', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cu', limit_type=LimitType.MAXIMUM, maximum=0.35))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cr', limit_type=LimitType.MAXIMUM, maximum=0.20))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Ni', limit_type=LimitType.MAXIMUM, maximum=0.40))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mo', limit_type=LimitType.MAXIMUM, maximum=0.08))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C + 1/6 Mn', limit_type=LimitType.MAXIMUM, maximum=0.40))
        elif plate.specification.value == 'VL E':
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C', limit_type=LimitType.MAXIMUM, maximum=0.18))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Si', limit_type=LimitType.RANGE, maximum=0.35, minimum=0.10))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mn', limit_type=LimitType.MINIMUM, minimum=0.70))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='P', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='S', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cu', limit_type=LimitType.MAXIMUM, maximum=0.35))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cr', limit_type=LimitType.MAXIMUM, maximum=0.20))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Ni', limit_type=LimitType.MAXIMUM, maximum=0.40))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mo', limit_type=LimitType.MAXIMUM, maximum=0.08))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C + 1/6 Mn', limit_type=LimitType.MAXIMUM, maximum=0.40))
        #   - High Strength Steel
        elif plate.specification.value in ('VL A27S', 'VL D27S', 'VL E27S'):
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C', limit_type=LimitType.MAXIMUM, maximum=0.18))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Si', limit_type=LimitType.MAXIMUM, maximum=0.50))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mn', limit_type=LimitType.RANGE, maximum=1.60, minimum=0.70))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='P', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='S', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cu', limit_type=LimitType.MAXIMUM, maximum=0.35))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cr', limit_type=LimitType.MAXIMUM, maximum=0.20))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Ni', limit_type=LimitType.MAXIMUM, maximum=0.40))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mo', limit_type=LimitType.MAXIMUM, maximum=0.08))
        elif plate.specification.value in (
                'VL A32',
                'VL D32',
                'VL E32',
                'VL A36',
                'VL D36',
                'VL E36',
                'VL A40',
                'VL D40',
                'VL E40'
        ):
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C', limit_type=LimitType.MAXIMUM, maximum=0.18))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Si', limit_type=LimitType.MAXIMUM, maximum=0.50))
            # Mn: Table 9 Chemical composition limits for high strength steel Foot Note 2
            # minimum 0.70% for thickness up to and including 12.5 mm
            if plate.thickness.value <= 12.5:
                limit_list.append(
                    ChemicalCompositionLimit(chemical_element='Mn', limit_type=LimitType.RANGE, maximum=1.60,
                                             minimum=0.70))
            else:
                limit_list.append(
                    ChemicalCompositionLimit(chemical_element='Mn', limit_type=LimitType.RANGE, maximum=1.60,
                                             minimum=0.90))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='P', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='S', limit_type=LimitType.MAXIMUM, maximum=0.035))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cu', limit_type=LimitType.MAXIMUM, maximum=0.35))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cr', limit_type=LimitType.MAXIMUM, maximum=0.20))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Ni', limit_type=LimitType.MAXIMUM, maximum=0.40))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mo', limit_type=LimitType.MAXIMUM, maximum=0.08))
        elif plate.specification.value in ('VL F27S', 'VL F32', 'VL F36', 'VL F40'):
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C', limit_type=LimitType.MAXIMUM, maximum=0.16))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Si', limit_type=LimitType.MAXIMUM, maximum=0.50))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mn', limit_type=LimitType.RANGE, maximum=1.60, minimum=0.90))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='P', limit_type=LimitType.MAXIMUM, maximum=0.025))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='S', limit_type=LimitType.MAXIMUM, maximum=0.025))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cu', limit_type=LimitType.MAXIMUM, maximum=0.35))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Cr', limit_type=LimitType.MAXIMUM, maximum=0.20))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Ni', limit_type=LimitType.MAXIMUM, maximum=0.80))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Mo', limit_type=LimitType.MAXIMUM, maximum=0.08))
        # High Strength Steel - Table 10 Maximum carbon equivalent values (Ceq) for high strength steel supplied in TM
        # condition.
        if plate.delivery_condition.value == 'TM':
            if plate.specification.value in ('VL A27S', 'VL D27S', 'VL E27S', 'VL F27S'):
                if plate.thickness.value <= 50:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.34))
                elif 50 < plate.thickness.value <= 100:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.36))
                elif 100 < plate.thickness.value <= 150:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.38))
            elif plate.specification.value in ('VL A32', 'VL D32', 'VL E32', 'VL F32'):
                if plate.thickness.value <= 50:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.36))
                elif 50 < plate.thickness.value <= 100:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.38))
                elif 100 < plate.thickness.value <= 150:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.40))
            elif plate.specification.value in ('VL A36', 'VL D36', 'VL E36', 'VL F36'):
                if plate.thickness.value <= 50:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.38))
                elif 50 < plate.thickness.value <= 100:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.40))
                elif 100 < plate.thickness.value <= 150:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.42))
            elif plate.specification.value in ('VL A40', 'VL D40', 'VL E40', 'VL F40'):
                if plate.thickness.value <= 50:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.40))
                elif 50 < plate.thickness.value <= 100:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.42))
                elif 100 < plate.thickness.value <= 150:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.45))
        # Mechanical Properties
        #   - Normal Strength Steel
        if plate.specification.value == 'VL A':
            limit_list.append(YieldStrengthLimit(minimum=235))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=520))
            limit_list.append(ElongationLimit(minimum=22))
            if plate.thickness.value <= 50:
                pass
            elif 50 < plate.thickness.value <= 70:
                if plate.delivery_condition.value == 'N':
                    pass
                else:
                    limit_list.append(TemperatureLimit(maximum=20))
                    limit_list.append(PositionDirectionImpactLimit())
                    if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                        limit_list.append(ImpactEnergyLimit(minimum=34))
                    elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                        limit_list.append(ImpactEnergyLimit(minimum=24))
            elif 70 < plate.thickness.value <= 150:
                if plate.delivery_condition.value == 'N':
                    pass
                else:
                    limit_list.append(TemperatureLimit(maximum=20))
                    limit_list.append(PositionDirectionImpactLimit())
                    if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                        limit_list.append(ImpactEnergyLimit(minimum=41))
                    elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                        limit_list.append(ImpactEnergyLimit(minimum=27))
        elif plate.specification.value == 'VL B':
            limit_list.append(YieldStrengthLimit(minimum=235))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=520))
            limit_list.append(ElongationLimit(minimum=22))
            if plate.thickness.value <= 25:
                pass
            elif 25 < plate.thickness.value <= 50:
                limit_list.append(TemperatureLimit(maximum=0))
                limit_list.append(PositionDirectionImpactLimit())
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=27))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=20))
            elif 50 < plate.thickness.value <= 70:
                limit_list.append(TemperatureLimit(maximum=0))
                limit_list.append(PositionDirectionImpactLimit())
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24))
            elif 70 < plate.thickness.value <= 150:
                limit_list.append(TemperatureLimit(maximum=0))
                limit_list.append(PositionDirectionImpactLimit())
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27))
        elif plate.specification.value == 'VL D':
            limit_list.append(YieldStrengthLimit(minimum=235))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=520))
            limit_list.append(ElongationLimit(minimum=22))
            limit_list.append(TemperatureLimit(maximum=-20))
            limit_list.append(PositionDirectionImpactLimit())
            if plate.thickness.value <= 50:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=27))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=20))
            elif 50 < plate.thickness.value <= 70:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24))
            elif 70 < plate.thickness.value <= 150:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27))
        elif plate.specification.value == 'VL E':
            limit_list.append(YieldStrengthLimit(minimum=235))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=520))
            limit_list.append(ElongationLimit(minimum=22))
            limit_list.append(TemperatureLimit(maximum=-40))
            limit_list.append(PositionDirectionImpactLimit())
            if plate.thickness.value <= 50:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=27))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=20))
            elif 50 < plate.thickness.value <= 70:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24))
            elif 70 < plate.thickness.value <= 150:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27))
        elif plate.specification.value in ('VL A27S', 'VL D27S', 'VL E27S', 'VL F27S'):
            limit_list.append(YieldStrengthLimit(minimum=265))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=530))
            limit_list.append(ElongationLimit(minimum=22))
            limit_list.append(PositionDirectionImpactLimit())
            if plate.thickness.value <= 50:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=27))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=20))
            elif 50 < plate.thickness.value <= 70:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24))
            elif 70 < plate.thickness.value <= 150:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27))
        elif plate.specification.value in ('VL A32', 'VL D32', 'VL E32', 'VL F32'):
            limit_list.append(YieldStrengthLimit(minimum=315))
            limit_list.append(TensileStrengthLimit(minimum=440, maximum=570))
            limit_list.append(ElongationLimit(minimum=22))
            limit_list.append(PositionDirectionImpactLimit())
            if plate.thickness.value <= 50:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=31))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=22))
            elif 50 < plate.thickness.value <= 70:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=38))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=26))
            elif 70 < plate.thickness.value <= 150:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=46))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=31))
        elif plate.specification.value in ('VL A36', 'VL D36', 'VL E36', 'VL F36'):
            limit_list.append(YieldStrengthLimit(minimum=355))
            limit_list.append(TensileStrengthLimit(minimum=490, maximum=630))
            limit_list.append(ElongationLimit(minimum=21))
            limit_list.append(PositionDirectionImpactLimit())
            if plate.thickness.value <= 50:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24))
            elif 50 < plate.thickness.value <= 70:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27))
            elif 70 < plate.thickness.value <= 150:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=50))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=34))
        elif plate.specification.value in ('VL A40', 'VL D40', 'VL E40', 'VL F40'):
            limit_list.append(YieldStrengthLimit(minimum=390))
            limit_list.append(TensileStrengthLimit(minimum=510, maximum=660))
            limit_list.append(ElongationLimit(minimum=20))
            limit_list.append(PositionDirectionImpactLimit())
            if plate.thickness.value <= 50:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=39))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=26))
            elif 50 < plate.thickness.value <= 70:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=46))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=31))
            elif 70 < plate.thickness.value <= 150:
                if plate.position_direction_impact.value == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=55))
                elif plate.position_direction_impact.value == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=37))
        # Mechanical Properties - High Strength Steel - Impact Test Temperature
        if plate.specification.value in ('VL A27S', 'VL A32', 'VL A36', 'VL A40'):
            limit_list.append(TemperatureLimit(maximum=0))
        elif plate.specification.value in ('VL D27S', 'VL D32', 'VL D36', 'VL D40'):
            limit_list.append(TemperatureLimit(maximum=-20))
        elif plate.specification.value in ('VL E27S', 'VL E32', 'VL E36', 'VL E40'):
            limit_list.append(TemperatureLimit(maximum=-40))
        elif plate.specification.value in ('VL F27S', 'VL F32', 'VL F36', 'VL F40'):
            limit_list.append(TemperatureLimit(maximum=-60))

        return limit_list


class LongTengRuleMaker(RuleMaker):

    @staticmethod
    def get_rules(plate: SteelPlate) -> List[Limit]:
        standard_rules = LongTengRuleMaker.get_standard_rules(plate)
        special_rules = LongTengRuleMaker.get_special_rules(plate)
        fine_grain_elements_rules = LongTengRuleMaker.get_fine_grain_elements_rules(plate)
        return special_rules + standard_rules + fine_grain_elements_rules

    @staticmethod
    def get_special_rules(plate: SteelPlate) -> List[Limit]:

        # Specification & Delivery Condition
        limit_list: List[Limit] = [
            SpecificationLimit(
                scope=['VL A', 'VL B', 'VL D', 'VL A32', 'VL A36', 'VL D32', 'VL D36']
            ),
            DeliveryConditionLimit(
                scope=['AR']
            )
        ]
        # Thickness
        if plate.specification.value in ['VL A', 'VL B']:
            if plate.steel_making_type:
                if plate.steel_making_type.value == 'BOC, CC':
                    limit_list.append(ThicknessLimit(maximum=15))
                elif plate.steel_making_type.value == 'EAF, CC':
                    limit_list.append(ThicknessLimit(maximum=20))
                elif plate.steel_making_type.value is None:
                    limit_list.append(ThicknessLimit(maximum=20))
                else:
                    raise ValueError(
                        f"The steel making type value {plate.steel_making_type.value} is not expected."
                    )
            else:
                raise ValueError(
                    f"The steel making type is not instantiated in the steel plate."
                )
        elif plate.specification.value == 'VL D':
            if plate.steel_making_type:
                if plate.steel_making_type.value == 'BOC, CC':
                    limit_list.append(ThicknessLimit(maximum=19))
                elif plate.steel_making_type.value == 'EAF, CC':
                    limit_list.append(ThicknessLimit(maximum=15))
                elif plate.steel_making_type.value is None:
                    limit_list.append(ThicknessLimit(maximum=19))
                else:
                    raise ValueError(
                        f"The steel making type value {plate.steel_making_type.value} is not expected."
                    )
            else:
                raise ValueError(
                    f"The steel making type is not instantiated in the steel plate."
                )
        elif plate.specification.value in ['VL A32', 'VL A36']:
            if plate.steel_making_type:
                if plate.steel_making_type.value == 'BOC, CC':
                    limit_list.append(ThicknessLimit(maximum=17))
                elif plate.steel_making_type.value == 'EAF, CC':
                    limit_list.append(ThicknessLimit(maximum=20))
                elif plate.steel_making_type.value is None:
                    limit_list.append(ThicknessLimit(maximum=20))
                else:
                    raise ValueError(
                        f"The steel making type value {plate.steel_making_type.value} is not expected."
                    )
            else:
                raise ValueError(
                    f"The steel making type is not instantiated in the steel plate."
                )
        elif plate.specification.value in ['VL D32', 'VL D36']:
            if plate.steel_making_type:
                if plate.steel_making_type.value == 'BOC, CC':
                    limit_list.append(ThicknessLimit(maximum=17))
                elif plate.steel_making_type.value == 'EAF, CC':
                    limit_list.append(ThicknessLimit(maximum=19))
                elif plate.steel_making_type.value is None:
                    limit_list.append(ThicknessLimit(maximum=19))
                else:
                    raise ValueError(
                        f"The steel making type value {plate.steel_making_type.value} is not expected."
                    )
            else:
                raise ValueError(
                    f"The steel making type is not instantiated in the steel plate."
                )
        return limit_list

    @staticmethod
    def get_fine_grain_elements_rules(plate: SteelPlate) -> List[FineGrainElementLimitCombination]:
        if plate.specification.value in ['VL A', 'VL B']:
            if plate.steel_making_type:
                if plate.steel_making_type.value == 'BOC, CC':
                    return [LongTengRuleMaker.compose_fine_grain_element_limit_combination(keys=['Al'])]
                elif plate.steel_making_type.value == 'EAF, CC':
                    return []
                else:
                    raise ValueError(
                        f"The steel making type value {plate.steel_making_type.value} is not expected."
                    )
            else:
                raise ValueError(
                    f"The steel making type is not instantiated in the steel plate."
                )
        elif plate.specification.value == 'VL D':
            if plate.steel_making_type:
                if plate.steel_making_type.value in ['BOC, CC', 'EAF, CC']:
                    return [LongTengRuleMaker.compose_fine_grain_element_limit_combination(keys=['Al'])]
                else:
                    raise ValueError(
                        f"The steel making type value {plate.steel_making_type.value} is not expected."
                    )
            else:
                raise ValueError(
                    f"The steel making type is not instantiated in the steel plate."
                )
        elif plate.specification.value in ['VL A32', 'VL A36']:
            if plate.steel_making_type:
                if plate.steel_making_type.value == 'BOC, CC':
                    keys = []
                    if plate.thickness.value <= 17:
                        keys.append('Al')
                    if plate.thickness.value <= 15:
                        keys.append('Al+Nb')
                        keys.append('Al+V')
                    return [LongTengRuleMaker.compose_fine_grain_element_limit_combination(keys)]
                elif plate.steel_making_type.value == 'EAF, CC':
                    return [LongTengRuleMaker.compose_fine_grain_element_limit_combination(['Al', 'Nb', 'Al+Nb'])]
                else:
                    raise ValueError(
                        f"The steel making type value {plate.steel_making_type.value} is not expected."
                    )
            else:
                raise ValueError(
                    f"The steel making type is not instantiated in the steel plate."
                )
        elif plate.specification.value in ['VL D32', 'VL D36']:
            if plate.steel_making_type:
                if plate.steel_making_type.value == 'BOC, CC':
                    keys = []
                    if plate.thickness.value <= 17:
                        keys.append('Al')
                    if plate.thickness.value <= 15:
                        keys.append('Al+Nb')
                        keys.append('Al+V')
                    return [LongTengRuleMaker.compose_fine_grain_element_limit_combination(keys)]
                elif plate.steel_making_type.value == 'EAF, CC':
                    return [LongTengRuleMaker.compose_fine_grain_element_limit_combination(['Al+Nb', 'Al+V'])]
                else:
                    raise ValueError(
                        f"The steel making type value {plate.steel_making_type.value} is not expected."
                    )
            else:
                raise ValueError(
                    "The steel making type is not instantiated in the steel plate."
                )

    @staticmethod
    def compose_fine_grain_element_limit_combination(keys: List[str]) -> FineGrainElementLimitCombination:
        concurrent_limits: List[FineGrainElementLimit] = []
        error_message: str = '[FAIL] Fine Grain Element failed test: '

        for key in keys:
            if key == 'Al':
                concurrent_limits.append(
                    FineGrainElementLimit(
                        concurrent_limits=[
                            ChemicalCompositionLimit(
                                chemical_element='Al',
                                limit_type=LimitType.MINIMUM,
                                minimum=0.020
                            )
                        ]
                    )
                )
                error_message += '[Al] Al expect minimum 0.020% '
            elif key == 'Nb':
                concurrent_limits.append(
                    FineGrainElementLimit(
                        concurrent_limits=[
                            ChemicalCompositionLimit(
                                chemical_element='Nb',
                                limit_type=LimitType.RANGE,
                                maximum=0.050,
                                minimum=0.020
                            )
                        ]
                    )
                )
                error_message += '[Nb] Nb expect range [0.020%, 0.050%] '
            elif key == 'Al+Nb':
                concurrent_limits.append(
                    FineGrainElementLimit(
                        concurrent_limits=[
                            ChemicalCompositionLimit(
                                chemical_element='Al',
                                limit_type=LimitType.MINIMUM,
                                minimum=0.015
                            ),
                            ChemicalCompositionLimit(
                                chemical_element='Nb',
                                limit_type=LimitType.MINIMUM,
                                minimum=0.010
                            ),
                            ChemicalCompositionLimit(
                                chemical_element='Nb + V + Ti',
                                limit_type=LimitType.MAXIMUM,
                                maximum=0.12
                            )
                        ]
                    )
                )
                error_message += \
                    '[Al+Nb] Al expect minimum 0.015, Nb expect minimum 0.010, Nb + V + Ti expect maximum 0.12 '
            elif key == 'Al+V':
                concurrent_limits.append(
                    FineGrainElementLimit(
                        concurrent_limits=[
                            ChemicalCompositionLimit(
                                chemical_element='Al',
                                limit_type=LimitType.MINIMUM,
                                minimum=0.015
                            ),
                            ChemicalCompositionLimit(
                                chemical_element='V',
                                limit_type=LimitType.MINIMUM,
                                minimum=0.030
                            ),
                            ChemicalCompositionLimit(
                                chemical_element='Nb + V + Ti',
                                limit_type=LimitType.MAXIMUM,
                                maximum=0.12
                            )
                        ]
                    )
                )
                error_message += \
                    '[Al+V] Al expect minimum 0.015, V expect minimum 0.030, Nb + V + Ti expect maximum 0.12 '
            else:
                raise ValueError(
                    f"key value {key} is not expected."
                )
        return FineGrainElementLimitCombination(
            fine_grain_element_limits=concurrent_limits,
            error_message=error_message
        )


class BaoSteelRuleMaker(RuleMaker):

    @staticmethod
    def get_rules(plate: SteelPlate) -> List[Limit]:
        return BaoSteelRuleMaker.get_special_rules() + BaoSteelRuleMaker.get_standard_rules(
            plate) + BaoSteelRuleMaker.get_fine_grain_elements_rules(plate)

    @staticmethod
    def get_special_rules() -> List[Limit]:
        specification_limit = SpecificationLimit(
            scope=[
                'VL A', 'VL B', 'VL D', 'VL E',
                'VL A27S', 'VL D27S', 'VL E27S', 'VL F27S',
                'VL A32', 'VL D32', 'VL E32', 'VL F32',
                'VL A36', 'VL D36', 'VL E36', 'VL F36',
                'VL A40', 'VL D40', 'VL E40', 'VL F40'
            ]
        )
        return [specification_limit]

    @staticmethod
    def get_fine_grain_elements_rules(plate: SteelPlate) -> List[Limit]:
        limit_list = []
        if plate.specification.value == 'VL A':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['N', 'AR', 'TM']
                )
            )
            if plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                key_list = []
                if plate.thickness.value <= 80 and 'Z35' not in plate.specification.value:
                    key_list.append('Al')
                if plate.thickness.value <= 35:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 80:
                    key_list.append('Al+Nb')
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', key_list)
                    )
            elif plate.delivery_condition.value == 'AR':
                if 'Z35' not in plate.specification.value:
                    limit_list.append(
                        ThicknessLimit(
                            maximum=50
                        )
                    )
                    if plate.thickness.value <= 50:
                        limit_list.append(
                            BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', ['Al+Ti'])
                        )
                else:
                    limit_list.append(
                        ThicknessLimit(
                            maximum=35
                        )
                    )
                    if plate.thickness.value <= 35:
                        limit_list.append(
                            BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', ['Al+Ti'])
                        )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=100
                    )
                )
                if plate.thickness.value <= 100:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL B':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['N', 'AR', 'TM']
                )
            )
            if plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                key_list = []
                if plate.thickness.value <= 80 and 'Z35' not in plate.specification.value:
                    key_list.append('Al')
                if plate.thickness.value <= 35:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 80:
                    key_list.append('Al+Nb')
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', key_list)
                    )
            elif plate.delivery_condition.value == 'AR':
                if 'Z35' not in plate.specification.value:
                    limit_list.append(
                        ThicknessLimit(
                            maximum=50
                        )
                    )
                    if plate.thickness.value <= 50:
                        limit_list.append(
                            BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', ['Al+Ti'])
                        )
                else:
                    limit_list.append(
                        ThicknessLimit(
                            maximum=35
                        )
                    )
                    if plate.thickness.value <= 35:
                        limit_list.append(
                            BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', ['Al+Ti'])
                        )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=100
                    )
                )
                if plate.thickness.value <= 100:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL D':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['AR', 'N', 'TM']
                )
            )
            if plate.delivery_condition.value == 'AR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=35
                    )
                )
                if plate.thickness.value <= 35:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', ['Al+Ti'])
                    )
            elif plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                key_list = []
                if plate.thickness.value <= 35:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 80:
                    key_list.append('Al+Nb')
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', key_list)
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=100
                    )
                )
                if plate.thickness.value <= 100:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL E':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['N', 'TM']
                )
            )
            if plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                key_list = []
                if plate.thickness.value <= 35:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 80:
                    key_list.append('Al+Nb')
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', key_list)
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=100
                    )
                )
                if plate.thickness.value <= 100:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('normal', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL A27S':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['AR', 'N', 'NR', 'TM']
                )
            )
            if plate.delivery_condition.value == 'AR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=20
                    )
                )
                if plate.thickness.value <= 20:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Ti'])
                    )
            elif plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                key_list = []
                if plate.thickness.value <= 30:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 80:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
            elif plate.delivery_condition.value == 'NR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=40
                    )
                )
                key_list = []
                if plate.thickness.value <= 30:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 40:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                if plate.thickness.value <= 90:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL A32':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['AR', 'N', 'NR', 'TM']
                )
            )
            if plate.delivery_condition.value == 'AR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=20
                    )
                )
                if plate.thickness.value <= 20:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Ti'])
                    )
            elif plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                key_list = []
                if plate.thickness.value <= 30:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 80:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
            elif plate.delivery_condition.value == 'NR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=40
                    )
                )
                key_list = []
                if plate.thickness.value <= 30:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 40:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                key_list = []
                if plate.thickness.value <= 50:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 90:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
        elif plate.specification.value == 'VL A36':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['AR', 'NR', 'N', 'TM']
                )
            )
            if plate.delivery_condition.value == 'AR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=20
                    )
                )
                if plate.thickness.value <= 20:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Ti'])
                    )
            elif plate.delivery_condition.value == 'NR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=40
                    )
                )
                key_list = []
                if plate.thickness.value <= 30:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 40:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
            elif plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                if plate.thickness.value <= 80:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                key_list = []
                if plate.thickness.value <= 50:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 90:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
        elif plate.specification.value == 'VL A40':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['TM']
                )
            )
            if plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                if plate.thickness.value <= 90:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL D27S':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['AR', 'N', 'NR', 'TM']
                )
            )
            if plate.delivery_condition.value == 'AR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=20
                    )
                )
                if plate.thickness.value <= 20:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Ti'])
                    )
            elif plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                key_list = []
                if plate.thickness.value <= 30:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 80:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
            elif plate.delivery_condition.value == 'NR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=40
                    )
                )
                if plate.thickness.value <= 40:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                if plate.thickness.value <= 90:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL D32':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['AR', 'N', 'NR', 'TM']
                )
            )
            if plate.delivery_condition.value == 'AR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=20
                    )
                )
                if plate.thickness.value <= 20:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Ti'])
                    )
            elif plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                key_list= []
                if plate.thickness.value <= 30:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 80:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
            elif plate.delivery_condition.value == 'NR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=40
                    )
                )
                if plate.thickness.value <= 40:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                key_list = []
                if plate.thickness.value <= 50:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 90:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
        elif plate.specification.value == 'VL D36':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['AR', 'N', 'NR', 'TM']
                )
            )
            if plate.delivery_condition.value == 'AR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=20
                    )
                )
                if plate.thickness.value <= 20:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Ti'])
                    )
            elif plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                if plate.thickness.value <= 80:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
            elif plate.delivery_condition.value == 'NR':
                limit_list.append(
                    ThicknessLimit(
                        maximum=40
                    )
                )
                if plate.thickness.value <= 40:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                key_list = []
                if plate.thickness.value <= 50:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 90:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
        elif plate.specification.value == 'VL D40':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['TM']
                )
            )
            if plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                if plate.thickness.value <= 90:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL E27S':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['N', 'TM']
                )
            )
            if plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                if plate.thickness.value <= 80:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                if plate.thickness.value <= 90:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL E32':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['N', 'TM']
                )
            )
            if plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                if plate.thickness.value <= 80:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                key_list = []
                if plate.thickness.value <= 50:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 90:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
        elif plate.specification.value == 'VL E36':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['N', 'TM']
                )
            )
            if plate.delivery_condition.value == 'N':
                limit_list.append(
                    ThicknessLimit(
                        maximum=80
                    )
                )
                if plate.thickness.value <= 80:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
            elif plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                key_list = []
                if plate.thickness.value <= 50:
                    key_list.append('Al+Ti')
                if plate.thickness.value <= 90:
                    key_list.append('Al+Nb+Ti')
                if len(key_list) > 0:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', key_list)
                    )
        elif plate.specification.value == 'VL E40':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['TM']
                )
            )
            if plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=90
                    )
                )
                if plate.thickness.value <= 90:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL F27S':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['TM']
                )
            )
            if plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=68
                    )
                )
                if plate.thickness.value <= 68:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti']))
        elif plate.specification.value == 'VL F32':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['TM']
                )
            )
            if plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=68
                    )
                )
                if plate.thickness.value <= 68:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL F36':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['TM']
                )
            )
            if plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=68
                    )
                )
                if plate.thickness.value <= 68:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
        elif plate.specification.value == 'VL F40':
            limit_list.append(
                DeliveryConditionLimit(
                    scope=['TM']
                )
            )
            if plate.delivery_condition.value == 'TM':
                limit_list.append(
                    ThicknessLimit(
                        maximum=68
                    )
                )
                if plate.thickness.value <= 68:
                    limit_list.append(
                        BaoSteelRuleMaker.create_fine_grain_element_limit_combination('high', ['Al+Nb+Ti'])
                    )
        return limit_list

    @staticmethod
    def create_fine_grain_element_limit(strength: str, key: str) -> Tuple[FineGrainElementLimit, str]:
        if strength == 'normal':
            if key == 'Al':
                return FineGrainElementLimit(
                    concurrent_limits=[
                        BaoSteelAlLimit(
                            alt_limit=ChemicalCompositionLimit(
                                chemical_element='Alt',
                                limit_type=LimitType.MINIMUM,
                                minimum=0.020
                            ),
                            als_limit=ChemicalCompositionLimit(
                                chemical_element='Als',
                                limit_type=LimitType.MINIMUM,
                                minimum=0.015
                            )
                        )
                    ]
                ), '[Al] Alt expect minimum 0.020 or Als expect minimum 0.015 '
            elif key == 'Al+Ti':
                return FineGrainElementLimit(
                    concurrent_limits=[
                        BaoSteelAlLimit(),
                        ChemicalCompositionLimit(
                            chemical_element='Ti',
                            limit_type=LimitType.MINIMUM,
                            minimum=0.007
                        )
                    ]
                ), '[Al+Ti] Alt expect minimum 0.015 or Als expect minimum 0.010, Ti expect minimum 0.007 '
            elif key == 'Al+Nb':
                return FineGrainElementLimit(
                    concurrent_limits=[
                        BaoSteelAlLimit(),
                        ChemicalCompositionLimit(
                            chemical_element='Nb',
                            limit_type=LimitType.MINIMUM,
                            minimum=0.010
                        )
                    ]
                ), '[Al+Nb] Alt expect minimum 0.015 or Als expect minimum 0.010, Nb expect minimum 0.010 '
            elif key == 'Al+Nb+Ti':
                return FineGrainElementLimit(
                    concurrent_limits=[
                        BaoSteelAlLimit(),
                        ChemicalCompositionLimit(
                            chemical_element='Nb',
                            limit_type=LimitType.MINIMUM,
                            minimum=0.010
                        ),
                        ChemicalCompositionLimit(
                            chemical_element='Ti',
                            limit_type=LimitType.MINIMUM,
                            minimum=0.007
                        )
                    ]
                ), (
                           '[Al+Nb+Ti] Alt expect minimum 0.015 or Als expect minimum 0.010, Nb expect minimum 0.010, '
                           'Ti expect minimum 0.007 '
                       )
            else:
                raise ValueError(
                    f"The key value {key} is not expected. (strength: {strength})"
                )
        elif strength == 'high':
            if key == 'Al+Ti':
                return FineGrainElementLimit(
                    concurrent_limits=[
                        BaoSteelAlLimit(),
                        ChemicalCompositionLimit(
                            chemical_element='Ti',
                            limit_type=LimitType.RANGE,
                            minimum=0.007,
                            maximum=0.02
                        )
                    ]
                ), '[Al+Ti] Alt expect minimum 0.015 or Als expect minimum 0.010, Ti expect range [0.007, 0.02] '
            elif key == 'Al+Nb+Ti':
                return FineGrainElementLimit(
                    concurrent_limits=[
                        BaoSteelAlLimit(),
                        ChemicalCompositionLimit(
                            chemical_element='Nb',
                            limit_type=LimitType.RANGE,
                            minimum=0.010,
                            maximum=0.05
                        ),
                        ChemicalCompositionLimit(
                            chemical_element='Ti',
                            limit_type=LimitType.RANGE,
                            minimum=0.007,
                            maximum=0.02
                        )
                    ]
                ), (
                           '[Al+Nb+Ti] Alt expect minimum 0.015 or Als expect minimum 0.010, '
                           'Nb expect range [0.010, 0.05], Ti expect range [0.007, 0.02] '
                       )
            elif key == 'Al+Nb+Ti+V':
                return FineGrainElementLimit(
                    concurrent_limits=[
                        BaoSteelAlLimit(),
                        ChemicalCompositionLimit(
                            chemical_element='Nb',
                            limit_type=LimitType.RANGE,
                            minimum=0.010,
                            maximum=0.05
                        ),
                        ChemicalCompositionLimit(
                            chemical_element='Ti',
                            limit_type=LimitType.RANGE,
                            minimum=0.007,
                            maximum=0.02
                        ),
                        ChemicalCompositionLimit(
                            chemical_element='V',
                            limit_type=LimitType.RANGE,
                            minimum=0.03,
                            maximum=0.10
                        ),
                        ChemicalCompositionLimit(
                            chemical_element='Nb + V + Ti',
                            limit_type=LimitType.MAXIMUM,
                            maximum=0.12
                        )
                    ]
                ), (
                           '[Al+Nb+Ti+V] Alt expect minimum 0.015 or Als expect minimum 0.010, '
                           'Nb expect range [0.010, 0.05], Ti expect range [0.007, 0.02], V expect range [0.03, 0.10], '
                           'Nb+V+Ti expect maximum 0.12 '
                       )
            else:
                raise ValueError(
                    f"The key value {key} is not expected. (strength: {strength})"
                )
        else:
            raise ValueError(
                f"The strength value {strength} is not expected."
            )

    @staticmethod
    def create_fine_grain_element_limit_combination(strength: str,
                                                    key_list: List[str]) -> FineGrainElementLimitCombination:
        limit_list = []
        error_message = '[FAIL] Fine Grain Element failed test: '
        for key in key_list:
            fine_grain_element_limit, error = BaoSteelRuleMaker.create_fine_grain_element_limit(strength, key)
            limit_list.append(fine_grain_element_limit)
            error_message += error
        return FineGrainElementLimitCombination(
            fine_grain_element_limits=limit_list,
            error_message=error_message
        )

    # def get_fine_grain_elements_rules(self, certificate: Certificate, steel_plate_index: int) -> List[
    #         ChemicalCompositionCombinedLimit]:
    #     limit_list: List[ChemicalCompositionCombinedLimit] = []
    #     plate = certificate.steel_plates[steel_plate_index]
    #     # specification = certificate.specification
    #     # delivery_condition = certificate.steel_plates[steel_plate_index].delivery_condition
    #     # thickness = certificate.thickness
    #
    #     # Normal Strength Steel
    #     if plate.specification.value in ('VL A', 'VL B'):
    #         if plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 35:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlLimit())
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusNbLimit())
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'AR':
    #             if plate.thickness.value <= 50:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #             # TODO When we enable Z35, we need to add a condition that the thickness limit changed to 35.
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 100:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL D':
    #         if plate.delivery_condition.value == 'AR':
    #             if plate.thickness.value <= 35:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 35:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusNbLimit())
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 100:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL E':
    #         if plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 35:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusNbLimit())
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 100:
    #                 limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     # High Strength Steel
    #     elif plate.specification.value == 'VL A27S':
    #         if plate.delivery_condition.value == 'AR':
    #             if plate.thickness.value <= 20:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 30:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'NR':
    #             if plate.thickness.value <= 30:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 40:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL A32':
    #         if plate.delivery_condition.value == 'AR':
    #             if plate.thickness.value <= 20:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 30:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'NR':
    #             if plate.thickness.value <= 30:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 40:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 50:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #     elif plate.specification.value == 'VL A36':
    #         if plate.delivery_condition.value == 'AR':
    #             if plate.thickness.value <= 20:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'NR':
    #             if plate.thickness.value <= 30:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 40:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 50:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL A40':
    #         if plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL D27S':
    #         if plate.delivery_condition.value == 'AR':
    #             if plate.thickness.value <= 20:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 30:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'NR':
    #             if plate.thickness.value <= 40:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL D32':
    #         if plate.delivery_condition.value == 'AR':
    #             if plate.thickness.value <= 20:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 30:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'NR':
    #             if plate.thickness.value <= 40:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 50:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL D36':
    #         if plate.delivery_condition.value == 'AR':
    #             if plate.thickness.value <= 20:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'NR':
    #             if plate.thickness.value <= 40:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 50:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL D40':
    #         if plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL E27S':
    #         if plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL E32':
    #         if plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 50:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL E36':
    #         if plate.delivery_condition.value == 'N':
    #             if plate.thickness.value <= 80:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         elif plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 50:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == 'VL E40':
    #         if plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 90:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     elif plate.specification.value == ('VL F27S', 'VL F32', 'VL F36', 'VL F40'):
    #         if plate.delivery_condition.value == 'TM':
    #             if plate.thickness.value <= 68:
    #                 limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
    #             else:
    #                 BaoSteelRuleMaker.update_thickness(plate.delivery_condition, plate.specification, plate.thickness)
    #         else:
    #             BaoSteelRuleMaker.update_delivery_condition(plate.delivery_condition, plate.specification)
    #     else:
    #         plate.specification.valid_flag = False
    #         plate.specification.message = (
    #             f"The specification value {plate.specification.value} is not expected according to agreed document."
    #         )
    #
    #     return limit_list
    #
    # @staticmethod
    # def update_thickness(delivery_condition: DeliveryCondition, specification: Specification, thickness: Thickness):
    #     thickness.valid_flag = False
    #     thickness.message = (
    #         f"[FAIL] The thickness value {thickness.value} violates the maximum limit of Specification "
    #         f"{specification.value} and Delivery Condition {delivery_condition.value}."
    #     )
    #
    # @staticmethod
    # def update_delivery_condition(delivery_condition: DeliveryCondition, specification: Specification):
    #     delivery_condition.valid_flag = False
    #     delivery_condition.message = (
    #         f"[FAIL] The delivery condition value {delivery_condition.value} is not expected for specification "
    #         f"{specification.value}."
    #     )


# if __name__ == '__main__':
#     yield_strength_limit = YieldStrengthLimit(
#         minimum=10
#     )
#     print(yield_strength_limit.__class__.__name__)
