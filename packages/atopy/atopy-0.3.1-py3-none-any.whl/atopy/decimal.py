from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_FLOOR, ROUND_UP, Decimal


def di_floor(d: Decimal) -> Decimal:
    """Round towards -Infinity"""
    return d.to_integral_value(rounding=ROUND_FLOOR)


def di_ceil(d: Decimal) -> Decimal:
    """Round towards +Infinity"""
    return d.to_integral_value(rounding=ROUND_CEILING)


def di_down(d: Decimal) -> Decimal:
    """Round towards zero"""
    return d.to_integral_value(rounding=ROUND_DOWN)


def di_up(d: Decimal) -> Decimal:
    """Round away from zero"""
    return d.to_integral_value(rounding=ROUND_UP)


def div(
    dividend: Decimal, divisor: Decimal, check_zero: bool = True
) -> Decimal:
    if check_zero:
        assert divisor != 0
    return dividend / divisor


def div_di_floor(dividend: Decimal, divisor: Decimal) -> Decimal:
    return di_floor(div(dividend, divisor))


def div_di_ceil(dividend: Decimal, divisor: Decimal) -> Decimal:
    return di_ceil(div(dividend, divisor))


def div_di_down(dividend: Decimal, divisor: Decimal) -> Decimal:
    return di_down(div(dividend, divisor))


def div_di_up(dividend: Decimal, divisor: Decimal) -> Decimal:
    return di_up(div(dividend, divisor))


def bid_ticksize(price: Decimal, ticksize: Decimal) -> Decimal:
    return ticksize * div_di_floor(price, ticksize)


def ask_ticksize(price: Decimal, ticksize: Decimal) -> Decimal:
    return ticksize * div_di_ceil(price, ticksize)


def qty_unit(qty: Decimal, qtyunit: Decimal) -> Decimal:
    return qtyunit * div_di_down(qty, qtyunit)


def cash_qty(
    cash: Decimal,
    price: Decimal,
    cash_leverage: Decimal,
    contract_unit: Decimal,
    qtyunit: Decimal,
) -> Decimal:
    return qty_unit(
        div(cash * cash_leverage, price * contract_unit),
        qtyunit,
    )


def cash_risk_qty(
    cash: Decimal,
    contract_unit: Decimal,
    qtyunit: Decimal,
    risk_point: Decimal,
    risk_target: Decimal,
) -> Decimal:
    return qty_unit(
        div(cash * risk_target, risk_point * contract_unit),
        qtyunit,
    )
