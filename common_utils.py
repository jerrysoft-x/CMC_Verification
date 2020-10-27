from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Union, Dict
from enum import Enum, unique

from certificate_element import Specification, Thickness, SerialNumbers, SteelPlate, ChemicalElementName, \
    CertificateElementToVerify


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonABCMeta(ABCMeta):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


@dataclass
class Certificate(metaclass=ABCMeta):
    file_path: str
    steel_plant: str
    specification: Specification
    thickness: Thickness
    serial_numbers: SerialNumbers
    steel_plates: List[SteelPlate]
    chemical_elements: Dict[str, ChemicalElementName]

    def __str__(self):
        chemical_element_str = {element: self.chemical_elements[element].precision for element in
                                self.chemical_elements}
        steel_plates_str = '\n'.join([str(steel_plate) for steel_plate in self.steel_plates])
        return (
            f"BaoSteelCertificate:\n"
            f"\tFile Path: {self.file_path}\n"
            f"\tSteel Plant: {self.steel_plant}\n"
            f"\tSpecification: {self.specification.value}\n"
            f"\tThickness: {self.thickness.value}\n"
            f"\tChemical Elements: {chemical_element_str}\n"
            f"\tSerial Numbers: {self.serial_numbers.value}\n"
            f"\tSteel Plates:\n{steel_plates_str}"
        )


class Limit(metaclass=ABCMeta):
    @abstractmethod
    def verify(self, value) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def get_element(self, certificate: Certificate, steel_plate_index: int):
        pass


@unique
class TableSearchType(Enum):
    SPLIT_LINE_BREAK_END = 1  # split by line break (\n) and check if the last element matches the keyword
    SPLIT_LINE_BREAK_START = 2  # split by line break (\n) and check if the first element matches the keyword
    REMOVE_LINE_BREAK_CONTAIN = 3  # remove all line breaks (\n) and check if contains the keyword
    SPLIT_LINE_BREAK_ALL_DIGIT = 4  # split by line break (\n) and check if all the elements are integer.


@unique
class Direction(Enum):
    TRANSVERSE = 'Transverse'  # 横向
    LONGITUDINAL = 'Longitudinal'  # 纵向


class CommonUtils:

    chemical_elements_table = [
        'C', 'Si', 'Mn', 'P', 'S', 'Cu', 'Cr', 'Ni', 'Mo', 'Ceq', 'Als', 'Alt', 'Nb', 'Ti', 'V'
    ]

    @staticmethod
    def search_table(
        table: List[List[Union[str, None]]],
        keyword: Union[str, None],
        search_type: TableSearchType = TableSearchType.SPLIT_LINE_BREAK_END,
        confirmed_row: int = None,
        confirmed_col: int = None
    ) -> Union[Tuple[int, int], None]:

        # Define search methods:
        search_methods = {
            TableSearchType.SPLIT_LINE_BREAK_END:
                lambda table_cell: table_cell is not None and table_cell.split('\n')[-1].strip() == keyword,
            TableSearchType.SPLIT_LINE_BREAK_START:
                lambda table_cell: table_cell is not None and table_cell.split('\n')[0].strip() == keyword,
            TableSearchType.REMOVE_LINE_BREAK_CONTAIN:
                lambda table_cell: table_cell is not None and keyword in table_cell.replace('\n', '').replace(' ', ''),
            TableSearchType.SPLIT_LINE_BREAK_ALL_DIGIT:
                lambda table_cell: table_cell is not None and all(
                    map(lambda x: x.strip().isdigit(), table_cell.split('\n')))
        }

        coordinates = None

        if confirmed_row is None:
            if confirmed_col is None:
                for row_index, row in enumerate(table):
                    if coordinates is not None:
                        break
                    for col_index, cell in enumerate(row):
                        if search_methods[search_type](cell):
                            coordinates = (row_index, col_index)
                            break
            else:
                for row_index, row in enumerate(table):
                    cell = row[confirmed_col]
                    if search_methods[search_type](cell):
                        coordinates = (row_index, confirmed_col)
                        break
        else:
            if confirmed_col is None:
                row = table[confirmed_row]
                for col_index, cell in enumerate(row):
                    if search_methods[search_type](cell):
                        coordinates = (confirmed_row, col_index)
                        break
            else:
                cell = table[confirmed_row][confirmed_col]
                if search_methods[search_type](cell):
                    coordinates = (confirmed_row, confirmed_col)

        return coordinates

    @staticmethod
    def verify_chemical_element_limit(element: str, chemical_composition_limit: dict, element_calculated_value: float):
        if chemical_composition_limit['type'] == 'maximum':
            if element_calculated_value <= chemical_composition_limit['limit']:
                print(
                    f"The value of chemical element {element} is {element_calculated_value}, meets "
                    f"the maximum limit {chemical_composition_limit['limit']}."
                )
            else:
                print(
                    f"The value of chemical element {element} is {element_calculated_value}, violates "
                    f"the maximum limit {chemical_composition_limit['limit']}."
                )
                return False
        elif chemical_composition_limit['type'] == 'minimum':
            if element_calculated_value >= chemical_composition_limit['limit']:
                print(
                    f"The value of chemical element {element} is {element_calculated_value}, meets "
                    f"the minimum limit {chemical_composition_limit['limit']}."
                )
            else:
                print(
                    f"The value of chemical element {element} is {element_calculated_value}, violates "
                    f"the minimum limit {chemical_composition_limit['limit']}."
                )
                return False
        elif chemical_composition_limit['type'] == 'range':
            if chemical_composition_limit['minimum'] <= element_calculated_value <= \
                    chemical_composition_limit['maximum']:
                print(
                    f"The value of chemical element {element} is {element_calculated_value}, meets "
                    f"the valid range [{chemical_composition_limit['minimum']}, "
                    f"{chemical_composition_limit['maximum']}]."
                )
            else:
                print(
                    f"The value of chemical element {element} is {element_calculated_value}, violates "
                    f"the valid range [{chemical_composition_limit['minimum']}, "
                    f"{chemical_composition_limit['maximum']}]."
                )
                return False
        else:
            raise ValueError(
                f"The chemical composition limit type {chemical_composition_limit['type']} of "
                f"chemical element {element} is invalid!"
            )
        return True

    @staticmethod
    def translate_to_vl_direction(position_direction_value: str) -> Direction:
        map_to_vl_direction = {
            'C': Direction.TRANSVERSE,
            'L': Direction.LONGITUDINAL
        }
        c_flag = 'C' in position_direction_value
        l_flag = 'L' in position_direction_value
        if c_flag and not l_flag:
            return map_to_vl_direction['C']
        if l_flag and not c_flag:
            return map_to_vl_direction['L']
        if c_flag and l_flag:
            raise ValueError(
                f"The position direction value {position_direction_value} contains both C (Transverse) and "
                f"L (Longitudinal), it is invalid."
            )
        if not c_flag and not l_flag:
            raise ValueError(
                f"The position direction value {position_direction_value} contains neither C (Transverse) nor "
                f"L (Longitudinal), it is invalid."
            )
