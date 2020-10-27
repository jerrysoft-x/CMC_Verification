from typing import List, Dict, Tuple, Optional
from abc import abstractmethod
from certificate_element import PDFFile, Specification, Thickness, SerialNumbers, SteelPlate, ChemicalElementName, \
    DeliveryCondition, Mass, ChemicalElementValue, YieldStrength, TensileStrength, Elongation, \
    PositionDirectionImpact, Temperature, ImpactEnergy, PlateNo
from dataclasses import dataclass

# from certificate_verification import BaoSteelRuleMaker, RuleMaker
from certificate_verification import RuleMaker, BaoSteelRuleMaker
from common_utils import CommonUtils, TableSearchType, Certificate, SingletonABCMeta


@dataclass
class BaoSteelCertificate(Certificate):
    pass


# Here the term of factory is not related to the steel plant, it is purely the concept of Factory Method design pattern.
# The pattern improves the code loosely coupled for better maintainability and extensibility.
# This class contains the factory method act as the creator of the certificates, and it must be instantiated by
# subclasses dedicated for each steel plant respectively.
class CertificateFactory(metaclass=SingletonABCMeta):

    @abstractmethod
    def read(self, pdf_file: PDFFile) -> Certificate:
        pass

    @abstractmethod
    def get_rule_maker(self) -> RuleMaker:
        pass


class BaoSteelCertificateFactory(CertificateFactory):

    # ################################ Singleton ################################ #
    # _singleton = None
    #
    # @classmethod
    # def get_singleton(cls):
    #     if not isinstance(cls._singleton, cls):
    #         cls._singleton = cls()
    #     return cls._singleton
    # ################################ Singleton ################################ #

    def get_rule_maker(self) -> RuleMaker:
        return BaoSteelRuleMaker()

    def read(self, pdf_file: PDFFile) -> Certificate:
        specification = BaoSteelCertificateFactory.extract_specification(pdf_file)
        thickness = BaoSteelCertificateFactory.extract_thickness(pdf_file)
        serial_numbers = BaoSteelCertificateFactory.extract_serial_numbers(pdf_file)
        chemical_elements, chemical_col_counter = BaoSteelCertificateFactory.extract_chemical_elements(pdf_file)
        non_test_lot_no_map = BaoSteelCertificateFactory.generate_non_test_lot_no_map(pdf_file, serial_numbers)
        # "Test Lot No" is something interrupting the extraction of position direction value, we need a mapping to help
        # skipping the Test Lot No values.
        steel_plates = BaoSteelCertificateFactory.extract_steel_plates(
            pdf_file=pdf_file,
            specification=specification,
            thickness=thickness,
            serial_numbers=serial_numbers,
            chemical_elements=chemical_elements,
            chemical_col_counter=chemical_col_counter,
            non_test_lot_no_map=non_test_lot_no_map
        )
        certificate = BaoSteelCertificate(
            file_path=pdf_file.pdf_path,
            steel_plant=pdf_file.steel_plant,
            specification=specification,
            thickness=thickness,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates,
            chemical_elements=chemical_elements
        )
        return certificate

    @staticmethod
    def generate_non_test_lot_no_map(pdf_file: PDFFile, serial_numbers: SerialNumbers) -> Dict[int, int]:
        # The number is always in the second table
        _, data_table = pdf_file.tables

        # The title "Test Lot No" is listed in the "PLATE NO." column, it's neighboring the Serial Numbers cell.
        x_coordinate = serial_numbers.x_coordinate
        y_coordinate = serial_numbers.y_coordinate + 1

        matching_index_gen = (index for index, item in enumerate(data_table[x_coordinate][y_coordinate].split('\n')) if
                              'Test Lot No:' not in item)

        non_test_lot_no_map: Dict[int, int] = dict()

        for steel_plate_index in range(len(serial_numbers)):
            try:
                matching_index = next(matching_index_gen)
                non_test_lot_no_map[steel_plate_index] = matching_index
            except StopIteration as e:
                print(f"Cannot match index {steel_plate_index} in 'NO.' with the index in 'PLATE NO.'.")
                raise e

        return non_test_lot_no_map

    @staticmethod
    def extract_steel_plates(
        pdf_file: PDFFile,
        specification: Specification,
        thickness: Thickness,
        serial_numbers: SerialNumbers,
        chemical_elements: Dict[str, ChemicalElementName],
        chemical_col_counter: Dict[int, int],
        non_test_lot_no_map: Dict[int, int]
    ) -> List[SteelPlate]:
        steel_plates = []
        for serial_number in serial_numbers:
            steel_plates.append(SteelPlate(serial_number))
        BaoSteelCertificateFactory.extract_mass(
            pdf_file=pdf_file,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates
        )
        BaoSteelCertificateFactory.extract_chemical_composition(
            pdf_file=pdf_file,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates,
            chemical_elements=chemical_elements,
            chemical_col_counter=chemical_col_counter
        )
        BaoSteelCertificateFactory.extract_delivery_condition(
            pdf_file=pdf_file,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates
        )
        BaoSteelCertificateFactory.extract_plate_no(
            pdf_file=pdf_file,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates,
            non_test_lot_no_map=non_test_lot_no_map
        )
        BaoSteelCertificateFactory.extract_yield_strength(
            pdf_file=pdf_file,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates,
            non_test_lot_no_map=non_test_lot_no_map
        )
        BaoSteelCertificateFactory.extract_tensile_strength(
            pdf_file=pdf_file,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates,
            non_test_lot_no_map=non_test_lot_no_map
        )
        BaoSteelCertificateFactory.extract_elongation(
            pdf_file=pdf_file,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates,
            non_test_lot_no_map=non_test_lot_no_map
        )
        impact_test_count, impact_test_map = BaoSteelCertificateFactory.impact_test_check(
            specification=specification,
            thickness=thickness,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates
        )
        if impact_test_count > 0:
            BaoSteelCertificateFactory.extract_position_direction_impact(
                pdf_file=pdf_file,
                serial_numbers=serial_numbers,
                steel_plates=steel_plates,
                non_test_lot_no_map=non_test_lot_no_map,
                # impact_test_count=impact_test_count,
                impact_test_map=impact_test_map
            )
            BaoSteelCertificateFactory.extract_temperature(
                pdf_file=pdf_file,
                serial_numbers=serial_numbers,
                steel_plates=steel_plates,
                non_test_lot_no_map=non_test_lot_no_map,
                # impact_test_count=impact_test_count,
                impact_test_map=impact_test_map
            )
            BaoSteelCertificateFactory.extract_impact_energy(
                pdf_file=pdf_file,
                serial_numbers=serial_numbers,
                steel_plates=steel_plates,
                non_test_lot_no_map=non_test_lot_no_map,
                # impact_test_count=impact_test_count,
                impact_test_map=impact_test_map
            )
        return steel_plates

    @staticmethod
    def extract_position_direction_impact(
            pdf_file: PDFFile,
            serial_numbers: SerialNumbers,
            steel_plates: List[SteelPlate],
            non_test_lot_no_map: Dict[int, int],
            # impact_test_count: int,
            impact_test_map: Dict[int, bool]
    ):
        # tensile strength data is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search the title IMPACTTEST to locate the y coordinate
        coordinates = CommonUtils.search_table(table, 'IMPACTTEST',
                                               search_type=TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find IMPACT TEST title in the given PDF {pdf_file.pdf_path}."
            )
        y_coordinate = coordinates[1]
        # x coordinate is the same of the serial numbers
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        cell_line_count = len(cell.split('\n'))
        if cell_line_count >= len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the position direction (impact test) cell, less than "
                f"the serial numbers count {len(serial_numbers)} plates in the given PDF {pdf_file.pdf_path}"
            )
        position_direction_cell_lines = cell.split('\n')

        for plate_index in range(len(serial_numbers)):
            if not impact_test_map[plate_index]:
                position_direction_cell_lines.insert(non_test_lot_no_map[plate_index], 'None')

        # Start extracting the elongation value for each plate
        for plate_index in range(len(serial_numbers)):
            if len(position_direction_cell_lines) > len(serial_numbers):
                position_direction_value = position_direction_cell_lines[non_test_lot_no_map[plate_index]]
            else:
                position_direction_value = position_direction_cell_lines[plate_index]
            if position_direction_value is not None and len(position_direction_value.strip()) > 0:
                position_direction_value = position_direction_value.strip()
            else:
                raise ValueError(
                    f"Could not find the position direction (impact test) value for plate No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.pdf_path}"
                )
            if position_direction_value == 'None':
                continue
            elif position_direction_value.isalnum():
                pass
            else:
                raise ValueError(
                    f"The position direction (impact test) value {position_direction_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} contains invalid character other than alphabet and "
                    f"number in the given PDF {pdf_file.pdf_path}"
                )
            steel_plates[plate_index].position_direction_impact = PositionDirectionImpact(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                index=plate_index,
                value=position_direction_value
            )

    @staticmethod
    def impact_test_check(specification: Specification, thickness: Thickness, serial_numbers: SerialNumbers,
                          steel_plates: List[SteelPlate]) -> Tuple[int, Dict[int, bool]]:
        impact_test_count = 0
        impact_test_map = dict()
        for steel_plate_index in range(len(serial_numbers)):
            delivery_condition = steel_plates[steel_plate_index].delivery_condition
            impact_test_flag = True
            if specification.value == 'VL A':
                if thickness.value <= 50:
                    impact_test_flag = False
                elif (50 < thickness.value <= 70) or (70 < thickness.value <= 150):
                    if delivery_condition.value == 'N':
                        impact_test_flag = False
                else:
                    raise ValueError(
                        f"Thickness value {thickness.value} is out of the value area of the impact test."
                    )
            elif specification.value == 'VL B':
                if thickness.value <= 25:
                    impact_test_flag = False
            if impact_test_flag:
                impact_test_count += 1
            impact_test_map[steel_plate_index] = impact_test_flag
        return impact_test_count, impact_test_map

    @staticmethod
    def extract_temperature(
            pdf_file: PDFFile,
            serial_numbers: SerialNumbers,
            steel_plates: List[SteelPlate],
            non_test_lot_no_map: Dict[int, int],
            # impact_test_count: int,
            impact_test_map: Dict[int, bool],
    ):
        # Firstly, hardcode that tensile strength data is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search the title TEMP to locate the y coordinate
        coordinates = CommonUtils.search_table(table, 'TEMP')
        if coordinates is None:
            raise ValueError(
                f"Could not find TEMP (Temperature) title in the given PDF {pdf_file.pdf_path}."
            )
        y_coordinate = coordinates[1]
        # x coordinate is the same of the serial numbers
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        # cell_line_count = len(cell.split('\n'))
        # if cell_line_count >= len(serial_numbers):
        #     pass
        # else:
        #     raise ValueError(
        #         f"There are {cell_line_count} lines in the temperature cell, less than "
        #         f"the serial numbers count {len(serial_numbers)} plates in the given PDF {pdf_file.pdf_path}"
        #     )
        temperature_cell_lines = cell.split('\n')

        for plate_index in range(len(serial_numbers)):
            if not impact_test_map[plate_index]:
                temperature_cell_lines.insert(non_test_lot_no_map[plate_index], 'None')

        # Start extracting the elongation value for each plate
        for plate_index in range(len(serial_numbers)):
            if len(temperature_cell_lines) > len(serial_numbers):
                temperature_value = temperature_cell_lines[non_test_lot_no_map[plate_index]]
            else:
                temperature_value = temperature_cell_lines[plate_index]
            if temperature_value is not None and len(temperature_value.strip()) > 0:
                temperature_value = temperature_value.strip()
            else:
                raise ValueError(
                    f"Could not find the temperature value for plate No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.pdf_path}"
                )
            value_to_check = temperature_value[1:] if temperature_value.startswith('-') else temperature_value
            if value_to_check == 'None':
                continue
            elif value_to_check.isdigit():
                temperature_value = int(temperature_value)
                pass
            else:
                raise ValueError(
                    f"The temperature value {temperature_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a number "
                    f"in the given PDF {pdf_file.pdf_path}"
                )
            steel_plates[plate_index].temperature = Temperature(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=temperature_value,
                index=plate_index,
                valid_flag=True,
                message=None
            )

    @staticmethod
    def extract_impact_energy(
        pdf_file: PDFFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate],
        non_test_lot_no_map: Dict[int, int],
        # impact_test_count: int,
        impact_test_map: Dict[int, bool]
    ):
        # Firstly, hardcode that tensile strength data is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search the title ABSORBED ENERGY to locate the y coordinate of the first test title.
        coordinates = CommonUtils.search_table(table, 'ABSORBEDENERGY',
                                               search_type=TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find ABSORBED ENERGY title in the given PDF {pdf_file.pdf_path}."
            )
        start_col = coordinates[1]

        # Search the title OC to locate the x coordinate of the first test title.
        coordinates = CommonUtils.search_table(table, 'OC', search_type=TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find OC title in the given PDF {pdf_file.pdf_path}."
            )
        confirmed_row = coordinates[0]

        y_coordinates: Dict[int, str] = {}
        # The titles to verify
        impact_test_titles = ['1', '2', '3', 'AVE.']

        def search_next(
            search_table: List[List[Optional[str]]],
            keyword: str,
            confirmed_search_row: int,
            start_search_col: int,
            pdf_path: str
        ) -> int:
            max_col_idx = len(search_table[confirmed_search_row]) - 1
            cursor_col = start_search_col
            while True:
                if cursor_col > max_col_idx:
                    raise ValueError(
                        f"Could not find title {keyword} in the given PDF {pdf_path}."
                    )
                else:
                    search_cell = search_table[confirmed_search_row][cursor_col]
                    if search_cell is not None and search_cell.strip() == keyword:
                        return cursor_col
                    else:
                        cursor_col += 1

        for title in impact_test_titles:
            y_coordinate = search_next(
                search_table=table,
                keyword=title,
                confirmed_search_row=confirmed_row,
                start_search_col=start_col,
                pdf_path=pdf_file.pdf_path
            )
            y_coordinates[y_coordinate] = title
            start_col = y_coordinate + 1

        # x coordinate is the same of the serial numbers
        x_coordinate = serial_numbers.x_coordinate

        for impact_energy_index, y_coordinate in enumerate(y_coordinates):

            cell = table[x_coordinate][y_coordinate]

            # cell_line_count = len(cell.split('\n'))
            # if cell_line_count >= len(serial_numbers):
            #     pass
            # else:
            #     raise ValueError(
            #         f"There are {cell_line_count} lines in the impact energy cell, less than "
            #         f"the serial numbers count {len(serial_numbers)} plates in the given PDF {pdf_file.pdf_path}"
            #     )
            impact_energy_cell_lines = cell.split('\n')

            for plate_index in range(len(serial_numbers)):
                if not impact_test_map[plate_index]:
                    impact_energy_cell_lines.insert(non_test_lot_no_map[plate_index], 'None')

            # Start extracting the elongation value for each plate
            for plate_index in range(len(serial_numbers)):
                if len(impact_energy_cell_lines) > len(serial_numbers):
                    impact_energy_value = impact_energy_cell_lines[non_test_lot_no_map[plate_index]]
                else:
                    impact_energy_value = impact_energy_cell_lines[plate_index]
                if impact_energy_value is not None and len(impact_energy_value.strip()) > 0:
                    impact_energy_value = impact_energy_value.strip()
                else:
                    raise ValueError(
                        f"Could not find the impact energy value for plate No. "
                        f"{serial_numbers[plate_index]} in the given PDF {pdf_file.pdf_path}"
                    )
                if impact_energy_value == 'None':
                    continue
                elif impact_energy_value.isdigit():
                    impact_energy_value = int(impact_energy_value)
                else:
                    raise ValueError(
                        f"The impact energy value {impact_energy_value} extracted for plate No. "
                        f"{serial_numbers[plate_index]} is not a number "
                        f"in the given PDF {pdf_file.pdf_path}"
                    )
                steel_plates[plate_index].impact_energy_list.append(
                    ImpactEnergy(
                        table_index=table_index,
                        x_coordinate=x_coordinate,
                        y_coordinate=y_coordinate,
                        value=impact_energy_value,
                        index=plate_index,
                        valid_flag=True,
                        message=None,
                        test_number=y_coordinates[y_coordinate],
                    )
                )

    @staticmethod
    def extract_plate_no(
        pdf_file: PDFFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate],
        non_test_lot_no_map: Dict[int, int]
    ):
        # Firstly, hardcode that yield strength data is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search the title PLATE NO. to locate the y coordinate
        coordinates = CommonUtils.search_table(table, 'PLATENO.', TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find PLATE NO. title in the given PDF {pdf_file.pdf_path}."
            )
        y_coordinate = coordinates[1]
        # x coordinate is the same of the serial numbers
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        cell_line_count = len(cell.split('\n'))
        if cell_line_count >= len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the plate no. cell, less than the serial numbers count "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.pdf_path}"
            )
        plate_no_cell_lines = cell.split('\n')

        # Start extracting the plate no value for each plate
        for plate_index in range(len(serial_numbers)):
            if len(plate_no_cell_lines) > len(serial_numbers):
                plate_no_value = plate_no_cell_lines[non_test_lot_no_map[plate_index]]
            else:
                plate_no_value = plate_no_cell_lines[plate_index]
            if plate_no_value is not None and len(plate_no_value.strip()) > 0:
                plate_no_value = plate_no_value.strip()
            else:
                raise ValueError(
                    f"Could not find the Plate No. value for plate No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.pdf_path}"
                )
            steel_plates[plate_index].plate_no = PlateNo(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=plate_no_value,
                index=plate_index
            )

    @staticmethod
    def extract_yield_strength(
        pdf_file: PDFFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate],
        non_test_lot_no_map: Dict[int, int]
    ):
        # Firstly, hardcode that yield strength data is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search the title Y.S. to locate the y coordinate
        coordinates = CommonUtils.search_table(table, 'Y.S.')
        if coordinates is None:
            raise ValueError(
                f"Could not find Y.S. (Yield Strength) title in the given PDF {pdf_file.pdf_path}."
            )
        y_coordinate = coordinates[1]
        # x coordinate is the same of the serial numbers
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        cell_line_count = len(cell.split('\n'))
        if cell_line_count >= len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the delivery condition cell, less than the serial numbers count "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.pdf_path}"
            )
        yield_strength_cell_lines = cell.split('\n')

        # Start extracting the yield strength value for each plate
        for plate_index in range(len(serial_numbers)):
            if len(yield_strength_cell_lines) > len(serial_numbers):
                yield_strength_value = yield_strength_cell_lines[non_test_lot_no_map[plate_index]]
            else:
                yield_strength_value = yield_strength_cell_lines[plate_index]
            if yield_strength_value is not None and len(yield_strength_value.strip()) > 0:
                yield_strength_value = yield_strength_value.strip()
            else:
                raise ValueError(
                    f"Could not find the yield strength value for plate No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.pdf_path}"
                )
            if yield_strength_value.isdigit():
                yield_strength_value = int(yield_strength_value)
                pass
            else:
                raise ValueError(
                    f"The yield strength value {yield_strength_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a number in the given "
                    f"PDF {pdf_file.pdf_path}"
                )
            steel_plates[plate_index].yield_strength = YieldStrength(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=yield_strength_value,
                index=plate_index,
                valid_flag=True,
                message=None
            )

    @staticmethod
    def extract_tensile_strength(
        pdf_file: PDFFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate],
        non_test_lot_no_map: Dict[int, int]
    ):
        # Firstly, hardcode that tensile strength data is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search the title T.S. to locate the y coordinate
        coordinates = CommonUtils.search_table(table, 'T.S.')
        if coordinates is None:
            raise ValueError(
                f"Could not find T.S. (Tensile Strength) title in the given PDF {pdf_file.pdf_path}."
            )
        y_coordinate = coordinates[1]
        # x coordinate is the same of the serial numbers
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        cell_line_count = len(cell.split('\n'))
        if cell_line_count >= len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the tensile strength cell, less than the serial numbers count "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.pdf_path}"
            )
        tensile_strength_cell_lines = cell.split('\n')

        # Start extracting the tensile strength value for each plate
        for plate_index in range(len(serial_numbers)):
            if len(tensile_strength_cell_lines) > len(serial_numbers):
                tensile_strength_value = tensile_strength_cell_lines[non_test_lot_no_map[plate_index]]
            else:
                tensile_strength_value = tensile_strength_cell_lines[plate_index]
            if tensile_strength_value is not None and len(tensile_strength_value.strip()) > 0:
                tensile_strength_value = tensile_strength_value.strip()
            else:
                raise ValueError(
                    f"Could not find the tensile strength value for plate No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.pdf_path}"
                )
            if tensile_strength_value.isdigit():
                tensile_strength_value = int(tensile_strength_value)
                pass
            else:
                raise ValueError(
                    f"The tensile strength value {tensile_strength_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a number in the given "
                    f"PDF {pdf_file.pdf_path}"
                )
            steel_plates[plate_index].tensile_strength = TensileStrength(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=tensile_strength_value,
                index=plate_index,
                valid_flag=True,
                message=None
            )

    @staticmethod
    def extract_elongation(
        pdf_file: PDFFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate],
        non_test_lot_no_map: Dict[int, int]
    ):
        # Firstly, hardcode that tensile strength data is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search the title EL. to locate the y coordinate
        coordinates = CommonUtils.search_table(table, 'EL')
        if coordinates is None:
            raise ValueError(
                f"Could not find EL (Elongation) title in the given PDF {pdf_file.pdf_path}."
            )
        y_coordinate = coordinates[1]
        # x coordinate is the same of the serial numbers
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        cell_line_count = len(cell.split('\n'))
        if cell_line_count >= len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the elongation cell, less than the serial numbers count "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.pdf_path}"
            )
        elongation_cell_lines = cell.split('\n')

        # Start extracting the elongation value for each plate
        for plate_index in range(len(serial_numbers)):
            if len(elongation_cell_lines) > len(serial_numbers):
                elongation_value = elongation_cell_lines[non_test_lot_no_map[plate_index]]
            else:
                elongation_value = elongation_cell_lines[plate_index]
            if elongation_value is not None and len(elongation_value.strip()) > 0:
                elongation_value = elongation_value.strip()
            else:
                raise ValueError(
                    f"Could not find the elongation value for plate No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.pdf_path}"
                )
            if elongation_value.isdigit():
                elongation_value = int(elongation_value)
                pass
            else:
                raise ValueError(
                    f"The elongation value {elongation_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a number in the given "
                    f"PDF {pdf_file.pdf_path}"
                )
            steel_plates[plate_index].elongation = Elongation(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=elongation_value,
                index=plate_index,
                valid_flag=True,
                message=None
            )

    @staticmethod
    def extract_chemical_elements(pdf_file: PDFFile) -> Tuple[Dict[str, ChemicalElementName], Dict[int, int]]:
        # HARD CODE: the information of chemical compositions is always in the second table.
        table_index = 1
        table = pdf_file.tables[table_index]

        # To locate the positions of the chemical composition cells, we need to find the row with both Notes *1 and *3
        # The chemical composition area starts at that row for 4 rows, and the columns are between the two notes.

        # Search Note '*1'
        coordinates = CommonUtils.search_table(table, '*1')
        if coordinates is None:
            raise ValueError(
                f"Could not find text '*1' in the given PDF {pdf_file.pdf_path}"
            )
        # If *1 is found, we can determine the index of the first row, and the columns start from the next column.
        start_row_index = coordinates[0]
        start_col_index = coordinates[1] + 1
        # If *1 is found, we need to check if *3 is at the same row,
        # so that we can determine the right boundary of the columns.
        coordinates = CommonUtils.search_table(table, '*3', confirmed_row=start_row_index)
        if coordinates is None:
            raise ValueError(
                f"Could not find text '*3' in the given PDF {pdf_file.pdf_path}"
            )
        # Now we find '*3' at the same row, we can determine the right boundary of the columns.
        end_col_index = coordinates[1]

        # There are two rows of chemical element names
        chemical_composition_name_area = [
            table[start_row_index][start_col_index: end_col_index],
            table[start_row_index + 2][start_col_index: end_col_index]
        ]
        chemical_composition_precision_area = [
            table[start_row_index + 1][start_col_index: end_col_index],
            table[start_row_index + 3][start_col_index: end_col_index]
        ]

        chemical_elements = dict()
        chemical_col_counter = dict()
        for row_index, element_seq in enumerate(chemical_composition_name_area):
            for col_index, cell in enumerate(element_seq):
                if cell is not None and cell.strip() in CommonUtils.chemical_elements_table:
                    chemical_element_name = cell.strip()
                    # get the corresponding precision value
                    chemical_element_precision = chemical_composition_precision_area[row_index][col_index]
                    if chemical_element_precision is None:
                        raise ValueError(
                            f"The corresponding precision value for chemical element {chemical_element_name} could not "
                            f"be found in the given PDF {pdf_file.pdf_path}"
                        )
                    else:
                        chemical_element_precision = chemical_element_precision.strip()
                        if chemical_element_precision.isdigit():
                            chemical_element_precision = int(chemical_element_precision)
                        else:
                            raise ValueError(
                                f"The extracted precision value {chemical_element_precision} for chemical element "
                                f"{chemical_element_name} is not a digit. The given PDF is {pdf_file.pdf_path}"
                            )
                    x_coordinate = start_row_index + row_index * 2
                    y_coordinate = start_col_index + col_index
                    chemical_elements[chemical_element_name] = ChemicalElementName(
                        table_index=table_index,
                        x_coordinate=x_coordinate,
                        y_coordinate=y_coordinate,
                        row_index=row_index,
                        value=chemical_element_name,
                        precision=chemical_element_precision
                    )
                    if start_col_index + col_index in chemical_col_counter:
                        chemical_col_counter[start_col_index + col_index] += 1
                    else:
                        chemical_col_counter[start_col_index + col_index] = 1
        return chemical_elements, chemical_col_counter

    @staticmethod
    def extract_chemical_composition(
        pdf_file: PDFFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate],
        chemical_elements: Dict[str, ChemicalElementName],
        chemical_col_counter: Dict[int, int]
    ):
        # HARD CODE: the information of chemical compositions is always in the second table.
        table_index = 1
        table = pdf_file.tables[table_index]
        # Start extracting the chemical composition values for each plate
        for plate_index in range(len(serial_numbers)):
            # Extract value for each chemical element
            for element in chemical_elements:
                # To locate the cell containing the value for the element, we need to get its x-coordinate
                # which is the x-coordinate of the numbers
                x_coordinate = serial_numbers.x_coordinate
                # y-coordinate is the same of the chemical element name.
                y_coordinate = chemical_elements[element].y_coordinate
                cell = table[x_coordinate][y_coordinate]
                # then we need to locate the index of the digit inside the cell
                idx = chemical_elements[element].row_index + plate_index * chemical_col_counter[y_coordinate]
                chemical_element_value = cell.split('\n')[idx].strip()
                if chemical_element_value.isdigit():
                    chemical_element_value = int(chemical_element_value)
                else:
                    raise ValueError(
                        f"The value {chemical_element_value} extracted for chemical element {element} is not a digit! "
                        f"The given PDF is {pdf_file.pdf_path}"
                    )
                steel_plates[plate_index].chemical_compositions[element] = ChemicalElementValue(
                    table_index=table_index,
                    x_coordinate=x_coordinate,
                    y_coordinate=y_coordinate,
                    value=chemical_element_value,
                    index=idx,
                    valid_flag=True,
                    message=None,
                    element=element,
                    precision=chemical_elements[element].precision
                )

    @staticmethod
    def extract_mass(
        pdf_file: PDFFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate]
    ):
        # To extract the mass value, we need its coordinates.
        # The row index is easy to get, because it is the same with the entity.
        # The col index is the same with the MASS(kg) title.

        # HARD CODE: the information of delivery condition is always in the second table.
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search MASS(kg) to get the col index
        coordinates = CommonUtils.search_table(table, 'MASS(kg)', TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find MASS(kg) title in the given PDF {pdf_file.pdf_path}."
            )

        y_coordinate = coordinates[1]
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        if cell is None or len(cell.strip()) == 0:
            raise ValueError(
                f"Could not find mass value in the given PDF {pdf_file.pdf_path}."
            )

        cell_line_count = len(cell.split('\n'))
        if cell_line_count == len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the mass cell, but there are "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.pdf_path}"
            )
        mass_cell_lines = cell.split('\n')

        # Start extracting the mass value for each plate
        for plate_index in range(len(serial_numbers)):
            mass_value = mass_cell_lines[plate_index]
            if mass_value is not None and len(mass_value.strip()) > 0:
                mass_value = mass_value.strip()
            else:
                raise ValueError(
                    f"Could not find the mass value for plate No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.pdf_path}"
                )
            if mass_value.isdigit():
                mass_value = int(mass_value)
            else:
                raise ValueError(
                    f"The mass value {mass_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a digit in the given "
                    f"PDF {pdf_file.pdf_path}"
                )
            steel_plates[plate_index].mass = Mass(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                index=plate_index,
                value=mass_value
            )

    @staticmethod
    def extract_delivery_condition(
        pdf_file: PDFFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate]
    ):
        # To extract the delivery condition value, we need its coordinates. The row index is easy to get, because
        # it is the same with the entity. The col index is the same with the delivery condition (with Note *9) title.

        # HARD CODE: the information of delivery condition is always in the second table.
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search *9 to get the col index
        coordinates = CommonUtils.search_table(table, '*9')
        if coordinates is None:
            raise ValueError(
                f"Could not find delivery condition (plus *9) title in the given PDF {pdf_file.pdf_path}."
            )

        y_coordinate = coordinates[1]
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        if cell is None or len(cell.strip()) == 0:
            raise ValueError(
                f"Could not find delivery condition value in the given PDF {pdf_file.pdf_path}."
            )

        cell_line_count = len(cell.split('\n'))
        if cell_line_count == len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the delivery condition cell, but there are "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.pdf_path}"
            )
        delivery_condition_cell_lines = cell.split('\n')

        # Start extracting the delivery condition value for each plate
        for plate_index in range(len(serial_numbers)):
            delivery_condition_value = delivery_condition_cell_lines[plate_index]
            if delivery_condition_value is not None and len(delivery_condition_value.strip()) > 0:
                delivery_condition_value = delivery_condition_value.strip()
            else:
                raise ValueError(
                    f"Could not find the delivery condition value for plate No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.pdf_path}"
                )
            if delivery_condition_value.isalpha():
                pass
            else:
                raise ValueError(
                    f"The delivery condition value {delivery_condition_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not purely composed of alphabets in the given "
                    f"PDF {pdf_file.pdf_path}"
                )
            steel_plates[plate_index].delivery_condition = DeliveryCondition(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                index=plate_index,
                value=delivery_condition_value,
                valid_flag=True,
                message=None
            )

    @staticmethod
    def extract_specification(pdf_file: PDFFile) -> Specification:
        # Hardcode here, the specification information is always in the first table:
        table_index = 0
        table = pdf_file.tables[table_index]
        # 遍历这张表格
        coordinates = CommonUtils.search_table(table, 'SPECIFICATION')
        if coordinates is None:
            raise ValueError(
                f"Could not find text 'SPECIFICATION' in the given PDF {pdf_file.pdf_path}."
            )

        # specification的value一般应该在title右边一格
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1] + 1
        specification_value = table[x_coordinate][y_coordinate]
        if specification_value is None:
            # 如果标准值不在对应格子里，则可能是都挤在同列的第一行，用\n分隔
            specification_value = table[0][coordinates[1] + 1].split('\n')[
                coordinates[0]].strip()
        if specification_value is None:
            raise ValueError(
                f"The value of 'SPECIFICATION' could not be found in the given PDF {pdf_file.pdf_path}."
            )
        if specification_value.startswith('DNV GL'):
            pass
        else:
            raise ValueError(
                f"The specification value should start with 'DNV GL', but the value {specification_value} extracted "
                f"from the given PDF {pdf_file.pdf_path} doesn't."
            )
        # TODO Z35 and Z25 plates can not be dealt with at this stage, will be implemented in future versions.
        # For now just raise an exception so that those files of Z35 and Z25 will manually be checked by surveyors.
        if 'Z35' in specification_value or 'Z25' in specification_value:
            raise ValueError(
                f"The specification value contains Z35 or Z25, this kind of certificate can not be automatically "
                f"verified right now, should be manually checked by surveyors."
            )
        # Verify the specification_value by searching the same value in extracted text
        if specification_value in pdf_file.content:
            pass
        else:
            raise ValueError(
                f"The specification value {specification_value} extracted from table could not be found in the "
                f"extracted text, might be wrong."
            )
        # Tailor the value to meet the standard specification type
        specification_value = specification_value.replace('DNV GL', '').strip()
        return Specification(
            table_index=table_index,
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate,
            value=specification_value,
            index=None,
            valid_flag=True,
            message=None
        )

    @staticmethod
    def extract_thickness(pdf_file: PDFFile) -> Thickness:
        # Hard code: the number is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]
        # To get the value of thickness we need to find the cell startswith THICKNESS
        coordinates = CommonUtils.search_table(table, 'THICKNESS', search_type=TableSearchType.SPLIT_LINE_BREAK_START)
        if coordinates is None:
            raise ValueError(
                f"Text 'THICKNESS' could not be found in the given PDF {pdf_file.pdf_path}."
            )
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1]
        thickness_value = table[x_coordinate][y_coordinate].split('\n')[1].strip()
        if len(thickness_value) == 0:
            raise ValueError(
                f"Thickness value could not be found in the Thickness cell."
            )
        try:
            thickness_value = float(thickness_value)
        except ValueError:
            raise ValueError(
                f"The extracted thickness value {thickness_value} could not be converted to a float number."
            )
        return Thickness(
            table_index=table_index,
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate,
            value=thickness_value,
            index=None,
            valid_flag=True,
            message=None
        )

    @staticmethod
    def extract_serial_numbers(pdf_file: PDFFile) -> SerialNumbers:
        # Hard code: the number is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]
        # 通常NO.都应该在[0, 0]的位置上
        coordinates = CommonUtils.search_table(table, 'NO.', confirmed_row=0, confirmed_col=0)
        if coordinates is None:
            raise ValueError(
                f"Text 'NO.' could not be found in the given PDF {pdf_file.pdf_path}."
            )
        # 序号一般都在同一列，但是行数不确定需要遍历
        coordinates = CommonUtils.search_table(table, keyword=None, confirmed_col=0,
                                               search_type=TableSearchType.SPLIT_LINE_BREAK_ALL_DIGIT)
        if coordinates is None:
            raise ValueError(
                f"Could not find NO. value in the given PDF {pdf_file.pdf_path}."
            )
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1]
        serial_numbers = []
        for number_str in table[x_coordinate][y_coordinate].split('\n'):
            number_str_stripped = number_str.strip()
            if number_str_stripped.isdigit():
                serial_numbers.append(int(number_str_stripped))
            else:
                raise ValueError(
                    f"The No. value {number_str_stripped} extracted is not a number in the given "
                    f"PDF {pdf_file.pdf_path}."
                )
        return SerialNumbers(table_index=table_index, x_coordinate=x_coordinate, y_coordinate=y_coordinate,
                             value=serial_numbers)
