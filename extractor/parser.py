from bs4 import BeautifulSoup
import re

def extract_price(element):

    if not element:
        return None

    fraction = element.select_one(
        ".andes-money-amount__fraction"
    )

    cents = element.select_one(
        ".andes-money-amount__cents"
    )

    if not fraction:
        return None

    value = fraction.get_text(strip=True)

    if cents:
        value += f",{cents.get_text(strip=True)}"

    return value

def parse_price(value: str):

    if not value:
        return 0.0

    value = re.sub(r"[^\d,\.]", "", value)

    value = value.replace(".", "")

    value = value.replace(",", ".")

    return float(value)

def extract_product(html: str):

    soup = BeautifulSoup(html, "lxml")

    product = {}

    # título
    title = soup.select_one(
        ".poly-component__title"
    )

    if title:

        product["title"] = title.get_text(
            strip=True
        )

        product["link"] = title.get("href")

    # imagem
    image = soup.select_one(
        ".poly-component__picture"
    )

    if image:
        product["image"] = image.get("src")

    # preço antigo
    old_price_element = soup.select_one(
        ".andes-money-amount--previous"
    )

    old_price = extract_price(
        old_price_element
    )

    # preço atual
    current_price_element = soup.select_one(
        ".poly-price__current .andes-money-amount"
    )

    new_price = extract_price(
        current_price_element
    )

    product["old_price"] = old_price
    product["new_price"] = new_price

    try:

        old_value = parse_price(old_price)

        new_value = parse_price(new_price)

        if old_value > 0:

            discount = round(
                (
                    (old_value - new_value)
                    / old_value
                ) * 100
            )

            economy = round(
                old_value - new_value,
                2
            )

            product["discount"] = discount

            product["economy"] = (
                f"{economy:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

    except Exception as e:

        print("Erro cálculo:", e)

    return product