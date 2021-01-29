from typing import List, Union, Tuple

from certificate_verification import LimitType, ChemicalCompositionLimit, ThicknessLimit, SpecificationLimit, \
    YieldStrengthLimit, TensileStrengthLimit, ElongationLimit, TemperatureLimit, ImpactEnergyLimit, \
    DeliveryConditionLimit, FineGrainElementLimitCombination, BaoSteelAlLimit, FineGrainElementLimit
from common import Limit, SteelPlate, Direction


class BaseTester:

    @staticmethod
    def reset_chemical_composition(
            plate: SteelPlate,
            chemical_element: str,
            value: float,
            precision: int = None
    ):
        if chemical_element in plate.chemical_compositions:
            if precision:
                plate.chemical_compositions[chemical_element].set_value_and_precision(
                    value=value,
                    precision=precision
                )
            else:
                plate.chemical_compositions[chemical_element].set_value(value)
            plate.chemical_compositions[chemical_element].valid_flag = True
            plate.chemical_compositions[chemical_element].message = None
        else:
            raise ValueError(
                f"The input chemical element {chemical_element} has not been initialized in the steel plate yet."
            )

    @staticmethod
    def get_limit(
            limit_list: List[Limit],
            limit_class: str,
            limit_type: LimitType,
            chemical_element: str = None,
            maximum: float = None,
            minimum: float = None,
            scope: Union[List[str], Tuple[Direction, Direction]] = None
    ):
        hit_limits = []
        for limit in limit_list:
            # check if the limit class name match
            if limit.__class__.__name__ == limit_class:
                pass
            else:
                continue
            # if limit is ChemicalCompositionLimit, check the value of chemical element
            if isinstance(limit, ChemicalCompositionLimit):
                # check if limit type match
                if limit.limit_type == limit_type:
                    pass
                else:
                    continue
                if limit.chemical_element == chemical_element:
                    pass
                else:
                    continue
                if limit.limit_type == LimitType.MAXIMUM and limit.maximum == maximum:
                    pass
                elif limit.limit_type == LimitType.MINIMUM and limit.minimum == minimum:
                    pass
                elif limit.limit_type == LimitType.RANGE and limit.maximum == maximum and limit.minimum == minimum:
                    pass
                else:
                    continue
            elif isinstance(limit, ThicknessLimit):
                if limit.limit_type == limit_type:
                    pass
                else:
                    continue
                if limit.limit_type == LimitType.RANGE and limit.maximum == maximum and limit.minimum == minimum:
                    pass
                else:
                    continue
            elif isinstance(limit, SpecificationLimit):
                if limit.limit_type == limit_type:
                    pass
                else:
                    continue
                if limit.limit_type == LimitType.SCOPE and BaseTester.match_scope(limit.scope, scope):
                    pass
                else:
                    continue
            elif isinstance(limit, DeliveryConditionLimit):
                if limit.limit_type == limit_type:
                    pass
                else:
                    continue
                if limit.limit_type == LimitType.SCOPE and BaseTester.match_scope(limit.scope, scope):
                    pass
                else:
                    continue
            elif isinstance(limit, YieldStrengthLimit):
                if limit.limit_type == limit_type:
                    pass
                else:
                    continue
                if limit.limit_type == LimitType.MINIMUM and limit.minimum == minimum:
                    pass
                else:
                    continue
            elif isinstance(limit, TensileStrengthLimit):
                if limit.limit_type == limit_type:
                    pass
                else:
                    continue
                if limit.limit_type == LimitType.RANGE and limit.minimum == minimum and limit.maximum == maximum:
                    pass
                else:
                    continue
            elif isinstance(limit, ElongationLimit):
                if limit.limit_type == limit_type:
                    pass
                else:
                    continue
                if limit.limit_type == LimitType.MINIMUM and limit.minimum == minimum:
                    pass
                else:
                    continue
            elif isinstance(limit, TemperatureLimit):
                if limit.limit_type == limit_type:
                    pass
                else:
                    continue
                if limit.limit_type == LimitType.MAXIMUM and limit.maximum == maximum:
                    pass
                else:
                    continue
            elif isinstance(limit, ImpactEnergyLimit):
                if limit.limit_type == limit_type:
                    pass
                else:
                    continue
                if limit.limit_type == LimitType.MINIMUM and limit.minimum == minimum:
                    pass
                else:
                    continue

            hit_limits.append(limit)
        assert len(hit_limits) == 1
        return hit_limits[0]

    @staticmethod
    def check_fine_grain_element_combiantion(
            limit_list: List[Limit],
            steel_plant: str,
            strength: str,
            include: List[str]
    ):
        assert steel_plant == 'BAOSHAN IRON & STEEL CO., LTD.'
        hit_combinations = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_combinations) == 1
        combination = hit_combinations[0]
        fgel_list = [fgel for fgel in combination.fine_grain_element_limits if isinstance(fgel, FineGrainElementLimit)]
        assert len(include) == len(fgel_list)
        for key in include:
            # print(key)
            hit_fgel = [fgel for fgel in fgel_list if
                        BaseTester.is_fine_grain_element_limit(fgel, steel_plant, strength, key)]
            # print(len(hit_fgel))
            assert len(hit_fgel) == 1

    @staticmethod
    def is_fine_grain_element_limit(
            fgel: FineGrainElementLimit,
            steel_plant: str,
            strength: str,
            key: str
    ) -> bool:
        if steel_plant == 'BAOSHAN IRON & STEEL CO., LTD.':
            if strength == 'normal':
                if key == 'Al':
                    if len(fgel.concurrent_limits) == 1:
                        al_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, BaoSteelAlLimit)
                            and limit.alt_limit.chemical_element == 'Alt'
                            and limit.alt_limit.limit_type == LimitType.MINIMUM
                            and limit.alt_limit.minimum == 0.020
                            and limit.als_limit.chemical_element == 'Als'
                            and limit.als_limit.limit_type == LimitType.MINIMUM
                            and limit.als_limit.minimum == 0.015
                        ]
                        if len(al_limits) == 1:
                            return True
                elif key == 'Al+Ti':
                    if len(fgel.concurrent_limits) == 2:
                        # Al
                        al_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, BaoSteelAlLimit)
                            and limit.alt_limit.chemical_element == 'Alt'
                            and limit.alt_limit.limit_type == LimitType.MINIMUM
                            and limit.alt_limit.minimum == 0.015
                            and limit.als_limit.chemical_element == 'Als'
                            and limit.als_limit.limit_type == LimitType.MINIMUM
                            and limit.als_limit.minimum == 0.010
                        ]
                        # Ti
                        ti_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Ti'
                            and limit.limit_type == LimitType.MINIMUM
                            and limit.minimum == 0.007
                        ]
                        if len(al_limits) == 1 and len(ti_limits) == 1:
                            return True
                elif key == 'Al+Nb':
                    if len(fgel.concurrent_limits) == 2:
                        # Al
                        al_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, BaoSteelAlLimit)
                            and limit.alt_limit.chemical_element == 'Alt'
                            and limit.alt_limit.limit_type == LimitType.MINIMUM
                            and limit.alt_limit.minimum == 0.015
                            and limit.als_limit.chemical_element == 'Als'
                            and limit.als_limit.limit_type == LimitType.MINIMUM
                            and limit.als_limit.minimum == 0.010
                        ]
                        # Nb
                        nb_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Nb'
                            and limit.limit_type == LimitType.MINIMUM
                            and limit.minimum == 0.010
                        ]
                        if len(al_limits) == 1 and len(nb_limits) == 1:
                            return True
                elif key == 'Al+Nb+Ti':
                    if len(fgel.concurrent_limits) == 3:
                        # Al
                        al_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, BaoSteelAlLimit)
                            and limit.alt_limit.chemical_element == 'Alt'
                            and limit.alt_limit.limit_type == LimitType.MINIMUM
                            and limit.alt_limit.minimum == 0.015
                            and limit.als_limit.chemical_element == 'Als'
                            and limit.als_limit.limit_type == LimitType.MINIMUM
                            and limit.als_limit.minimum == 0.010
                        ]
                        # Nb
                        nb_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Nb'
                            and limit.limit_type == LimitType.MINIMUM
                            and limit.minimum == 0.010
                        ]
                        # Ti
                        ti_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Ti'
                            and limit.limit_type == LimitType.MINIMUM
                            and limit.minimum == 0.007
                        ]
                        if len(al_limits) == 1 and len(nb_limits) == 1 and len(ti_limits) == 1:
                            return True
                else:
                    raise ValueError(
                        f"The input key value {key} is not expected. (strength: {strength}, steel_plant: {steel_plant})"
                    )
            elif strength == 'high':
                if key == 'Al+Ti':
                    if len(fgel.concurrent_limits) == 2:
                        # Al
                        al_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, BaoSteelAlLimit)
                            and limit.alt_limit.chemical_element == 'Alt'
                            and limit.alt_limit.limit_type == LimitType.MINIMUM
                            and limit.alt_limit.minimum == 0.015
                            and limit.als_limit.chemical_element == 'Als'
                            and limit.als_limit.limit_type == LimitType.MINIMUM
                            and limit.als_limit.minimum == 0.010
                        ]
                        # Ti
                        ti_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Ti'
                            and limit.limit_type == LimitType.RANGE
                            and limit.minimum == 0.007
                            and limit.maximum == 0.02
                        ]
                        if len(al_limits) == 1 and len(ti_limits) == 1:
                            return True
                elif key == 'Al+Nb+Ti':
                    if len(fgel.concurrent_limits) == 3:
                        # Al
                        al_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, BaoSteelAlLimit)
                            and limit.alt_limit.chemical_element == 'Alt'
                            and limit.alt_limit.limit_type == LimitType.MINIMUM
                            and limit.alt_limit.minimum == 0.015
                            and limit.als_limit.chemical_element == 'Als'
                            and limit.als_limit.limit_type == LimitType.MINIMUM
                            and limit.als_limit.minimum == 0.010
                        ]
                        # Nb
                        nb_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Nb'
                            and limit.limit_type == LimitType.RANGE
                            and limit.minimum == 0.010
                            and limit.maximum == 0.05
                        ]
                        # Ti
                        ti_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Ti'
                            and limit.limit_type == LimitType.RANGE
                            and limit.minimum == 0.007
                            and limit.maximum == 0.02
                        ]
                        if len(al_limits) == 1 and len(nb_limits) == 1 and len(ti_limits) == 1:
                            return True
                elif key == 'Al+Nb+Ti+V':
                    if len(fgel.concurrent_limits) == 5:
                        # Al
                        al_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, BaoSteelAlLimit)
                            and limit.alt_limit.chemical_element == 'Alt'
                            and limit.alt_limit.limit_type == LimitType.MINIMUM
                            and limit.alt_limit.minimum == 0.015
                            and limit.als_limit.chemical_element == 'Als'
                            and limit.als_limit.limit_type == LimitType.MINIMUM
                            and limit.als_limit.minimum == 0.010
                        ]
                        # Nb
                        nb_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Nb'
                            and limit.limit_type == LimitType.RANGE
                            and limit.minimum == 0.010
                            and limit.maximum == 0.05
                        ]
                        # Ti
                        ti_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Ti'
                            and limit.limit_type == LimitType.RANGE
                            and limit.minimum == 0.007
                            and limit.maximum == 0.02
                        ]
                        # V
                        v_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'V'
                            and limit.limit_type == LimitType.RANGE
                            and limit.minimum == 0.03
                            and limit.maximum == 0.10
                        ]
                        # Nb+V+Ti
                        nb_v_ti_limits = [
                            limit for limit in fgel.concurrent_limits
                            if isinstance(limit, ChemicalCompositionLimit)
                            and limit.chemical_element == 'Nb + V + Ti'
                            and limit.limit_type == LimitType.MAXIMUM
                            and limit.maximum == 0.12
                        ]
                        if len(al_limits) == 1 and len(nb_limits) == 1 and len(ti_limits) == 1 and len(
                                v_limits) == 1 and len(nb_v_ti_limits) == 1:
                            return True
                else:
                    raise ValueError(
                        f"The input key value {key} is not expected. (strength: {strength}, steel_plant: {steel_plant})"
                    )
            else:
                raise ValueError(
                    f"The input strength value {strength} is not expected. (steel_plant: {steel_plant})"
                )
        else:
            raise ValueError(
                f"The input steel plant value {steel_plant} is not expected."
            )
        return False

    @staticmethod
    def match_scope(left_scope, right_scope) -> bool:
        if len(left_scope) == len(right_scope):
            if all([elem in right_scope for elem in left_scope]):
                return True
        return False


# if __name__ == '__main__':
#     print(BaseTester.match_scope(['AR', 'N'], ['N', 'AR']))
