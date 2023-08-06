from ..api_and_utils import np, qmc, math


class McPathGenerator:

    def __init__(self, riskfree_rate, dividend, vol, intraday, expiry_date, year_base, path_num=100000,
                 antithetic_flag=True, qmc_flag=True, random_seed=None):
        """

        蒙特卡洛路径生成函数，输出结果为spot价格为1的几何布朗运动
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param vol: 波动率
        :param intraday: 日内时间
        :param expiry_date: 到日期离当前日收盘天数
        :param year_base: 年化日历天数
        :param path_num: 路径数
        :param antithetic_flag: 是否使用对偶变量
        :param qmc_flag: 是否使用quasi-monte carlo，S使用obol低差异化序列
        :param random_seed: 指定随机种子

        e.g.
        intraday = 0.2
        expiry_date = 252
        剩余整数天数为252天，当前日内时间为0.8天，当日剩余天数为0.2天，则剩余到期时间为251.2天。
        生成时间序列为[0, 0.2, 1.2, 2.2, ... 251.2], 长度为253；
        生成时间间隔dt序列为[0.2, 1, 1, 1, ... 1], 长度为252；
        返回长度为253的几何布朗运动，其中第一列是1，为当前时刻价格，后面252列为每个观测日(日终)；
        将返回矩阵乘以当前价格即可得到价格路径。
        """
        self.year_base = float(year_base)
        self.path_num = path_num
        self.antithetic_flag = antithetic_flag
        self.qmc_flag = qmc_flag
        self.random_seed = random_seed

        self.drift = riskfree_rate - dividend - 0.5 * vol ** 2
        self.sigma = vol
        self.t_arr = np.arange(1, expiry_date + 1, 1) - intraday
        self.t_arr = np.hstack([0, self.t_arr])
        self.dt_arr = (self.t_arr[1:] - self.t_arr[:-1]) / self.year_base

    def generate_randn(self, qmc_flag, antithetic_flag, random_seed, M, N):
        """生成标准正态分布随机数矩阵"""
        if qmc_flag:
            _mean_dem = [0] * N
            _qmc_engine = qmc.Sobol(N, seed=random_seed)
            _randn = qmc.MultivariateNormalQMC(mean=_mean_dem, cov=np.eye(len(_mean_dem)), seed=random_seed,
                                               engine=_qmc_engine).random(pow(2, math.ceil(math.log2(M))))
        else:
            np.random.seed(random_seed)
            _randn = np.random.randn(M, N)
        if antithetic_flag:
            _randn = np.vstack([_randn, -_randn])
        return _randn

    def generate(self):
        """生成spot价格为1的几何布朗运动"""
        randn = self.generate_randn(self.qmc_flag, self.antithetic_flag, self.random_seed, self.path_num, len(self.dt_arr))
        log_rtn = self.drift * self.dt_arr + self.sigma * np.sqrt(self.dt_arr) * randn
        cum_log_rtn = np.cumsum(log_rtn, axis=1)
        cum_log_rtn = np.hstack([np.zeros([len(cum_log_rtn), 1]), cum_log_rtn])
        return np.exp(cum_log_rtn)
