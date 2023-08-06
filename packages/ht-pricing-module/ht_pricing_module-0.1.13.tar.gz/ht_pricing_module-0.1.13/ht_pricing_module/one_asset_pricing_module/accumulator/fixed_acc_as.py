from ..one_asset_option_base import *
from ..vanilla import Vanilla
from ..binary import Binary


class FixedAcc(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        rst = 0

        vanilla_option_type = {OptionType.ACCUMULATOR: OptionType.PUT,
                               OptionType.DECUMULATOR: OptionType.CALL}[self.param.option_type]
        binary_option_type = {OptionType.ACCUMULATOR: OptionType.CALL,
                              OptionType.DECUMULATOR: OptionType.PUT}[self.param.option_type]

        for obs in self.param.obs_date:
            param = Struct({})
            param['option_type'] = vanilla_option_type
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['expiry_date'] = obs.obs_index
            param['current_date'] = self.param.current_date
            param['volatility'] = self.param.volatility
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['year_base'] = int(self.param.year_base)
            vanilla = Vanilla(param)

            param = Struct({})
            param['option_type'] = binary_option_type
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['expiry_date'] = obs.obs_index
            param['current_date'] = self.param.current_date
            param['volatility'] = self.param.volatility
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['payoff'] = self.param.payoff
            param['year_base'] = int(self.param.year_base)
            binary = Binary(param)
            rst = rst + (-self.param.leverage * vanilla.present_value() + binary.present_value())
        return rst
