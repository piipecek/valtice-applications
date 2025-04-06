def pretty_penize(castka, billing_currency: str) -> str:
    if castka is None:
        return "-"
    if castka == 0:
        castka = 0
    if castka == int(castka):
        castka = int(castka)
    else:
        castka = str(round(castka, 2)).replace(".", ",")
    if billing_currency == "czk":
        return f"{castka} Kč"
    elif billing_currency == "eur":
        return f"€ {castka}"