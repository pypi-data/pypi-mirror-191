class __PricingMethodEnum:
    """
    定义定价器类型结构体，不可修改其属性值
    AS: 1，Analytical Solution
    MC: 2，Monte Carlo
    PDE: 3, Partial Differential Equation
    """

    @property
    def AS(self) -> int: return 1

    @property
    def MC(self) -> int: return 2

    @property
    def PDE(self) -> int: return 3


class __OptionTypeEnum:
    """
    定义期权类型结构体，不可修改其属性值
    看涨期权: 1
    看跌期权: 2
    累计: 3
    累沽: 4
    标准: 5
    反向: 6
    单触碰: 7
    双向触碰: 8
    """

    @property
    def CALL(self) -> int: return 1

    @property
    def PUT(self) -> int: return 2

    @property
    def ACCUMULATOR(self) -> int: return 3

    @property
    def DECUMULATOR(self) -> int: return 4

    @property
    def STANDARD(self) -> int: return 5

    @property
    def REVERSE(self) -> int: return 6

    @property
    def ONETOUCH(self) -> int: return 7

    @property
    def DOUBLEONETOUCH(self) -> int: return 8


class __ExerciseTypeEnum:
    """
    定义行权类型结构体，不可修改其属性值
    欧式期权: 1
    美式期权: 2
    """

    @property
    def EUROPEAN(self) -> int: return 1

    @property
    def AMERICAN(self) -> int: return 2


class __ObsTypeEnum:
    """
    定义观测类型结构体，不可修改其属性值
    连续观测: 1
    离散观测: 2
    """

    @property
    def CONTINUOUS(self) -> int: return 1

    @property
    def DISCRETE(self) -> int: return 2


class __RebateTypeEnum:
    """
    定义观测类型结构体，不可修改其属性值
    立即支付 PAH: pay at hit 1
    到期支付 PAE: pay at end 2
    """

    @property
    def PAH(self) -> int: return 1

    @property
    def PAE(self) -> int: return 2


class __BarrierTypeEnum:
    """
    定义障碍类型结构体，不可修改其属性值
    向上障碍: 1
    向下障碍: 2
    """

    @property
    def UP(self) -> int: return 1

    @property
    def DOWN(self) -> int: return 2


class __KnockTypeEnum:
    """
    定义障碍敲击类型结构体，不可修改其属性值
    敲入: 1
    敲出: 2
    """

    @property
    def IN(self) -> int: return 1

    @property
    def OUT(self) -> int: return 2


class __AccumulatorTypeEnum:
    """
    累计期权类型
    线性累计: 1
    固定赔付累计: 2
    固定赔付整体敲出累计: 3
    固定赔付(带障碍)累计: 4
    """

    @property
    def LinearAcc(self) -> int: return 1

    @property
    def FixedAcc(self) -> int: return 2

    @property
    def FixedAccAKO(self) -> int: return 3

    @property
    def FixedAccBarrier(self) -> int: return 4


class __InstrumentTypeEnum:

    @property
    def INSTRUMENTTYPE_VANILLA(self) -> int: return 1

    @property
    def INSTRUMENTTYPE_BARRIER(self) -> int: return 2

    @property
    def INSTRUMENTTYPE_BINARY(self) -> int: return 3

    @property
    def INSTRUMENTTYPE_ASIAN(self) -> int: return 4

    @property
    def INSTRUMENTTYPE_SHARKFIN(self) -> int: return 5

    @property
    def INSTRUMENTTYPE_SNOWBALL(self) -> int: return 6


class __ContractTypeEnum:

    @property
    def CONTRACTTYPE_BARRIER(self) -> int: return 1

    @property
    def CONTRACTTYPE_BINARY(self) -> int: return 2

    @property
    def CONTRACTTYPE_ASIAN(self) -> int: return 3

    @property
    def CONTRACTTYPE_LINEAR_ACC(self) -> int: return 4

    @property
    def CONTRACTTYPE_FIXED_ACC(self) -> int: return 5

    @property
    def CONTRACTTYPE_FIXED_ACC_AKO(self) -> int: return 6

    @property
    def CONTRACTTYPE_SNOWBALL(self) -> int: return 7

    @property
    def CONTRACTTYPE_AIRBAG(self) -> int: return 8
    

ObsType = __ObsTypeEnum()
OptionType = __OptionTypeEnum()
ExerciseType = __ExerciseTypeEnum()
BarrierType = __BarrierTypeEnum()
KnockType = __KnockTypeEnum()
RebateType = __RebateTypeEnum()
PricingMethod = __PricingMethodEnum()
AccumulatorType = __AccumulatorTypeEnum()

InstrumentType = __InstrumentTypeEnum()
ContractType = __ContractTypeEnum()
