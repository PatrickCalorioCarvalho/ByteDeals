from bs4 import BeautifulSoup

def extract_product(html: str):

    soup = BeautifulSoup(html, "lxml")

    product = {}

    title = soup.select_one(".poly-component__title")

    if title:
        product["title"] = title.get_text(strip=True)

    image = soup.select_one(".poly-component__picture")

    if image:
        product["image"] = image.get("src")

    if title:
        product["link"] = title.get("href")

    amounts = soup.select(".andes-money-amount")

    prices = []

    for amount in amounts:

        fraction = amount.select_one(
            ".andes-money-amount__fraction"
        )

        cents = amount.select_one(
            ".andes-money-amount__cents"
        )

        if fraction:

            value = fraction.get_text(strip=True)

            if cents:
                value += f",{cents.get_text(strip=True)}"

            prices.append(value)

    if len(prices) >= 1:
        product["old_price"] = prices[0]

    if len(prices) >= 2:
        product["new_price"] = prices[1]

    return product

