def format_product_message(product: dict, url: str):

    title = product.get("title")
    old_price = product.get("old_price")
    new_price = product.get("new_price")
    discount = product.get("discount")
    link = product.get("link")

    message = f"""
        🎉 {title}

        💸 De R$ {old_price} por R$ {new_price}

        🔥 {discount}% OFF

        🛒 Confira:
        {url if link is None else link}
    """

    return message.strip()
