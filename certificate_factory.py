from typing import List, Dict, Tuple, Optional
from abc import abstractmethod

from certificate_verifier import CertificateVerifier, LongTengCertificateVerifier, BaoSteelCertificateVerifier
from common import PdfFile, Specification, Thickness, SerialNumbers, SteelPlate, ChemicalElementName, \
    DeliveryCondition, Mass, ChemicalElementValue, YieldStrength, TensileStrength, Elongation, \
    PositionDirectionImpact, Temperature, ImpactEnergy, PlateNo, BatchNo, Quantity, CertificateFile, DocxFile, \
    SerialNumber, CommonUtils, TableSearchType, Certificate, SingletonABCMeta, Direction, SteelMakingType
from dataclasses import dataclass

# from certificate_verification import BaoSteelRuleMaker, RuleMaker
from certificate_verification import RuleMaker, BaoSteelRuleMaker, LongTengRuleMaker

# In order to unify the standards between the different steel plants, we have already moved specification and
# thickness to the SteelPlate object. However, for BAOSHAN we still keep them in the certificate (duplication in effect)
# object because the forms BAOSHAN deliver have them in the certificate level, so at first we read them and put them in
# the certificate object, and then copy them to each SteelPlate object (in a way like broadcasting) the certificate
# contains.
from output_utilities.output_excel import write_multiple_certificates_to_excel


@dataclass
class BaoSteelCertificate(Certificate):
    specification: Specification
    thickness: Thickness


# Delivery Condition (Condition of Supply in LongTeng form) is duplicated in certificate object, because the value is
# provided in the certificate level, we will read it and put it in the certificate object, and then copy it to each
# SteelPlate object (in a way like broadcasting) the certificate contains.
@dataclass
class LongTengCertificate(Certificate):
    delivery_condition: Optional[DeliveryCondition]


# Here the term of factory is not related to the steel plant, it is purely the concept of Factory Method design pattern.
# The pattern improves the code loosely coupled for better maintainability and extensibility.
# This class contains the factory method act as the creator of the certificates, and it must be instantiated by
# subclasses dedicated for each steel plant respectively.
class CertificateFactory(metaclass=SingletonABCMeta):

    @abstractmethod
    def read(self, file: CertificateFile) -> List[Certificate]:
        pass

    @abstractmethod
    def get_rule_maker(self) -> RuleMaker:
        pass

    @abstractmethod
    def get_verifier(self) -> CertificateVerifier:
        pass


class LongTengCertificateFactory(CertificateFactory):

    def get_rule_maker(self) -> LongTengRuleMaker:
        return LongTengRuleMaker()

    def get_verifier(self) -> LongTengCertificateVerifier:
        return LongTengCertificateVerifier()

    def read(self, file: DocxFile) -> List[LongTengCertificate]:
        certificate_list = []
        for cert_index, table in enumerate(file.tables):
            certificate_no = self.extract_certificate_no(file.file_path, cert_index, table)
            delivery_condition = self.extract_delivery_condition(file.file_path, cert_index, table)
            serial_numbers = self.extract_serial_numbers(file.file_path, cert_index, table)
            chemical_elements = self.extract_chemical_elements(file.file_path, cert_index, table)
            steel_plates = self.extract_steel_plates(file.file_path, cert_index, table, serial_numbers,
                                                     delivery_condition, chemical_elements)
            certificate_list.append(
                LongTengCertificate(
                    file_path=file.file_path,
                    steel_plant=file.steel_plant,
                    certificate_no=certificate_no,
                    serial_numbers=serial_numbers,
                    steel_plates=steel_plates,
                    chemical_elements=chemical_elements,
                    delivery_condition=delivery_condition
                )
            )
        return certificate_list

    @staticmethod
    def extract_certificate_no(file_path: str, cert_index: int, table: List[List[str]]):
        # 遍历这张表格
        coordinates = CommonUtils.search_table(table, '质保书编号', TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find text '质保书编号' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx "
                f"file {file_path}."
            )
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1]
        certificate_no_value = table[x_coordinate][y_coordinate]
        if certificate_no_value is None:
            raise ValueError(
                f"The value of '质保书编号' could not be found in the {CommonUtils.ordinal(cert_index + 1)} table in the "
                f"given docx file {file_path}"
            )
        return certificate_no_value.replace('质保书编号：', '').replace('Certificate No.', '').strip()

    @staticmethod
    def extract_delivery_condition(file_path: str, cert_index: int, table: List[List[str]]):
        coordinates = CommonUtils.search_table(table, "交货状态：热轧\nCondition of Supply: As Rolled",
                                               TableSearchType.EXACT_MATCH)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'Condition of Supply' in the {CommonUtils.ordinal(cert_index + 1)} table in the given "
                f"docx file {file_path}"
            )
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1]
        # If no exception here, the delivery condition value (Condition of Supply) is hardcoded in all the certificates
        # as "As Rolled", corresponding to the "AR".
        delivery_condition = 'AR'
        return DeliveryCondition(
            table_index=cert_index,
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate,
            index=None,
            message=None,
            valid_flag=True,
            value=delivery_condition
        )

    @staticmethod
    def extract_serial_numbers(file_path: str, cert_index: int, table: List[List[str]]):
        coordinates = CommonUtils.search_table(table, '冶炼炉号', TableSearchType.REMOVE_LINE_BREAK_CONTAIN,
                                               confirmed_col=0)
        if coordinates is None:
            raise ValueError(
                f"Could not find '冶炼炉号' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file "
                f"{file_path}"
            )
        start_row_index = coordinates[0]
        coordinates = CommonUtils.search_table(table, '冶炼炉号', TableSearchType.REMOVE_LINE_BREAK_CONTAIN,
                                               confirmed_row=start_row_index + 2, confirmed_col=0)
        if coordinates is None:
            raise ValueError(
                f"The cell of '冶炼炉号' doesn't span three rows, this might be caused by the table layout being "
                f"changed by the steel plant provider Long Teng."
            )
        # print(f"start row index == {start_row_index}")
        coordinates = CommonUtils.search_table(table, '验船师签字:', TableSearchType.SPLIT_LINE_BREAK_START)
        if coordinates is None:
            raise ValueError(
                f"Could not find '验船师签字:' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file "
                f"{file_path}"
            )
        end_row_index = coordinates[0]
        # print(f"end row index == {end_row_index}")
        serial_number_list = []
        row_cursor = start_row_index + 2  # This is the last row contains '冶炼炉号', this cell spans three row.
        current_index = 0
        while (row_cursor := row_cursor + 1) < end_row_index:
            # print(f"current cursor = {row_cursor}")
            if len(table[row_cursor][0].strip()) > 0:
                serial_number_list.append(SerialNumber(
                    table_index=cert_index,
                    x_coordinate=row_cursor,
                    y_coordinate=0,
                    value=(current_index := current_index + 1)
                ))
                # print(f"cell content is {table[row_cursor][0]}")
                # print(f"got serial number {current_index}")
        return SerialNumbers(
            table_index=cert_index,
            x_coordinate=start_row_index + 1,
            y_coordinate=0,
            value=serial_number_list
        )

    @staticmethod
    def extract_chemical_elements(file_path: str, cert_index: int, table: List[List[str]]):
        # To locate the chemical element area
        # the row index of the line is the next to the line contains "Chemical Composition"
        # and the column index span from the first catch "Chemical Composition" until "Mechanical Properties"
        coordinates = CommonUtils.search_table(table, 'Chemical Composition', TableSearchType.SPLIT_LINE_BREAK_END)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'Chemical Composition' in the {CommonUtils.ordinal(cert_index + 1)} table in the "
                f"given docx file {file_path}"
            )
        chemical_elements_row_index = coordinates[0] + 1
        chemical_elements_column_start_index = coordinates[1]
        coordinates = CommonUtils.search_table(table, 'Mechanical Properties', TableSearchType.SPLIT_LINE_BREAK_END)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'Mechanical Properties' in the {CommonUtils.ordinal(cert_index + 1)} table in the "
                f"given docx file {file_path}"
            )
        chemical_elements_column_end_index = coordinates[1]
        column_cursor = chemical_elements_column_start_index - 1
        chemical_elements = dict()
        while (column_cursor := column_cursor + 1) < chemical_elements_column_end_index:
            cell = table[chemical_elements_row_index][column_cursor].strip()
            if cell in CommonUtils.chemical_elements_table:
                if cell not in chemical_elements:
                    chemical_elements[cell] = ChemicalElementName(
                        table_index=cert_index,
                        x_coordinate=chemical_elements_row_index,
                        y_coordinate=column_cursor,
                        value=cell,
                        row_index=chemical_elements_row_index,
                        precision=0  # No precision setting in LongTeng certificate
                    )
        return chemical_elements

    @staticmethod
    def extract_steel_plates(file_path: str, cert_index: int, table: List[List[str]], serial_numbers: SerialNumbers,
                             delivery_condition: DeliveryCondition, chemical_elements: Dict[str, ChemicalElementName]):
        steel_plate_list = []
        for serial_number in serial_numbers:
            plate = SteelPlate(serial_number)
            plate.delivery_condition = delivery_condition
            steel_plate_list.append(plate)
        LongTengCertificateFactory.extract_batch_no(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_plate_no(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_specification(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_thickness(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_quantity(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_mass(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_chemical_compositions(file_path, cert_index, table, steel_plate_list,
                                                                 chemical_elements)
        LongTengCertificateFactory.extract_yield_strength(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_tensile_strength(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_elongation(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_position_direction_impact(cert_index, steel_plate_list)
        LongTengCertificateFactory.extract_temperature(file_path, cert_index, table, steel_plate_list)
        LongTengCertificateFactory.extract_impact_energy_list(file_path, cert_index, table, steel_plate_list)
        return steel_plate_list

    # Steel Making Type value is embedded in the batch-no value:
    # D1 D2 代表电炉冶炼 EAF (Electric arc furnace) EAF B1 B2代表转炉冶炼 BOC (Basic oxygen converter)
    @staticmethod
    def extract_batch_no(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate]):
        # To get the column index of the Batch No. cell
        coordinates = CommonUtils.search_table(table, 'Batch No.', TableSearchType.SPLIT_LINE_BREAK_END)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'Batch No.' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file "
                f"{file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            batch_no_value = table[x_coordinate][y_coordinate].strip()
            if len(batch_no_value) == 0:
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for 'Batch No.' in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            plate.batch_no = BatchNo(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=batch_no_value,
                index=plate_index
            )
            # set the steel making type value here. (this is a bit special since the value is embedded in batch-no)
            if batch_no_value.startswith('D1') or batch_no_value.startswith('D2'):
                plate.steel_making_type = SteelMakingType(
                    table_index=cert_index,
                    x_coordinate=x_coordinate,
                    y_coordinate=y_coordinate,
                    value='EAF, CC',
                    index=plate_index
                )
            elif batch_no_value.startswith('B1') or batch_no_value.startswith('B2'):
                plate.steel_making_type = SteelMakingType(
                    table_index=cert_index,
                    x_coordinate=x_coordinate,
                    y_coordinate=y_coordinate,
                    value='BOC, CC',
                    index=plate_index
                )
            else:
                raise ValueError(
                    f"The batch no. value {batch_no_value} is invalid "
                    f"in the {CommonUtils.ordinal(plate.serial_number.value)} plate in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}, "
                    f"the expected value should start with 'D1', 'D2', 'B1' and 'B2'."
                )

    @staticmethod
    def extract_plate_no(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate]):
        # To get the column index of the Roll No. cell
        coordinates = CommonUtils.search_table(table, 'Roll No.', TableSearchType.SPLIT_LINE_BREAK_END)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'Roll No.' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file "
                f"{file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            roll_no_value = table[x_coordinate][y_coordinate].strip()
            if len(roll_no_value) == 0:
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for 'Roll No.' in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            plate.plate_no = PlateNo(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=roll_no_value,
                index=plate_index
            )

    @staticmethod
    def extract_specification(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate]):
        # To get the column index of the Grade cell
        coordinates = CommonUtils.search_table(table, 'Grade', TableSearchType.SPLIT_LINE_BREAK_END)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'Grade' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file "
                f"{file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            grade_value = table[x_coordinate][y_coordinate].strip()
            if len(grade_value) == 0:
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for 'Grade' in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            plate.specification = Specification(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=grade_value,
                index=plate_index,
                message=None,
                valid_flag=True
            )

    @staticmethod
    def extract_thickness(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate]):
        # To get the column index of the Dimensions cell
        coordinates = CommonUtils.search_table(table, 'Dimensions', TableSearchType.SPLIT_LINE_BREAK_END)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'Dimensions' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file"
                f" {file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            dimensions_value = table[x_coordinate][y_coordinate].strip()
            if len(dimensions_value) == 0:
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for 'Dimensions' in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            thickness_value = dimensions_value.split('×')[-1].strip()
            if thickness_value.isdigit():
                thickness_value = float(thickness_value)
            else:
                raise ValueError(
                    f"The last dimension value {thickness_value} in the Dimensions value {dimensions_value} isn't a "
                    f"digit in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            plate.thickness = Thickness(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=thickness_value,
                index=plate_index,
                message=None,
                valid_flag=True
            )

    @staticmethod
    def extract_quantity(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate]):
        # To get the column index of the PCS cell
        coordinates = CommonUtils.search_table(table, 'PCS', TableSearchType.SPLIT_LINE_BREAK_END)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'PCS' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file "
                f"{file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            pcs_value = table[x_coordinate][y_coordinate].strip()
            if len(pcs_value) == 0:
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for 'PCS' in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            if pcs_value.isdigit():
                pcs_value = int(pcs_value)
            else:
                raise ValueError(
                    f"The PCS value {pcs_value} isn't a "
                    f"digit in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            plate.quantity = Quantity(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=pcs_value,
                index=plate_index
            )

    @staticmethod
    def extract_mass(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate]):
        # To get the column index of the Weight cell
        coordinates = CommonUtils.search_table(table, '重量Weight(t)', TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'Weight' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file "
                f"{file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            weight_value = table[x_coordinate][y_coordinate].strip()
            if len(weight_value) == 0:
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for 'Weight' in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            try:
                weight_value = float(weight_value)
            except ValueError:
                raise ValueError(
                    f"The Weight value {weight_value} isn't a "
                    f"float in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            plate.mass = Mass(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=weight_value,
                index=plate_index
            )

    @staticmethod
    def extract_chemical_compositions(file_path: str, cert_index: int, table: List[List[str]],
                                      steel_plates: List[SteelPlate],
                                      chemical_elements: Dict[str, ChemicalElementName]):
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            chemical_compositions = dict()
            for element in chemical_elements:
                y_coordinate = chemical_elements[element].y_coordinate
                element_value = table[x_coordinate][y_coordinate].strip()
                if len(element_value) == 0:
                    raise ValueError(
                        f"The cell [{x_coordinate}, {y_coordinate}] in the "
                        f"{CommonUtils.ordinal(plate.serial_number.value)} plate has no value for chemical element "
                        f"{element} in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file "
                        f"{file_path}"
                    )
                try:
                    element_value = float(element_value.replace('≤', ''))
                except ValueError:
                    raise ValueError(
                        f"The value of chemical element {element} {element_value} isn't a "
                        f"float in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                    )
                chemical_compositions[element] = ChemicalElementValue(
                    table_index=cert_index,
                    x_coordinate=x_coordinate,
                    y_coordinate=y_coordinate,
                    value=element_value,
                    index=plate_index,
                    valid_flag=True,
                    message=None,
                    element=element,
                    precision=chemical_elements[element].precision
                )
            ###################################################
            # Temporary solution hardcode Mo and Ti
            chemical_compositions['Mo'] = ChemicalElementValue(
                table_index=cert_index,
                x_coordinate=None,
                y_coordinate=None,
                value=0.02,
                index=plate_index,
                valid_flag=True,
                message=None,
                element='Mo',
                precision=0
            )
            chemical_compositions['Ti'] = ChemicalElementValue(
                table_index=cert_index,
                x_coordinate=None,
                y_coordinate=None,
                value=0.02,
                index=plate_index,
                valid_flag=True,
                message=None,
                element='Ti',
                precision=0
            )
            ###########################################################
            plate.chemical_compositions = chemical_compositions
            # print(
            #     f"{{'C': {chemical_compositions['C'].calculated_value}, "
            #     f"'Si': {chemical_compositions['Si'].calculated_value}, "
            #     f"'Mn': {chemical_compositions['Mn'].calculated_value}, "
            #     f"'P': {chemical_compositions['P'].calculated_value}, "
            #     f"'S': {chemical_compositions['S'].calculated_value}, "
            #     f"'Ni': {chemical_compositions['Ni'].calculated_value}, "
            #     f"'Cr': {chemical_compositions['Cr'].calculated_value}, "
            #     f"'Cu': {chemical_compositions['Cu'].calculated_value}, "
            #     f"'V': {chemical_compositions['V'].calculated_value}, "
            #     f"'Al': {chemical_compositions['Al'].calculated_value}, "
            #     f"'Nb': {chemical_compositions['Nb'].calculated_value}, "
            #     f"'Ceq': {chemical_compositions['Ceq'].calculated_value}}},"
            # )

    @staticmethod
    def extract_yield_strength(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate]):
        # To get the column index of the 屈服强度 cell
        coordinates = CommonUtils.search_table(table, '屈服强度', TableSearchType.SPLIT_LINE_BREAK_START)
        if coordinates is None:
            raise ValueError(
                f"Could not find '屈服强度' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx "
                f"file {file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            yield_strength_value = table[x_coordinate][y_coordinate].strip()
            if len(yield_strength_value) == 0:
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for '屈服强度' in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            try:
                yield_strength_value = int(yield_strength_value)
            except ValueError:
                raise ValueError(
                    f"The 屈服强度 value {yield_strength_value} isn't an "
                    f"integer in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            plate.yield_strength = YieldStrength(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=yield_strength_value,
                index=plate_index,
                valid_flag=True,
                message=None
            )

    @staticmethod
    def extract_tensile_strength(file_path: str, cert_index: int, table: List[List[str]],
                                 steel_plates: List[SteelPlate]):
        # To get the column index of the 抗拉强度 cell
        coordinates = CommonUtils.search_table(table, '抗拉强度', TableSearchType.SPLIT_LINE_BREAK_START)
        if coordinates is None:
            raise ValueError(
                f"Could not find '抗拉强度' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx "
                f"file {file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            tensile_strength_value = table[x_coordinate][y_coordinate].strip()
            if len(tensile_strength_value) == 0:
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for '抗拉强度' in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            try:
                tensile_strength_value = int(tensile_strength_value)
            except ValueError:
                raise ValueError(
                    f"The 抗拉强度 value {tensile_strength_value} isn't an "
                    f"integer in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            plate.tensile_strength = TensileStrength(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=tensile_strength_value,
                index=plate_index,
                valid_flag=True,
                message=None
            )

    @staticmethod
    def extract_elongation(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate]):
        # To get the column index of the 抗拉强度 cell
        coordinates = CommonUtils.search_table(table, '伸长率', TableSearchType.SPLIT_LINE_BREAK_START)
        if coordinates is None:
            raise ValueError(
                f"Could not find '伸长率' in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx "
                f"file {file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            elongation_value = table[x_coordinate][y_coordinate].strip()
            if len(elongation_value) == 0:
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for '伸长率' in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            try:
                elongation_value = int(elongation_value)
            except ValueError:
                raise ValueError(
                    f"The 伸长率 value {elongation_value} isn't an "
                    f"integer in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            plate.elongation = Elongation(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=elongation_value,
                index=plate_index,
                valid_flag=True,
                message=None
            )

    @staticmethod
    def extract_position_direction_impact(cert_index: int, steel_plates: List[SteelPlate]):
        # Longteng's steel plates are all longitudinal by default
        for plate_index, plate in enumerate(steel_plates):
            plate.position_direction_impact = PositionDirectionImpact(
                table_index=cert_index,
                x_coordinate=None,
                y_coordinate=None,
                value=Direction.LONGITUDINAL,
                index=plate_index
            )

    @staticmethod
    def extract_temperature(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate]):
        # Temperature is hardcoded as 0 degree in the impact title in longteng certificate
        coordinates = CommonUtils.search_table(table, 'V型冲击功 (J, 0℃)\nCharpy V-notch Impact',
                                               TableSearchType.EXACT_MATCH)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'V型冲击功 (J, 0℃)' in the {CommonUtils.ordinal(cert_index + 1)} table in the given "
                f"docx file {file_path}"
            )
        y_coordinate = coordinates[1]
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            temperature_value = 0  # hardcode value as described in the form title.
            plate.temperature = Temperature(
                table_index=cert_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=temperature_value,
                index=plate_index,
                valid_flag=True,
                message=None
            )

    @staticmethod
    def extract_impact_energy_list(file_path: str, cert_index: int, table: List[List[str]],
                                   steel_plates: List[SteelPlate]):
        # Get the coordinates of the Impact title cell
        coordinates = CommonUtils.search_table(table, 'V型冲击功 (J, 0℃)\nCharpy V-notch Impact',
                                               TableSearchType.EXACT_MATCH)
        if coordinates is None:
            raise ValueError(
                f"Could not find 'V型冲击功 (J, 0℃)' in the {CommonUtils.ordinal(cert_index + 1)} table in the given "
                f"docx file {file_path}"
            )
        x_coordinate = coordinates[0] + 1
        y_coordinate = coordinates[1]
        expected_title_values = ['1', '2', '3', 'Avg']
        for title_index, title_value in enumerate(expected_title_values):
            LongTengCertificateFactory.extract_impact_energy(file_path, cert_index, table, steel_plates, title_value,
                                                             x_coordinate, y_coordinate + title_index)
        # print(
        #     [[impact_energy.value for impact_energy in plate.impact_energy_list] for plate in steel_plates]
        # )

    @staticmethod
    def extract_impact_energy(file_path: str, cert_index: int, table: List[List[str]], steel_plates: List[SteelPlate],
                              expected_title_value: str, expected_title_x_coordinate: int,
                              expected_title_y_coordinate: int):
        # To confirm the existence of the expected title cell
        coordinates = CommonUtils.search_table(table, expected_title_value, TableSearchType.EXACT_MATCH,
                                               confirmed_row=expected_title_x_coordinate,
                                               confirmed_col=expected_title_y_coordinate)
        if coordinates is None:
            raise ValueError(
                f"Could not find sub title '{expected_title_value}' of the impact energy section in the "
                f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
            )
        y_coordinate = expected_title_y_coordinate
        for plate_index, plate in enumerate(steel_plates):
            x_coordinate = plate.serial_number.x_coordinate
            impact_energy_value = table[x_coordinate][y_coordinate].strip()
            if len(impact_energy_value) == 0:
                ########################################################
                # under below conditions, impact energy values are not required
                if plate.specification.value == 'VL A':
                    if plate.thickness.value <= 50:
                        continue
                    elif plate.delivery_condition.value == 'N':
                        continue
                if plate.specification.value == 'VL B':
                    if plate.thickness.value <= 25:
                        continue
                #########################################################
                raise ValueError(
                    f"The cell [{x_coordinate}, {y_coordinate}] in the {CommonUtils.ordinal(plate.serial_number.value)}"
                    f" plate has no value for impact energy {expected_title_value} in the "
                    f"{CommonUtils.ordinal(cert_index + 1)} table in the given docx file {file_path}"
                )
            try:
                impact_energy_value = int(impact_energy_value)
            except ValueError:
                raise ValueError(
                    f"The impact energy value {impact_energy_value} (in the cell [{x_coordinate}, {y_coordinate}] ) "
                    f"isn't an integer in the {CommonUtils.ordinal(cert_index + 1)} table in the given docx file "
                    f"{file_path}"
                )
            plate.impact_energy_list.append(
                ImpactEnergy(
                    table_index=cert_index,
                    x_coordinate=x_coordinate,
                    y_coordinate=y_coordinate,
                    value=impact_energy_value,
                    index=plate_index,
                    test_number=expected_title_value,
                    valid_flag=True,
                    message=None
                )
            )


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

    def get_rule_maker(self) -> BaoSteelRuleMaker:
        return BaoSteelRuleMaker()

    def get_verifier(self) -> BaoSteelCertificateVerifier:
        return BaoSteelCertificateVerifier()

    def read(self, file: PdfFile) -> List[Certificate]:
        certificate_no = BaoSteelCertificateFactory.extract_certificate_no(file)
        specification = BaoSteelCertificateFactory.extract_specification(file)
        thickness = BaoSteelCertificateFactory.extract_thickness(file)
        serial_numbers = BaoSteelCertificateFactory.extract_serial_numbers(file)
        chemical_elements, chemical_col_counter = BaoSteelCertificateFactory.extract_chemical_elements(file)
        non_test_lot_no_map = BaoSteelCertificateFactory.generate_non_test_lot_no_map(file, serial_numbers)
        # "Test Lot No" is something interrupting the extraction of position direction value, we need a mapping to help
        # skipping the Test Lot No values.
        steel_plates = BaoSteelCertificateFactory.extract_steel_plates(
            pdf_file=file,
            specification=specification,
            thickness=thickness,
            serial_numbers=serial_numbers,
            chemical_elements=chemical_elements,
            chemical_col_counter=chemical_col_counter,
            non_test_lot_no_map=non_test_lot_no_map
        )
        certificate = BaoSteelCertificate(
            file_path=file.file_path,
            steel_plant=file.steel_plant,
            certificate_no=certificate_no,
            specification=specification,
            thickness=thickness,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates,
            chemical_elements=chemical_elements
        )
        return [certificate]

    @staticmethod
    def generate_non_test_lot_no_map(pdf_file: PdfFile, serial_numbers: SerialNumbers) -> Dict[int, int]:
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
        pdf_file: PdfFile,
        specification: Specification,
        thickness: Thickness,
        serial_numbers: SerialNumbers,
        chemical_elements: Dict[str, ChemicalElementName],
        chemical_col_counter: Dict[int, int],
        non_test_lot_no_map: Dict[int, int]
    ) -> List[SteelPlate]:
        steel_plates = []
        for serial_number in serial_numbers:
            plate = SteelPlate(serial_number)
            plate.specification = specification
            plate.thickness = thickness
            steel_plates.append(plate)
        BaoSteelCertificateFactory.extract_quantity(
            pdf_file=pdf_file,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates
        )
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
        BaoSteelCertificateFactory.extract_batch_no(
            pdf_file=pdf_file,
            serial_numbers=serial_numbers,
            steel_plates=steel_plates,
            non_test_lot_no_map=non_test_lot_no_map
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

    @staticmethod
    def extract_position_direction_impact(
            pdf_file: PdfFile,
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
                f"Could not find IMPACT TEST title in the given PDF {pdf_file.file_path}."
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
                f"the serial numbers count {len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
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
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                )
            if position_direction_value == 'None':
                continue
            elif position_direction_value.isalnum():
                pass
            else:
                raise ValueError(
                    f"The position direction (impact test) value {position_direction_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} contains invalid character other than alphabet and "
                    f"number in the given PDF {pdf_file.file_path}"
                )
            steel_plates[plate_index].position_direction_impact = PositionDirectionImpact(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                index=plate_index,
                value=BaoSteelCertificateFactory.translate_to_vl_direction(position_direction_value)
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
            pdf_file: PdfFile,
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
                f"Could not find TEMP (Temperature) title in the given PDF {pdf_file.file_path}."
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
        #         f"the serial numbers count {len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
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
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
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
                    f"in the given PDF {pdf_file.file_path}"
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
        pdf_file: PdfFile,
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
                f"Could not find ABSORBED ENERGY title in the given PDF {pdf_file.file_path}."
            )
        start_col = coordinates[1]

        # Search the title OC to locate the x coordinate of the first test title.
        coordinates = CommonUtils.search_table(table, 'OC', search_type=TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find OC title in the given PDF {pdf_file.file_path}."
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
                pdf_path=pdf_file.file_path
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
            #         f"the serial numbers count {len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
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
                        f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                    )
                if impact_energy_value == 'None':
                    continue
                elif impact_energy_value.isdigit():
                    impact_energy_value = int(impact_energy_value)
                else:
                    raise ValueError(
                        f"The impact energy value {impact_energy_value} extracted for plate No. "
                        f"{serial_numbers[plate_index]} is not a number "
                        f"in the given PDF {pdf_file.file_path}"
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
        pdf_file: PdfFile,
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
                f"Could not find PLATE NO. title in the given PDF {pdf_file.file_path}."
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
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
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
                    f"Could not find the Plate No. value for No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                )
            steel_plates[plate_index].plate_no = PlateNo(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=plate_no_value,
                index=plate_index
            )

    @staticmethod
    def extract_batch_no(
        pdf_file: PdfFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate],
        non_test_lot_no_map: Dict[int, int]
    ):
        # Firstly, hardcode that HEAT NO. data is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search the title HEAT NO. to locate the y coordinate
        coordinates = CommonUtils.search_table(table, 'HEATNO.', TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find HEAT NO. title in the given PDF {pdf_file.file_path}."
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
                f"There are {cell_line_count} lines in the HEAT NO. cell, less than the serial numbers count "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
            )
        heat_no_cell_lines = cell.split('\n')

        # Start extracting the HEAT NO. value for each plate
        for plate_index in range(len(serial_numbers)):
            if len(heat_no_cell_lines) > len(serial_numbers):
                heat_no_value = heat_no_cell_lines[non_test_lot_no_map[plate_index]]
            else:
                heat_no_value = heat_no_cell_lines[plate_index]
            if heat_no_value is not None and len(heat_no_value.strip()) > 0:
                heat_no_value = heat_no_value.strip()
            else:
                raise ValueError(
                    f"Could not find the HEAT NO. value for No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                )
            steel_plates[plate_index].batch_no = BatchNo(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                value=heat_no_value,
                index=plate_index
            )

    @staticmethod
    def extract_yield_strength(
        pdf_file: PdfFile,
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
                f"Could not find Y.S. (Yield Strength) title in the given PDF {pdf_file.file_path}."
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
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
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
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                )
            if yield_strength_value.isdigit():
                yield_strength_value = int(yield_strength_value)
                pass
            else:
                raise ValueError(
                    f"The yield strength value {yield_strength_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a number in the given "
                    f"PDF {pdf_file.file_path}"
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
        pdf_file: PdfFile,
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
                f"Could not find T.S. (Tensile Strength) title in the given PDF {pdf_file.file_path}."
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
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
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
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                )
            if tensile_strength_value.isdigit():
                tensile_strength_value = int(tensile_strength_value)
                pass
            else:
                raise ValueError(
                    f"The tensile strength value {tensile_strength_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a number in the given "
                    f"PDF {pdf_file.file_path}"
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
        pdf_file: PdfFile,
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
                f"Could not find EL (Elongation) title in the given PDF {pdf_file.file_path}."
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
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
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
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                )
            if elongation_value.isdigit():
                elongation_value = int(elongation_value)
                pass
            else:
                raise ValueError(
                    f"The elongation value {elongation_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a number in the given "
                    f"PDF {pdf_file.file_path}"
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
    def extract_chemical_elements(pdf_file: PdfFile) -> Tuple[Dict[str, ChemicalElementName], Dict[int, int]]:
        # HARD CODE: the information of chemical compositions is always in the second table.
        table_index = 1
        table = pdf_file.tables[table_index]

        # To locate the positions of the chemical composition cells, we need to find the row with both Notes *1 and *3
        # The chemical composition area starts at that row for 4 rows, and the columns are between the two notes.

        # Search Note '*1'
        coordinates = CommonUtils.search_table(table, '*1')
        if coordinates is None:
            raise ValueError(
                f"Could not find text '*1' in the given PDF {pdf_file.file_path}"
            )
        # If *1 is found, we can determine the index of the first row, and the columns start from the next column.
        start_row_index = coordinates[0]
        start_col_index = coordinates[1] + 1
        # If *1 is found, we need to check if *3 is at the same row,
        # so that we can determine the right boundary of the columns.
        coordinates = CommonUtils.search_table(table, '*3', confirmed_row=start_row_index)
        if coordinates is None:
            raise ValueError(
                f"Could not find text '*3' in the given PDF {pdf_file.file_path}"
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
                            f"be found in the given PDF {pdf_file.file_path}"
                        )
                    else:
                        chemical_element_precision = chemical_element_precision.strip()
                        if chemical_element_precision.isdigit():
                            chemical_element_precision = int(chemical_element_precision)
                        else:
                            raise ValueError(
                                f"The extracted precision value {chemical_element_precision} for chemical element "
                                f"{chemical_element_name} is not a digit. The given PDF is {pdf_file.file_path}"
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
        pdf_file: PdfFile,
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
                        f"The given PDF is {pdf_file.file_path}"
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
    def extract_quantity(
        pdf_file: PdfFile,
        serial_numbers: SerialNumbers,
        steel_plates: List[SteelPlate]
    ):
        # To extract the quantity value, we need its coordinates.
        # The row index is easy to get, because it is the same with the entity.
        # The col index is the same with the QYT title.

        # HARD CODE: the information of delivery condition is always in the second table.
        table_index = 1
        table = pdf_file.tables[table_index]

        # Search QTY to get the col index
        coordinates = CommonUtils.search_table(table, 'QTY', TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find QTY title in the given PDF {pdf_file.file_path}."
            )

        y_coordinate = coordinates[1]
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        if cell is None or len(cell.strip()) == 0:
            raise ValueError(
                f"Could not find QTY value in the given PDF {pdf_file.file_path}."
            )

        cell_line_count = len(cell.split('\n'))
        if cell_line_count == len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the QTY cell, but there are "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
            )
        qty_cell_lines = cell.split('\n')

        # Start extracting the mass value for each plate
        for plate_index in range(len(serial_numbers)):
            qty_value = qty_cell_lines[plate_index]
            if qty_value is not None and len(qty_value.strip()) > 0:
                qty_value = qty_value.strip()
            else:
                raise ValueError(
                    f"Could not find the QTY value for plate No. "
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                )
            if qty_value.isdigit():
                qty_value = int(qty_value)
            else:
                raise ValueError(
                    f"The QTY value {qty_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a digit in the given "
                    f"PDF {pdf_file.file_path}"
                )
            steel_plates[plate_index].quantity = Quantity(
                table_index=table_index,
                x_coordinate=x_coordinate,
                y_coordinate=y_coordinate,
                index=plate_index,
                value=qty_value
            )

    @staticmethod
    def extract_mass(
        pdf_file: PdfFile,
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
                f"Could not find MASS(kg) title in the given PDF {pdf_file.file_path}."
            )

        y_coordinate = coordinates[1]
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        if cell is None or len(cell.strip()) == 0:
            raise ValueError(
                f"Could not find mass value in the given PDF {pdf_file.file_path}."
            )

        cell_line_count = len(cell.split('\n'))
        if cell_line_count == len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the mass cell, but there are "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
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
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                )
            if mass_value.isdigit():
                mass_value = int(mass_value) / 1000  # convert to tons
            else:
                raise ValueError(
                    f"The mass value {mass_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not a digit in the given "
                    f"PDF {pdf_file.file_path}"
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
        pdf_file: PdfFile,
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
                f"Could not find delivery condition (plus *9) title in the given PDF {pdf_file.file_path}."
            )

        y_coordinate = coordinates[1]
        x_coordinate = serial_numbers.x_coordinate

        cell = table[x_coordinate][y_coordinate]

        if cell is None or len(cell.strip()) == 0:
            raise ValueError(
                f"Could not find delivery condition value in the given PDF {pdf_file.file_path}."
            )

        cell_line_count = len(cell.split('\n'))
        if cell_line_count == len(serial_numbers):
            pass
        else:
            raise ValueError(
                f"There are {cell_line_count} lines in the delivery condition cell, but there are "
                f"{len(serial_numbers)} plates in the given PDF {pdf_file.file_path}"
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
                    f"{serial_numbers[plate_index]} in the given PDF {pdf_file.file_path}"
                )
            if delivery_condition_value.isalpha():
                pass
            else:
                raise ValueError(
                    f"The delivery condition value {delivery_condition_value} extracted for plate No. "
                    f"{serial_numbers[plate_index]} is not purely composed of alphabets in the given "
                    f"PDF {pdf_file.file_path}"
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
    def extract_specification(pdf_file: PdfFile) -> Specification:
        # Hardcode here, the specification information is always in the first table:
        table_index = 0
        table = pdf_file.tables[table_index]
        # 遍历这张表格
        coordinates = CommonUtils.search_table(table, 'SPECIFICATION')
        if coordinates is None:
            raise ValueError(
                f"Could not find text 'SPECIFICATION' in the given PDF {pdf_file.file_path}."
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
                f"The value of 'SPECIFICATION' could not be found in the given PDF {pdf_file.file_path}."
            )
        if specification_value.startswith('DNV GL'):
            pass
        else:
            raise ValueError(
                f"The specification value should start with 'DNV GL', but the value {specification_value} extracted "
                f"from the given PDF {pdf_file.file_path} doesn't."
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
    def extract_certificate_no(pdf_file: PdfFile) -> str:
        # Hardcode here, the specification information is always in the first table:
        table_index = 0
        table = pdf_file.tables[table_index]
        # 遍历这张表格
        coordinates = CommonUtils.search_table(table, 'CERTIFICATENO.',
                                               search_type=TableSearchType.REMOVE_LINE_BREAK_CONTAIN)
        if coordinates is None:
            raise ValueError(
                f"Could not find text 'CERTIFICATE NO.' in the given PDF {pdf_file.file_path}."
            )

        # specification的value一般应该在title右边一格
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1] + 1
        certificate_no_value = table[x_coordinate][y_coordinate]
        if certificate_no_value is None:
            raise ValueError(
                f"The value of 'CERTIFICATE NO.' could not be found in the given PDF {pdf_file.file_path}."
            )
        return certificate_no_value.strip()

    @staticmethod
    def extract_thickness(pdf_file: PdfFile) -> Thickness:
        # Hard code: the number is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]
        # To get the value of thickness we need to find the cell startswith THICKNESS
        coordinates = CommonUtils.search_table(table, 'THICKNESS', search_type=TableSearchType.SPLIT_LINE_BREAK_START)
        if coordinates is None:
            raise ValueError(
                f"Text 'THICKNESS' could not be found in the given PDF {pdf_file.file_path}."
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
        if thickness_value < 0:
            raise ValueError(
                f"The extracted thickness value {thickness_value} is negative, and not expected."
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
    def extract_serial_numbers(pdf_file: PdfFile) -> SerialNumbers:
        # Hard code: the number is always in the second table
        table_index = 1
        table = pdf_file.tables[table_index]
        # 通常NO.都应该在[0, 0]的位置上
        coordinates = CommonUtils.search_table(table, 'NO.', confirmed_row=0, confirmed_col=0)
        if coordinates is None:
            raise ValueError(
                f"Text 'NO.' could not be found in the given PDF {pdf_file.file_path}."
            )
        # 序号一般都在同一列，但是行数不确定需要遍历
        coordinates = CommonUtils.search_table(table, keyword=None, confirmed_col=0,
                                               search_type=TableSearchType.SPLIT_LINE_BREAK_ALL_DIGIT)
        if coordinates is None:
            raise ValueError(
                f"Could not find NO. value in the given PDF {pdf_file.file_path}."
            )
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1]
        serial_numbers = []
        for number_str in table[x_coordinate][y_coordinate].split('\n'):
            number_str_stripped = number_str.strip()
            if number_str_stripped.isdigit():
                serial_numbers.append(SerialNumber(
                    table_index=table_index,
                    x_coordinate=x_coordinate,
                    y_coordinate=y_coordinate,
                    value=int(number_str_stripped)
                ))
            else:
                raise ValueError(
                    f"The No. value {number_str_stripped} extracted is not a number in the given "
                    f"PDF {pdf_file.file_path}."
                )
        return SerialNumbers(table_index=table_index, x_coordinate=x_coordinate, y_coordinate=y_coordinate,
                             value=serial_numbers)


class CertificateFactoryRegister:

    def __init__(self):
        self._factories = {}

    def register_factory(self, steel_plant: str, certificate_factory: CertificateFactory) -> None:
        self._factories[steel_plant] = certificate_factory

    def get_factory(self, steel_plant: str) -> CertificateFactory:
        certificate_factory = self._factories.get(steel_plant)
        if not certificate_factory:
            raise ValueError(f"The certificate factory supporting steel plant {steel_plant} has not been registered.")
        return certificate_factory


if __name__ == '__main__':
    test_file = r'C:\Users\jjli\Documents\CloudStation\Lab\Python\Work\Maritime\Document\DNVGL质保书样本.docx'
    with DocxFile(test_file) as docx_file:
        factory = LongTengCertificateFactory()
        certificates = factory.read(docx_file)
        write_multiple_certificates_to_excel(certificates)
