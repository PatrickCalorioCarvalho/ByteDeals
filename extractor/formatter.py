def format_product_message(product: dict, url: str):
    title = product.get("title")
    old_price = product.get("old_price")
    new_price = product.get("new_price")
    discount = product.get("discount")

    lines = []
    lines.append("🔥 OFERTA ENCONTRADA 🔥")
    lines.append("")
    lines.append(f"🛍️ {title}")

    # preços
    if old_price and new_price:

        lines.append("")
        lines.append(f"💸 De ~R$ {old_price}~ por *R$ {new_price}*")
        try:

            old_value = float(
                old_price.replace(",", ".")
            )
            new_value = float(
                new_price.replace(",", ".")
            )
            economy = round(
                old_value - new_value,
                2
            )
            lines.append(
                f"💰 Economize R$ {economy:.2f}"
            )
        except:
            pass

    elif new_price:

        lines.append("")
        lines.append(f"💰 Apenas *R$ {new_price}*")

    if discount:
        lines.append("")
        lines.append(f"🔥 {discount}% OFF")

    lines.append("")
    lines.append("🛒 Confira a oferta:")
    lines.append(url)

    return "\n".join(lines)
