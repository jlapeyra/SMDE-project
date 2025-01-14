def float_formatter(decimals:int):
    def format_floats(val):
        if isinstance(val, float):
            return f"{val:.{decimals}f}"
        return val
    return format_floats