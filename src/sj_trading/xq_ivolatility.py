# xq_ivolatility.py
# Rebuild XQ XS IVolatility function in Python
# Author: (you can put your name here)

import math
from dataclasses import dataclass
from scipy.stats import norm


@dataclass
class XQIVolatility:
    """
    XQ-style Implied Volatility calculator
    IV unit: percentage (e.g. 20 = 20%)
    """

    @staticmethod
    def bs_price(
        call_put_flag: str,
        spot: float,
        strike: float,
        d_to_m: float,
        rate_100: float,
        b_100: float,
        vol_100: float
    ) -> float:
        """
        Black-Scholes price
        All rates & vol are in percentage form (XQ style)
        """
        # Convert units
        T = d_to_m / 365.0
        r = rate_100 / 100.0
        b = b_100 / 100.0
        sigma = vol_100 / 100.0

        if T <= 0 or sigma <= 0:
            return 0.0

        d1 = (
            math.log(spot / strike)
            + (b + 0.5 * sigma ** 2) * T
        ) / (sigma * math.sqrt(T))

        d2 = d1 - sigma * math.sqrt(T)

        if call_put_flag.upper() == "C":
            price = (
                spot * math.exp((b - r) * T) * norm.cdf(d1)
                - strike * math.exp(-r * T) * norm.cdf(d2)
            )
        elif call_put_flag.upper() == "P":
            price = (
                strike * math.exp(-r * T) * norm.cdf(-d2)
                - spot * math.exp((b - r) * T) * norm.cdf(-d1)
            )
        else:
            raise ValueError("call_put_flag must be 'C' or 'P'")

        return price

    @classmethod
    def ivolatility(
        cls,
        call_put_flag: str,
        spot_price: float,
        strike_price: float,
        d_to_m: float,
        rate_100: float,
        b_100: float,
        option_price: float
    ) -> float:
        """
        XQ XS-style IVolatility
        """

        # === condition1 ===
        if d_to_m <= 0 or strike_price <= 0 or spot_price <= 0:
            return 0.0

        var1 = 100.0  # initial IV
        var2 = cls.bs_price(
            call_put_flag,
            spot_price,
            strike_price,
            d_to_m,
            rate_100,
            b_100,
            var1
        )

        # === coarse search ===
        while var2 < option_price and var1 <= 900:
            var1 += 100.0
            var2 = cls.bs_price(
                call_put_flag,
                spot_price,
                strike_price,
                d_to_m,
                rate_100,
                b_100,
                var1
            )

        if var2 < option_price:
            return 999.0

        # === fine tuning ===
        var3 = 1
        var4 = 100.0

        while abs(var2 - option_price) >= 0.005 and var3 < 11:
            var4 *= 0.5

            if var2 > option_price:
                var1 -= var4
            elif var2 < option_price:
                var1 += var4

            var2 = cls.bs_price(
                call_put_flag,
                spot_price,
                strike_price,
                d_to_m,
                rate_100,
                b_100,
                var1
            )
            var3 += 1

        return var1
