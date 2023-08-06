from ..one_asset_option_base import *
from ..barrier.discrete_barrier_as import DiscreteBarrierAs
from ..barrier.discrete_barrier_binary_as import DiscreteBarrierBinary


class FixedAccAKO(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        rst = 0

        barrier_option_type = {OptionType.ACCUMULATOR: OptionType.PUT,
                               OptionType.DECUMULATOR: OptionType.CALL}[self.param.option_type]
        barrier_binary_option_type = {OptionType.ACCUMULATOR: OptionType.CALL,
                                      OptionType.DECUMULATOR: OptionType.PUT}[self.param.option_type]

        barrier_type = {OptionType.ACCUMULATOR: BarrierType.UP,
                        OptionType.DECUMULATOR: BarrierType.DOWN}[self.param.option_type]

        for obs in self.param.obs_date:
            param = Struct({})
            param['option_type'] = barrier_option_type
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['barrier_price'] = self.param.barrier_price
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['volatility'] = self.param.volatility
            param['expiry_date'] = obs.obs_index
            param['current_date'] = self.param.current_date
            param['year_base'] = int(self.param.year_base)
            param['barrier_type'] = barrier_type
            param['knock_type'] = KnockType.OUT
            param['is_knock_in'] = 0
            param['rebate'] = 0
            param['obs_freq'] = self.param.obs_freq
            barrier = DiscreteBarrierAs(param)

            param = Struct({})
            param['option_type'] = barrier_binary_option_type
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['barrier_price'] = self.param.barrier_price
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['volatility'] = self.param.volatility
            param['expiry_date'] = obs.obs_index
            param['current_date'] = self.param.current_date
            param['year_base'] = int(self.param.year_base)
            param['barrier_type'] = barrier_type
            param['knock_type'] = KnockType.OUT
            param['is_knock_in'] = 0
            param['payoff'] = self.param.payoff
            param['obs_freq'] = self.param.obs_freq
            barrier_binary = DiscreteBarrierBinary(param)
            rst = rst + (-self.param.leverage * barrier.present_value() + barrier_binary.present_value())
        return rst
