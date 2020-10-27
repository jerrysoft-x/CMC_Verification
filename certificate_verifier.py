import os
import shutil
# import pickle
from typing import List, Tuple

from certificate_element import PDFFile, CertificateElementToVerify, ChemicalElementValue
from certificate_factory import BaoSteelCertificateFactory, CertificateFactory
from certificate_verification import RuleMaker
from common_utils import Certificate
from output_utilities.output_excel import write_single_certificate_to_excel, write_multiple_certificates_to_excel, \
    write_certificates_with_exception


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


class CertificateVerifier:
    @staticmethod
    def verify(cert: Certificate, rule_maker: RuleMaker) -> bool:
        all_valid_flag = True
        for steel_plate_index in range(len(cert.serial_numbers)):
            print(f"Checking Steel Plate No. {cert.steel_plates[steel_plate_index].serial_number}:")
            limit_list = rule_maker.get_rules(cert, steel_plate_index)
            for limit in limit_list:
                certificate_element = limit.get_element(cert, steel_plate_index)
                if isinstance(certificate_element, CertificateElementToVerify):
                    if isinstance(certificate_element, ChemicalElementValue):
                        certificate_element.valid_flag, certificate_element.message = limit.verify(
                            certificate_element.calculated_value)
                    else:
                        certificate_element.valid_flag, certificate_element.message = limit.verify(
                            certificate_element.value)
                    all_valid_flag = all_valid_flag and certificate_element.valid_flag
                else:
                    pass_flag, _ = limit.verify(certificate_element)
                    all_valid_flag = all_valid_flag and pass_flag
            fine_grain_elements_limit_list = rule_maker.get_fine_grain_elements_rules(cert, steel_plate_index)
            if not cert.specification.valid_flag:
                print(cert.specification.message)
            if not cert.thickness.valid_flag:
                print(cert.thickness.message)
            if not cert.steel_plates[steel_plate_index].delivery_condition.valid_flag:
                print(cert.steel_plates[steel_plate_index].delivery_condition.message)
            if len(fine_grain_elements_limit_list) > 0:
                print(
                    f"Eligible fine grain element combinations are ["
                    f"{', '.join([str(limit) for limit in fine_grain_elements_limit_list])}]."
                )
            fine_grain_elements_valid_flag = False
            for limit in fine_grain_elements_limit_list:
                certificate_element = limit.get_element(cert, steel_plate_index)
                pass_flag, _ = limit.verify(certificate_element)
                if pass_flag:
                    fine_grain_elements_valid_flag = True
                    break
            if not fine_grain_elements_valid_flag:
                CertificateVerifier.update_fine_grain_elements(cert, steel_plate_index, 'Alt')
                CertificateVerifier.update_fine_grain_elements(cert, steel_plate_index, 'Als')
                CertificateVerifier.update_fine_grain_elements(cert, steel_plate_index, 'Ti')
                CertificateVerifier.update_fine_grain_elements(cert, steel_plate_index, 'Nb')
                all_valid_flag = False
        return all_valid_flag

    @staticmethod
    def update_fine_grain_elements(cert: Certificate, steel_plate_index: int, element: str):
        chemical_composition = cert.steel_plates[steel_plate_index].chemical_compositions
        error_message = (
            f"Fine Grain Elements don't meet the requirements of Specification {cert.specification.value} "
            f"and Delivery Condition {cert.steel_plates[steel_plate_index].delivery_condition.value} and "
            f"Thickness {cert.thickness.value}."
        )
        if element in chemical_composition:
            chemical_composition[element].valid_flag = False
            chemical_composition[element].message = error_message
        else:
            chemical_composition[element] = ChemicalElementValue(
                table_index=1,
                x_coordinate=None,
                y_coordinate=None,
                value=None,
                index=steel_plate_index,
                valid_flag=False,
                message=error_message,
                element=element,
                precision=None
            )


if __name__ == '__main__':
    register = CertificateFactoryRegister()
    register.register_factory(steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
                              certificate_factory=BaoSteelCertificateFactory())

    # Print the current working directory
    print(os.getcwd())
    # List the pdf files and subdirectories in the working directory
    pdf_files = []
    subdirectories = []
    with os.scandir() as it:
        for entry in it:
            if entry.is_file() and entry.name.lower().endswith('.pdf'):
                pdf_files.append(entry.name)
            if entry.is_dir():
                subdirectories.append(entry.name)

    # create the destination folders if they don't exist
    if 'PASS' not in subdirectories:
        os.mkdir('PASS')
    if 'FAIL' not in subdirectories:
        os.mkdir('FAIL')
    if 'EXCEPTION' not in subdirectories:
        os.mkdir('EXCEPTION')

    passed_certificates: List[Certificate] = []
    certificates_with_exception: List[Tuple[str, str]] = []
    # Iterate the pdf files, read each pdf file and verify, and distribute the files to respective destination folders.
    for file in pdf_files:
        print(f"\n\nProcessing file {file} ...")
        certificate = None
        try:
            with PDFFile(file) as pdf_file:
                factory = register.get_factory(steel_plant=pdf_file.steel_plant)
                certificate = factory.read(pdf_file=pdf_file)
            print(certificate)
            valid_flag = CertificateVerifier.verify(certificate, factory.get_rule_maker())
            # with open(file.replace('.pdf', '.pickle'), 'wb') as f:
            #     pickle.dump(certificate, f)
            if valid_flag:
                print(f"Verification Pass!")
                shutil.copy(file, 'PASS')
                # os.remove is used instead of shutil.move because of compatibility problem with pyinstaller
                os.remove(file)
                passed_certificates.append(certificate)
            else:
                print(f"Verification Fail!")
                shutil.copy(file, 'FAIL')
                # os.remove is used instead of shutil.move because of compatibility problem with pyinstaller
                os.remove(file)
                write_single_certificate_to_excel(
                    certificate=certificate,
                    sheet_name='FAIL',
                    output_file=os.path.join('FAIL', file.replace('.pdf', '.xlsx'))
                )
        except Exception as e:
            print(f"Exception occurred during reading the PDF file!")
            print(e)
            shutil.copy(file, 'EXCEPTION')
            # os.remove is used instead of shutil.move because of compatibility problem with pyinstaller
            os.remove(file)
            # with open(os.path.join('EXCEPTION', file.replace('.pdf', '.txt')), 'w') as f:
            #     f.write(str(e))
            certificates_with_exception.append((file, str(e)))
    write_multiple_certificates_to_excel(passed_certificates)
    write_certificates_with_exception(certificates_with_exception)
    # input(f"Click enter or close button to finish...")
