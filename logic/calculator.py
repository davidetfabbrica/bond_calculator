# logic/calculator.py
# ---------------------------------------------------------------
# This module contains all financial calculation logic.
# It has no knowledge of the UI - it just receives inputs,
# performs calculations, and returns results.
# ---------------------------------------------------------------

from scipy.optimize import brentq  # Numerical solver for YTM
from datetime import date


def calculate_ytm(face_value: float,
                  coupon_rate: float,
                  market_price: float,
                  settlement_date: date,
                  maturity_date: date,
                  coupon_frequency: int = 2) -> float:
    """
    Calculate the Yield to Maturity (YTM) for a bond or UK gilt.

    YTM is the single discount rate that makes the present value of all
    future cash flows (coupons + face value repayment) equal to the
    bond's current market price.

    Parameters:
    -----------
    face_value      : The nominal/par value of the bond (e.g. 100.0 for a gilt)
    coupon_rate     : Annual coupon rate as a percentage (e.g. 4.5 for 4.5%)
    market_price    : Current market price of the bond (e.g. 97.50)
    settlement_date : The date the bond is purchased (usually today)
    maturity_date   : The date the bond matures and face value is repaid
    coupon_frequency: Number of coupon payments per year (2 = semi-annual, UK standard)

    Returns:
    --------
    ytm : float — the annualised YTM as a percentage (e.g. 4.82)

    Raises:
    -------
    ValueError if inputs are invalid or the solver cannot converge.
    """

    # --- Input Validation ---
    if face_value <= 0:
        raise ValueError("Face value must be greater than zero.")
    if market_price <= 0:
        raise ValueError("Market price must be greater than zero.")
    if not (0 < coupon_rate < 100):
        raise ValueError("Coupon rate must be between 0 and 100.")
    if maturity_date <= settlement_date:
        raise ValueError("Maturity date must be after the settlement date.")
    if coupon_frequency not in [1, 2, 4]:
        raise ValueError("Coupon frequency must be 1 (annual), 2 (semi-annual), or 4 (quarterly).")

    # --- Derived values ---
    # Annual coupon payment in £
    annual_coupon = face_value * (coupon_rate / 100)

    # Payment per period (e.g. every 6 months for semi-annual)
    coupon_per_period = annual_coupon / coupon_frequency

    # Total number of days from settlement to maturity
    total_days = (maturity_date - settlement_date).days

    # Number of full coupon periods remaining
    # We calculate this based on actual days for accuracy
    days_per_period = 365.25 / coupon_frequency
    num_periods = total_days / days_per_period

    # --- Define the price function ---
    # This function calculates what the bond SHOULD be worth
    # given a particular yield (y). We want to find the y that
    # makes this equal to market_price.
    def bond_price(y):
        """
        Calculate theoretical bond price for a given periodic yield y.
        Sums the present value of all future cash flows.
        """
        price = 0.0

        # Add present value of each coupon payment
        for t in range(1, int(num_periods) + 1):
            price += coupon_per_period / ((1 + y) ** t)

        # Handle fractional last period (accrued time to next coupon)
        fractional = num_periods - int(num_periods)
        if fractional > 0:
            price += coupon_per_period / ((1 + y) ** num_periods)

        # Add present value of face value repayment at maturity
        price += face_value / ((1 + y) ** num_periods)

        return price

    # --- Solve for YTM using Brent's method ---
    # brentq finds the root of a function within a bracket [a, b].
    # We want bond_price(y) - market_price = 0, so we solve for y.
    # The yield is bracketed between near-zero and 100% (sensible range).
    try:
        periodic_ytm = brentq(
            lambda y: bond_price(y) - market_price,
            a=0.0001,   # lower bound: near 0%
            b=0.9999,   # upper bound: near 100%
            xtol=1e-10  # tolerance: extremely precise
        )
    except ValueError:
        raise ValueError(
            "Could not calculate YTM. Please check your inputs — "
            "the price may be inconsistent with the coupon and maturity."
        )

    # Convert periodic yield to annualised percentage
    annual_ytm = periodic_ytm * coupon_frequency * 100

    return round(annual_ytm, 4)


def calculate_investment_returns(face_value: float,
                                 coupon_rate: float,
                                 market_price: float,
                                 settlement_date: date,
                                 maturity_date: date,
                                 investment_amount: float,
                                 coupon_frequency: int = 2) -> dict:
    """
    Calculate projected returns for a given investment amount in a bond.

    Parameters:
    -----------
    face_value        : Nominal/par value per bond (e.g. 100.0)
    coupon_rate       : Annual coupon rate as a percentage
    market_price      : Current market price per bond
    settlement_date   : Purchase date
    maturity_date     : Maturity date
    investment_amount : Total amount the investor wishes to invest (£)
    coupon_frequency  : Coupon payments per year (default 2 = semi-annual)

    Returns:
    --------
    dict containing:
        - bonds_purchased       : number of bonds bought
        - actual_invested       : actual £ spent (may differ slightly from input)
        - coupon_per_period     : £ received each coupon payment
        - annual_coupon_income  : total £ coupon income per year
        - total_coupon_income   : total £ coupon income over full term
        - capital_gain_loss     : £ gain or loss at maturity vs purchase price
        - total_return_gbp      : total £ return (coupons + capital)
        - total_return_pct      : total return as a percentage of amount invested
        - ytm                   : YTM % for reference
        - yearly_breakdown      : list of dicts showing cumulative income by year
    """

    # --- Input Validation ---
    if investment_amount <= 0:
        raise ValueError("Investment amount must be greater than zero.")

    # Calculate how many whole bonds can be purchased
    # Bonds are typically traded in £100 face value units for gilts
    bonds_purchased = int(investment_amount / market_price)

    if bonds_purchased < 1:
        raise ValueError(
            f"Investment amount of £{investment_amount:,.2f} is insufficient "
            f"to purchase even one bond at £{market_price:.2f}."
        )

    # Actual amount spent (whole bonds only — you can't buy a fraction)
    actual_invested = bonds_purchased * market_price

    # Total face value held at maturity
    total_face_value = bonds_purchased * face_value

    # Coupon calculations
    annual_coupon_per_bond = face_value * (coupon_rate / 100)
    coupon_per_period_per_bond = annual_coupon_per_bond / coupon_frequency

    total_annual_coupon = annual_coupon_per_bond * bonds_purchased
    total_coupon_per_period = coupon_per_period_per_bond * bonds_purchased

    # Number of years to maturity (approximate for display purposes)
    years_to_maturity = (maturity_date - settlement_date).days / 365.25

    # Total coupon income over the full term
    total_periods = years_to_maturity * coupon_frequency
    total_coupon_income = total_coupon_per_period * total_periods

    # Capital gain or loss at maturity
    # If you bought below face value, you gain the difference at maturity
    capital_gain_loss = total_face_value - actual_invested

    # Total return in £ and %
    total_return_gbp = total_coupon_income + capital_gain_loss
    total_return_pct = (total_return_gbp / actual_invested) * 100

    # YTM for reference
    ytm = calculate_ytm(
        face_value, coupon_rate, market_price,
        settlement_date, maturity_date, coupon_frequency
    )

    # --- Year-by-year breakdown ---
    yearly_breakdown = []
    cumulative_income = 0.0

    for year in range(1, int(years_to_maturity) + 1):
        cumulative_income += total_annual_coupon
        yearly_breakdown.append({
            "year": year,
            "coupon_income_this_year": round(total_annual_coupon, 2),
            "cumulative_coupon_income": round(cumulative_income, 2),
            # Total value = what you'd have if you sold at face value + coupons received
            "cumulative_total_value": round(actual_invested + cumulative_income, 2)
        })

    return {
        "bonds_purchased": bonds_purchased,
        "actual_invested": round(actual_invested, 2),
        "coupon_per_period": round(total_coupon_per_period, 2),
        "annual_coupon_income": round(total_annual_coupon, 2),
        "total_coupon_income": round(total_coupon_income, 2),
        "capital_gain_loss": round(capital_gain_loss, 2),
        "total_return_gbp": round(total_return_gbp, 2),
        "total_return_pct": round(total_return_pct, 4),
        "years_to_maturity": round(years_to_maturity, 2),
        "ytm": ytm,
        "yearly_breakdown": yearly_breakdown
    }