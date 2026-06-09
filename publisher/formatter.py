def format_product_message(product: dict):

    title = product.get("title")

    old_price = product.get("old_price")

    new_price = product.get("new_price")

    discount = product.get("discount")

    economy = product.get("economy")

    ai_text = product.get("ai_text")

    link = product.get("link")

    lines = []

    # frase IA
    if ai_text:

        lines.append(ai_text)

        lines.append("")

    # título
    lines.append("🔥 OFERTA ENCONTRADA 🔥")

    lines.append("")

    lines.append(f"🛍️ {title}")

    # preços
    if old_price and new_price:

        lines.append("")

        lines.append(
            f"💸 De ~R$ {old_price}~ por *R$ {new_price}*"
        )

    elif new_price:

        lines.append("")

        lines.append(
            f"💰 Apenas *R$ {new_price}*"
        )

    if economy:

        lines.append("")

        lines.append(
            f"💰 Economize R$ {economy}"
        )

    if discount:

        lines.append(
            f"🔥 {discount}% OFF"
        )

    lines.append("")

    lines.append("🛒 Confira a oferta:")

    lines.append(link)

    return "\n".join(lines)