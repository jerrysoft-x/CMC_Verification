from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, unique
from typing import Tuple, Union, List, Dict

from certificate_element import ChemicalElementValue, CertificateElementToVerify, Specification, DeliveryCondition, \
    Thickness
from common_utils import Limit, Direction, SingletonABCMeta, CommonUtils, Certificate


@unique
class LimitType(Enum):
    MAXIMUM = 1
    MINIMUM = 2
    RANGE = 3
    UNIQUE = 4


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

    def verify(self, value: float) -> Tuple[bool, str]:
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

    def get_element(self, certificate: Certificate, steel_plate_index: int) -> CertificateElementToVerify:
        chemical_compositions = certificate.steel_plates[steel_plate_index].chemical_compositions
        if self.chemical_element in chemical_compositions:
            return chemical_compositions[self.chemical_element]
        else:
            raise ValueError(
                f"Could not find chemical composition value for {self.chemical_element} which is required to be "
                f"checked."
            )


class ChemicalCompositionCombinedLimit(Limit):
    @abstractmethod
    def verify(self, value) -> Tuple[bool, str]:
        pass

    def get_element(self, certificate: Certificate, steel_plate_index: int) -> Dict[str, ChemicalElementValue]:
        return certificate.steel_plates[steel_plate_index].chemical_compositions

    @staticmethod
    def get_element_value(element_name: str,
                          chemical_composition: Dict[str, ChemicalElementValue]) -> ChemicalElementValue:
        if element_name in chemical_composition:
            return chemical_composition[element_name]
        else:
            raise ValueError(
                f"Element {element_name} is required but missing in this certificate."
            )


class CPlusMnLimit(ChemicalCompositionCombinedLimit):
    def verify(self, value) -> Tuple[bool, str]:
        chemical_composition: Dict[str, ChemicalElementValue] = value
        c = self.get_element_value('C', chemical_composition)
        mn = self.get_element_value('Mn', chemical_composition)
        c_mn_combined_value = c.calculated_value + mn.calculated_value / 6
        if c_mn_combined_value <= 0.40:
            message = (
                f"[PASS] The value of C + 1/6 Mn is {c_mn_combined_value}, meets the maximum limit 0.40 % by weight."
            )
            print(message)
            c.valid_flag = c.valid_flag and True
            c.message = c.message + ' ' + message
            mn.valid_flag = mn.valid_flag and True
            mn.message = mn.message + ' ' + message
            return True, message
        else:
            message = (
                f"[FAIL] The value of C + 1/6 Mn is {c_mn_combined_value}, violates the maximum limit 0.40 % by weight."
            )
            print(message)
            c.valid_flag = False
            c.message = c.message + ' ' + message
            mn.valid_flag = False
            mn.message = mn.message + ' ' + message
            return False, message


class NormalStrengthSteelFineGrainAlLimit(ChemicalCompositionCombinedLimit):
    def verify(self, value) -> Tuple[bool, str]:
        chemical_composition: Dict[str, ChemicalElementValue] = value
        alt = self.get_element_value('Alt', chemical_composition)
        als = self.get_element_value('Als', chemical_composition)
        alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
                                                               minimum=0.020).verify(alt.calculated_value)
        als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
                                                               minimum=0.015).verify(als.calculated_value)
        if alt.valid_flag and not als.valid_flag:
            als.valid_flag = True
        elif als.valid_flag and not alt.valid_flag:
            alt.valid_flag = True

        if alt.valid_flag and als.valid_flag:
            return True, ''
        else:
            return False, ''

    def __str__(self):
        return 'Al'


class NormalStrengthSteelFineGrainAlPlusTiLimit(ChemicalCompositionCombinedLimit):
    def verify(self, value) -> Tuple[bool, str]:
        chemical_composition: Dict[str, ChemicalElementValue] = value
        alt = self.get_element_value('Alt', chemical_composition)
        als = self.get_element_value('Als', chemical_composition)
        ti = self.get_element_value('Ti', chemical_composition)
        alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
                                                               minimum=0.015).verify(alt.calculated_value)
        als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
                                                               minimum=0.010).verify(als.calculated_value)
        ti.valid_flag, ti.message = ChemicalCompositionLimit(chemical_element='Ti', limit_type=LimitType.MINIMUM,
                                                             minimum=0.007).verify(ti.calculated_value)

        if alt.valid_flag and not als.valid_flag:
            als.valid_flag = True
        elif als.valid_flag and not alt.valid_flag:
            alt.valid_flag = True

        if alt.valid_flag and als.valid_flag and ti.valid_flag:
            return True, ''
        else:
            return False, ''

    def __str__(self):
        return 'Al+Ti'


class NormalStrengthSteelFineGrainAlPlusNbLimit(ChemicalCompositionCombinedLimit):
    def verify(self, value) -> Tuple[bool, str]:
        chemical_composition: Dict[str, ChemicalElementValue] = value
        alt = self.get_element_value('Alt', chemical_composition)
        als = self.get_element_value('Als', chemical_composition)
        nb = self.get_element_value('Nb', chemical_composition)
        alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
                                                               minimum=0.015).verify(alt.calculated_value)
        als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
                                                               minimum=0.010).verify(als.calculated_value)
        nb.valid_flag, nb.message = ChemicalCompositionLimit(chemical_element='Nb', limit_type=LimitType.MINIMUM,
                                                             minimum=0.010).verify(nb.calculated_value)

        if alt.valid_flag and not als.valid_flag:
            als.valid_flag = True
        elif als.valid_flag and not alt.valid_flag:
            alt.valid_flag = True

        if alt.valid_flag and als.valid_flag and nb.valid_flag:
            return True, ''
        else:
            return False, ''

    def __str__(self):
        return 'Al+Nb'


class NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit(ChemicalCompositionCombinedLimit):
    def verify(self, value) -> Tuple[bool, str]:
        chemical_composition: Dict[str, ChemicalElementValue] = value
        alt = self.get_element_value('Alt', chemical_composition)
        als = self.get_element_value('Als', chemical_composition)
        nb = self.get_element_value('Nb', chemical_composition)
        ti = self.get_element_value('Ti', chemical_composition)
        alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
                                                               minimum=0.015).verify(alt.calculated_value)
        als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
                                                               minimum=0.010).verify(als.calculated_value)
        nb.valid_flag, nb.message = ChemicalCompositionLimit(chemical_element='Nb', limit_type=LimitType.MINIMUM,
                                                             minimum=0.010).verify(nb.calculated_value)
        ti.valid_flag, ti.message = ChemicalCompositionLimit(chemical_element='Ti', limit_type=LimitType.MINIMUM,
                                                             minimum=0.007).verify(ti.calculated_value)

        if alt.valid_flag and not als.valid_flag:
            als.valid_flag = True
        elif als.valid_flag and not alt.valid_flag:
            alt.valid_flag = True

        if alt.valid_flag and als.valid_flag and nb.valid_flag and ti.valid_flag:
            return True, ''
        else:
            return False, ''

    def __str__(self):
        return 'Al+Nb+Ti'


class HighStrengthSteelFineGrainAlPlusTiLimit(ChemicalCompositionCombinedLimit):
    def verify(self, value) -> Tuple[bool, str]:
        chemical_composition: Dict[str, ChemicalElementValue] = value
        alt = self.get_element_value('Alt', chemical_composition)
        als = self.get_element_value('Als', chemical_composition)
        ti = self.get_element_value('Ti', chemical_composition)
        alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
                                                               minimum=0.015).verify(alt.calculated_value)
        als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
                                                               minimum=0.010).verify(als.calculated_value)
        ti.valid_flag, ti.message = ChemicalCompositionLimit(chemical_element='Ti', limit_type=LimitType.RANGE,
                                                             minimum=0.007, maximum=0.02).verify(ti.calculated_value)

        if alt.valid_flag and not als.valid_flag:
            als.valid_flag = True
        elif als.valid_flag and not alt.valid_flag:
            alt.valid_flag = True

        if alt.valid_flag and als.valid_flag and ti.valid_flag:
            return True, ''
        else:
            return False, ''

    def __str__(self):
        return 'Al+Ti'


class HighStrengthSteelFineGrainAlPlusNbPlusTiLimit(ChemicalCompositionCombinedLimit):
    def verify(self, value) -> Tuple[bool, str]:
        chemical_composition: Dict[str, ChemicalElementValue] = value
        alt = self.get_element_value('Alt', chemical_composition)
        als = self.get_element_value('Als', chemical_composition)
        nb = self.get_element_value('Nb', chemical_composition)
        ti = self.get_element_value('Ti', chemical_composition)
        alt.valid_flag, alt.message = ChemicalCompositionLimit(chemical_element='Alt', limit_type=LimitType.MINIMUM,
                                                               minimum=0.015).verify(alt.calculated_value)
        als.valid_flag, als.message = ChemicalCompositionLimit(chemical_element='Als', limit_type=LimitType.MINIMUM,
                                                               minimum=0.010).verify(als.calculated_value)
        nb.valid_flag, nb.message = ChemicalCompositionLimit(chemical_element='Nb', limit_type=LimitType.RANGE,
                                                             minimum=0.010, maximum=0.050).verify(nb.calculated_value)
        ti.valid_flag, ti.message = ChemicalCompositionLimit(chemical_element='Ti', limit_type=LimitType.RANGE,
                                                             minimum=0.007, maximum=0.020).verify(ti.calculated_value)

        if alt.valid_flag and not als.valid_flag:
            als.valid_flag = True
        elif als.valid_flag and not alt.valid_flag:
            alt.valid_flag = True

        if alt.valid_flag and als.valid_flag and nb.valid_flag and ti.valid_flag:
            return True, ''
        else:
            return False, ''

    def __str__(self):
        return 'Al+Nb+Ti'


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
    limit_type: LimitType = LimitType.MAXIMUM
    unit: str = 'mm'

    def verify(self, value: Union[float, int]) -> Tuple[bool, str]:
        if value <= self.maximum:
            message = f"[PASS] Thickness value is {value}, meets the maximum limit {self.maximum} {self.unit}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Thickness value is {value}, violates the maximum limit {self.maximum} {self.unit}."
            print(message)
            return False, message

    def get_element(self, certificate: Certificate, steel_plate_index: int) -> CertificateElementToVerify:
        return certificate.thickness


@dataclass
class YieldStrengthLimit(Limit):
    minimum: int
    limit_type: LimitType = LimitType.MINIMUM
    unit: str = 'MPa'

    def verify(self, value: int) -> Tuple[bool, str]:
        if value >= self.minimum:
            message = f"[PASS] Yield Strength value is {value}, meets the minimum limit {self.minimum} {self.unit}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Yield Strength value is {value}, violates the minimum limit {self.minimum} {self.unit}."
            print(message)
            return False, message

    def get_element(self, certificate: Certificate, steel_plate_index: int) -> CertificateElementToVerify:
        yield_strength = certificate.steel_plates[steel_plate_index].yield_strength
        if yield_strength:
            return yield_strength
        else:
            raise ValueError(
                f"Could not find value of Yield Strength in the plate whose serial number is {steel_plate_index + 1}."
            )


@dataclass
class TensileStrengthLimit(Limit):
    minimum: int
    maximum: int
    limit_type: LimitType = LimitType.RANGE
    unit: str = 'MPa'

    def verify(self, value: int) -> Tuple[bool, str]:
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

    def get_element(self, certificate: Certificate, steel_plate_index: int) -> CertificateElementToVerify:
        tensile_strength = certificate.steel_plates[steel_plate_index].tensile_strength
        if tensile_strength:
            return tensile_strength
        else:
            raise ValueError(
                f"Could not find value of Tensile Strength in the plate whose serial number is {steel_plate_index + 1}."
            )


@dataclass
class ElongationLimit(Limit):
    minimum: int
    limit_type: LimitType = LimitType.MINIMUM
    unit: str = '%'

    def verify(self, value: int) -> Tuple[bool, str]:
        if value >= self.minimum:
            message = f"[PASS] Elongation value is {value}, meets the minimum limit {self.minimum} {self.unit}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Elongation value is {value}, violates the minimum limit {self.minimum} {self.unit}."
            print(message)
            return False, message

    def get_element(self, certificate: Certificate, steel_plate_index: int) -> CertificateElementToVerify:
        elongation = certificate.steel_plates[steel_plate_index].elongation
        if elongation:
            return elongation
        else:
            raise ValueError(
                f"Could not find value of Elongation in the plate whose serial number is {steel_plate_index + 1}."
            )


@dataclass
class TemperatureLimit(Limit):
    unique_value: int
    limit_type: LimitType = LimitType.UNIQUE
    unit: str = 'Degrees Celsius'

    def verify(self, value: int) -> Tuple[bool, str]:
        if value == self.unique_value:
            message = f"[PASS] Temperature value is {value}, meets the valid value {self.unique_value} {self.unit}."
            print(message)
            return True, message
        else:
            message = f"[FAIL] Temperature value is {value}, violates the valid value {self.unique_value} {self.unit}."
            print(message)
            return False, message

    def get_element(self, certificate: Certificate, steel_plate_index: int) -> CertificateElementToVerify:
        temperature = certificate.steel_plates[steel_plate_index].temperature
        if temperature:
            return temperature
        else:
            raise ValueError(
                f"Could not find value of Temperature in the plate whose serial number is {steel_plate_index + 1}."
            )


@dataclass
class ImpactEnergyLimit(Limit):
    minimum: int
    test_number: str
    limit_type: LimitType = LimitType.MINIMUM
    unit: str = 'J'

    def verify(self, value: int) -> Tuple[bool, str]:
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

    def get_element(self, certificate: Certificate, steel_plate_index: int) -> CertificateElementToVerify:
        impact_energy_list = certificate.steel_plates[steel_plate_index].impact_energy_list
        if len(impact_energy_list) == 4:
            if self.test_number == '1':
                return impact_energy_list[0]
            elif self.test_number == '2':
                return impact_energy_list[1]
            elif self.test_number == '3':
                return impact_energy_list[2]
            elif self.test_number == 'AVE.':
                return impact_energy_list[3]
            else:
                raise ValueError(
                    f"Test number value {self.test_number} of impact energy is not expected."
                )
        else:
            raise ValueError(
                f"It is expected to have 4 values of impact energy, so far there is {len(impact_energy_list)}."
            )


class RuleMaker(metaclass=SingletonABCMeta):

    @abstractmethod
    def get_fine_grain_elements_rules(self, certificate: Certificate, steel_plate_index: int) -> List[
            ChemicalCompositionCombinedLimit]:
        pass

    @staticmethod
    def get_rules(certificate: Certificate, steel_plate_index: int) -> List[Limit]:
        limit_list: List[Limit] = []
        delivery_condition = certificate.steel_plates[steel_plate_index].delivery_condition
        thickness = certificate.thickness
        impact_test_direction = 'None' \
            if certificate.steel_plates[steel_plate_index].position_direction_impact is None \
            else CommonUtils.translate_to_vl_direction(
                certificate.steel_plates[steel_plate_index].position_direction_impact.value)
        # Chemical Composition
        #   - Normal Strength Steel
        if certificate.specification.value == 'VL A':
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
            limit_list.append(CPlusMnLimit())
        elif certificate.specification.value == 'VL B':
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='C', limit_type=LimitType.MAXIMUM, maximum=0.21))
            limit_list.append(
                ChemicalCompositionLimit(chemical_element='Si', limit_type=LimitType.MAXIMUM, maximum=0.35))
            # Mn: Table 5 Foot Note 6 - minimum 0.60% when the steel is impact tested
            if len(certificate.steel_plates[steel_plate_index].impact_energy_list) > 0:
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
            limit_list.append(CPlusMnLimit())
        elif certificate.specification.value == 'VL D':
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
            limit_list.append(CPlusMnLimit())
        elif certificate.specification.value == 'VL E':
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
            limit_list.append(CPlusMnLimit())
        #   - High Strength Steel
        elif certificate.specification.value in ('VL A27S', 'VL D27S', 'VL E27S'):
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
        elif certificate.specification.value in (
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
            if thickness.value <= 12.5:
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
        elif certificate.specification.value in ('VL F27S', 'VL F32', 'VL F36', 'VL F40'):
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
        else:
            raise ValueError(
                f"Specification value {certificate.specification.value} is outside the area of the Chemical "
                f"Composition limits."
            )
        # High Strength Steel - Table 10 Maximum carbon equivalent values (Ceq) for high strength steel supplied in TM
        # condition.
        if delivery_condition.value == 'TM':
            if certificate.specification.value in ('VL A27S', 'VL D27S', 'VL E27S', 'VL F27S'):
                if thickness.value <= 50:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.34))
                elif 50 < thickness.value <= 100:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.36))
                elif 100 < thickness.value <= 150:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.38))
                else:
                    raise ValueError(
                        f"Thickness value {thickness.value} is out of the area in Table 10 Maximum carbon equivalent "
                        f"values (Ceq) for high strength steel supplied in TM condition."
                    )
            elif certificate.specification.value in ('VL A32', 'VL D32', 'VL E32', 'VL F32'):
                if thickness.value <= 50:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.36))
                elif 50 < thickness.value <= 100:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.38))
                elif 100 < thickness.value <= 150:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.40))
                else:
                    raise ValueError(
                        f"Thickness value {thickness.value} is out of the area in Table 10 Maximum carbon equivalent "
                        f"values (Ceq) for high strength steel supplied in TM condition."
                    )
            elif certificate.specification.value in ('VL A36', 'VL D36', 'VL E36', 'VL F36'):
                if thickness.value <= 50:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.38))
                elif 50 < thickness.value <= 100:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.40))
                elif 100 < thickness.value <= 150:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.42))
                else:
                    raise ValueError(
                        f"Thickness value {thickness.value} is out of the area in Table 10 Maximum carbon equivalent "
                        f"values (Ceq) for high strength steel supplied in TM condition."
                    )
            elif certificate.specification.value in ('VL A40', 'VL D40', 'VL E40', 'VL F40'):
                if thickness.value <= 50:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.40))
                elif 50 < thickness.value <= 100:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.42))
                elif 100 < thickness.value <= 150:
                    limit_list.append(
                        ChemicalCompositionLimit(chemical_element='Ceq', limit_type=LimitType.MAXIMUM, maximum=0.45))
                else:
                    raise ValueError(
                        f"Thickness value {thickness.value} is out of the area in Table 10 Maximum carbon equivalent "
                        f"values (Ceq) for high strength steel supplied in TM condition."
                    )
        # Mechanical Properties
        #   - Normal Strength Steel
        if certificate.specification.value == 'VL A':
            limit_list.append(YieldStrengthLimit(minimum=235))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=520))
            limit_list.append(ElongationLimit(minimum=22))
            if thickness.value <= 50:
                pass
            elif 50 < thickness.value <= 70:
                if delivery_condition.value == 'N':
                    pass
                else:
                    limit_list.append(TemperatureLimit(unique_value=20))
                    if impact_test_direction == Direction.LONGITUDINAL:
                        limit_list.append(ImpactEnergyLimit(minimum=34, test_number='1'))
                        limit_list.append(ImpactEnergyLimit(minimum=34, test_number='2'))
                        limit_list.append(ImpactEnergyLimit(minimum=34, test_number='3'))
                        limit_list.append(ImpactEnergyLimit(minimum=34, test_number='AVE.'))
                    elif impact_test_direction == Direction.TRANSVERSE:
                        limit_list.append(ImpactEnergyLimit(minimum=24, test_number='1'))
                        limit_list.append(ImpactEnergyLimit(minimum=24, test_number='2'))
                        limit_list.append(ImpactEnergyLimit(minimum=24, test_number='3'))
                        limit_list.append(ImpactEnergyLimit(minimum=24, test_number='AVE.'))
                    else:
                        raise ValueError(
                            f"Impact test direction value {impact_test_direction} is not expected."
                        )
            elif 70 < thickness.value <= 150:
                if delivery_condition.value == 'N':
                    pass
                else:
                    limit_list.append(TemperatureLimit(unique_value=20))
                    if impact_test_direction == Direction.LONGITUDINAL:
                        limit_list.append(ImpactEnergyLimit(minimum=41, test_number='1'))
                        limit_list.append(ImpactEnergyLimit(minimum=41, test_number='2'))
                        limit_list.append(ImpactEnergyLimit(minimum=41, test_number='3'))
                        limit_list.append(ImpactEnergyLimit(minimum=41, test_number='AVE.'))
                    elif impact_test_direction == Direction.TRANSVERSE:
                        limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                        limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                        limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                        limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                    else:
                        raise ValueError(
                            f"Impact test direction value {impact_test_direction} is not expected."
                        )
            else:
                raise ValueError(
                    f"Thickness value {thickness.value} is out of the area of impact test."
                )
        elif certificate.specification.value == 'VL B':
            limit_list.append(YieldStrengthLimit(minimum=235))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=520))
            limit_list.append(ElongationLimit(minimum=22))
            if thickness.value <= 25:
                pass
            if 25 < thickness.value <= 50:
                limit_list.append(TemperatureLimit(unique_value=0))
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 50 < thickness.value <= 70:
                limit_list.append(TemperatureLimit(unique_value=0))
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 70 < thickness.value <= 150:
                limit_list.append(TemperatureLimit(unique_value=0))
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            else:
                raise ValueError(
                    f"Thickness value {thickness.value} is out of the area of impact test."
                )
        elif certificate.specification.value == 'VL D':
            limit_list.append(YieldStrengthLimit(minimum=235))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=520))
            limit_list.append(ElongationLimit(minimum=22))
            limit_list.append(TemperatureLimit(unique_value=-20))
            if thickness.value <= 50:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 50 < thickness.value <= 70:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 70 < thickness.value <= 150:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            else:
                raise ValueError(
                    f"Thickness value {thickness.value} is out of the area of impact test."
                )
        elif certificate.specification.value == 'VL E':
            limit_list.append(YieldStrengthLimit(minimum=235))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=520))
            limit_list.append(ElongationLimit(minimum=22))
            limit_list.append(TemperatureLimit(unique_value=-40))
            if thickness.value <= 50:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 50 < thickness.value <= 70:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 70 < thickness.value <= 150:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            else:
                raise ValueError(
                    f"Thickness value {thickness.value} is out of the area of impact test."
                )
        elif certificate.specification.value in ('VL A27S', 'VL D27S', 'VL E27S', 'VL F27S'):
            limit_list.append(YieldStrengthLimit(minimum=265))
            limit_list.append(TensileStrengthLimit(minimum=400, maximum=530))
            limit_list.append(ElongationLimit(minimum=22))
            if thickness.value <= 50:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=20, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 50 < thickness.value <= 70:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 70 < thickness.value <= 150:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            else:
                raise ValueError(
                    f"Thickness value {thickness.value} is out of the area of impact test."
                )
        elif certificate.specification.value in ('VL A32', 'VL D32', 'VL E32', 'VL F32'):
            limit_list.append(YieldStrengthLimit(minimum=315))
            limit_list.append(TensileStrengthLimit(minimum=440, maximum=570))
            limit_list.append(ElongationLimit(minimum=22))
            if thickness.value <= 50:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=22, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=22, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=22, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=22, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 50 < thickness.value <= 70:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=38, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=38, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=38, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=38, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=26, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=26, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=26, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=26, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 70 < thickness.value <= 150:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=46, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=46, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=46, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=46, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            else:
                raise ValueError(
                    f"Thickness value {thickness.value} is out of the area of impact test."
                )
        elif certificate.specification.value in ('VL A36', 'VL D36', 'VL E36', 'VL F36'):
            limit_list.append(YieldStrengthLimit(minimum=355))
            limit_list.append(TensileStrengthLimit(minimum=490, maximum=630))
            limit_list.append(ElongationLimit(minimum=21))
            if thickness.value <= 50:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=24, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 50 < thickness.value <= 70:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=41, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=27, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 70 < thickness.value <= 150:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=50, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=50, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=50, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=50, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=34, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            else:
                raise ValueError(
                    f"Thickness value {thickness.value} is out of the area of impact test."
                )
        elif certificate.specification.value in ('VL A40', 'VL D40', 'VL E40', 'VL F40'):
            limit_list.append(YieldStrengthLimit(minimum=390))
            limit_list.append(TensileStrengthLimit(minimum=510, maximum=660))
            limit_list.append(ElongationLimit(minimum=20))
            if thickness.value <= 50:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=39, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=39, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=39, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=39, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=26, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=26, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=26, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=26, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 50 < thickness.value <= 70:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=46, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=46, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=46, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=46, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=31, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            elif 70 < thickness.value <= 150:
                if impact_test_direction == Direction.LONGITUDINAL:
                    limit_list.append(ImpactEnergyLimit(minimum=55, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=55, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=55, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=55, test_number='AVE.'))
                elif impact_test_direction == Direction.TRANSVERSE:
                    limit_list.append(ImpactEnergyLimit(minimum=37, test_number='1'))
                    limit_list.append(ImpactEnergyLimit(minimum=37, test_number='2'))
                    limit_list.append(ImpactEnergyLimit(minimum=37, test_number='3'))
                    limit_list.append(ImpactEnergyLimit(minimum=37, test_number='AVE.'))
                else:
                    raise ValueError(
                        f"Impact test direction value {impact_test_direction} is not expected."
                    )
            else:
                raise ValueError(
                    f"Thickness value {thickness.value} is out of the area of impact test."
                )
        else:
            raise ValueError(
                f"Certificate specification value {certificate.specification.value} is out of the area of Mechanical "
                f"properties."
            )
        # Mechanical Properties - High Strength Steel - Impact Test Temperature
        if certificate.specification.value in ('VL A27S', 'VL A32', 'VL A36', 'VL A40'):
            limit_list.append(TemperatureLimit(unique_value=0))
        elif certificate.specification.value in ('VL D27S', 'VL D32', 'VL D36', 'VL D40'):
            limit_list.append(TemperatureLimit(unique_value=-20))
        elif certificate.specification.value in ('VL E27S', 'VL E32', 'VL E36', 'VL E40'):
            limit_list.append(TemperatureLimit(unique_value=-40))
        elif certificate.specification.value in ('VL F27S', 'VL F32', 'VL F36', 'VL F40'):
            limit_list.append(TemperatureLimit(unique_value=-60))

        return limit_list


class BaoSteelRuleMaker(RuleMaker):

    def get_fine_grain_elements_rules(self, certificate: Certificate, steel_plate_index: int) -> List[
            ChemicalCompositionCombinedLimit]:
        limit_list: List[ChemicalCompositionCombinedLimit] = []

        specification = certificate.specification
        delivery_condition = certificate.steel_plates[steel_plate_index].delivery_condition
        thickness = certificate.thickness

        # Normal Strength Steel
        if specification.value in ('VL A', 'VL B'):
            if delivery_condition.value == 'N':
                if thickness.value <= 35:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 80:
                    limit_list.append(NormalStrengthSteelFineGrainAlLimit())
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusNbLimit())
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'AR':
                if thickness.value <= 50:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
                # TODO When we enable Z35, we need to add a condition that the thickness limit changed to 35.
            elif delivery_condition.value == 'TM':
                if thickness.value <= 100:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL D':
            if delivery_condition.value == 'AR':
                if thickness.value <= 35:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'N':
                if thickness.value <= 35:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 80:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusNbLimit())
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 100:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL E':
            if delivery_condition.value == 'N':
                if thickness.value <= 35:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 80:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusNbLimit())
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 100:
                    limit_list.append(NormalStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        # High Strength Steel
        elif specification.value == 'VL A27S':
            if delivery_condition.value == 'AR':
                if thickness.value <= 20:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'N':
                if thickness.value <= 30:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 80:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'NR':
                if thickness.value <= 30:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 40:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL A32':
            if delivery_condition.value == 'AR':
                if thickness.value <= 20:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'N':
                if thickness.value <= 30:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 80:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'NR':
                if thickness.value <= 30:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 40:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 50:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
        elif specification.value == 'VL A36':
            if delivery_condition.value == 'AR':
                if thickness.value <= 20:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'NR':
                if thickness.value <= 30:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 40:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'N':
                if thickness.value <= 80:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 50:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL A40':
            if delivery_condition.value == 'TM':
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL D27S':
            if delivery_condition.value == 'AR':
                if thickness.value <= 20:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'N':
                if thickness.value <= 30:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 80:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'NR':
                if thickness.value <= 40:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL D32':
            if delivery_condition.value == 'AR':
                if thickness.value <= 20:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'N':
                if thickness.value <= 30:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 80:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'NR':
                if thickness.value <= 40:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 50:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL D36':
            if delivery_condition.value == 'AR':
                if thickness.value <= 20:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'N':
                if thickness.value <= 80:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'NR':
                if thickness.value <= 40:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 50:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL D40':
            if delivery_condition.value == 'TM':
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL E27S':
            if delivery_condition.value == 'N':
                if thickness.value <= 80:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL E32':
            if delivery_condition.value == 'N':
                if thickness.value <= 80:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 50:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL E36':
            if delivery_condition.value == 'N':
                if thickness.value <= 80:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            elif delivery_condition.value == 'TM':
                if thickness.value <= 50:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusTiLimit())
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == 'VL E40':
            if delivery_condition.value == 'TM':
                if thickness.value <= 90:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        elif specification.value == ('VL F27S', 'VL F32', 'VL F36', 'VL F40'):
            if delivery_condition.value == 'TM':
                if thickness.value <= 68:
                    limit_list.append(HighStrengthSteelFineGrainAlPlusNbPlusTiLimit())
                else:
                    BaoSteelRuleMaker.update_thickness(delivery_condition, specification, thickness)
            else:
                BaoSteelRuleMaker.update_delivery_condition(delivery_condition, specification)
        else:
            specification.valid_flag = False
            specification.message = (
                f"The specification value {specification.value} is not expected according to agreed document."
            )

        return limit_list

    @staticmethod
    def update_thickness(delivery_condition: DeliveryCondition, specification: Specification, thickness: Thickness):
        thickness.valid_flag = False
        thickness.message = (
            f"[FAIL] The thickness value {thickness.value} violates the maximum limit of Specification "
            f"{specification.value} and Delivery Condition {delivery_condition.value}."
        )

    @staticmethod
    def update_delivery_condition(delivery_condition: DeliveryCondition, specification: Specification):
        delivery_condition.valid_flag = False
        delivery_condition.message = (
            f"[FAIL] The delivery condition value {delivery_condition.value} is not expected for specification "
            f"{specification.value}."
        )
