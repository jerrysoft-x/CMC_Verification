from dataclasses import dataclass, field
from typing import List, Optional, Dict

import pdfplumber


@dataclass
class CertificateElement:
    table_index: Optional[int]
    x_coordinate: Optional[int]
    y_coordinate: Optional[int]
    value: str


@dataclass
class CertificateElementInPlate(CertificateElement):
    index: Optional[int]


@dataclass
class CertificateElementToVerify(CertificateElementInPlate):
    valid_flag: bool
    message: Optional[str]

    def is_valid(self):
        return self.valid_flag


@dataclass
class Specification(CertificateElementToVerify):
    pass


@dataclass
class SerialNumbers(CertificateElement):
    value: List[int]

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]


@dataclass
class ChemicalElementName(CertificateElement):
    row_index: int
    precision: int


@dataclass
class DeliveryCondition(CertificateElementToVerify):
    pass


@dataclass
class Mass(CertificateElementInPlate):
    value: int


@dataclass
class PositionDirectionImpact(CertificateElementInPlate):
    pass


@dataclass
class PlateNo(CertificateElementInPlate):
    pass


@dataclass
class Thickness(CertificateElementToVerify):
    value: float


@dataclass
class ChemicalElementValue(CertificateElementToVerify):
    value: Optional[int]
    element: str
    precision: Optional[int]
    calculated_value: Optional[float] = field(init=False)

    def __post_init__(self):
        if self.value is None or self.precision is None:
            self.calculated_value = None
        else:
            self.calculated_value = round(self.value * (10 ** -self.precision), self.precision)

    def __str__(self):
        return (
            f"{self.element}(value={self.value}, precision={self.precision}, calculated_value={self.calculated_value})"
        )


@dataclass
class YieldStrength(CertificateElementToVerify):
    value: int


@dataclass
class TensileStrength(CertificateElementToVerify):
    value: int


@dataclass
class Elongation(CertificateElementToVerify):
    value: int


@dataclass
class Temperature(CertificateElementToVerify):
    value: int


@dataclass
class ImpactEnergy(CertificateElementToVerify):
    value: int
    test_number: str


class SteelPlate:

    def __init__(self, serial_number: int):
        self.serial_number: int = serial_number
        self.plate_no: Optional[PlateNo] = None
        self.mass: Optional[Mass] = None
        self.chemical_compositions: Dict[str, ChemicalElementValue] = dict()
        self.yield_strength: Optional[YieldStrength] = None
        self.tensile_strength: Optional[TensileStrength] = None
        self.elongation: Optional[Elongation] = None
        self.position_direction_impact: Optional[PositionDirectionImpact] = None
        self.temperature: Optional[Temperature] = None
        self.impact_energy_list: List[ImpactEnergy] = []
        self.delivery_condition: Optional[DeliveryCondition] = None

    def __str__(self):
        chemical_str = '\n\t\t\t'.join(
            [str(self.chemical_compositions[element]) for element in
             self.chemical_compositions])
        position_direction_str = \
            'None' if self.position_direction_impact is None else self.position_direction_impact.value
        temperature_str = 'None' if self.temperature is None else self.temperature.value
        impact_energy_str = ', '.join(
            ['None' if impact_energy is None else f"{impact_energy.test_number}: {str(impact_energy.value)}" for
             impact_energy in self.impact_energy_list])
        return (
            # f"\tSteel Plate:\n"
            f"\t\tSerial Number: {self.serial_number}\n"
            f"\t\tPlate No.: {self.plate_no}\n"
            f"\t\tMass: {self.mass.value}\n"
            f"\t\tChemical Composition:\n"
            f"\t\t\t{chemical_str}\n"
            f"\t\tYield Strength: {self.yield_strength.value}\n"
            f"\t\tTensile Strength: {self.tensile_strength.value}\n"
            f"\t\tElongation: {self.elongation.value}\n"
            f"\t\tPosition Direction of Impact Test: {position_direction_str}\n"
            f"\t\tTemperature: {temperature_str}\n"
            f"\t\tAbsorbed Energy: {impact_energy_str}\n"
            f"\t\tDelivery Condition: {self.delivery_condition.value}\n"
        )


class PDFFile:

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def __enter__(self):
        self.pdf = pdfplumber.open(self.pdf_path)
        self.page = self.pdf.pages[0]  # Always has only one page
        self.tables = self.page.extract_tables()
        self.content = self.page.extract_text()
        self.steel_plant = self.extract_steel_plant()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pdf:
            self.pdf.close()

    def extract_steel_plant(self):
        if "No.885 Fujin ROAD, BAOSHAN DISTRICT".replace(" ", "").upper() in self.content.replace(" ", "").upper():
            return 'BAOSHAN IRON & STEEL CO., LTD.'
        else:
            raise ValueError(
                f"The steel plant name could not be recognized for the given PDF file {self.pdf_path}."
            )


# @dataclass
# class Certificate:
#     steel_plant: str
#     specification: Specification
#     thickness: Thickness
#     serial_number: SerialNumbers
#     steel_plate: SteelPlate
#     chemical_elements: List[ChemicalElementName]
