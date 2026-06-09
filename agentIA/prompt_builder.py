def build_prompt(product: dict):
    return f"""

    Crie UMA frase curta para oferta. de forma atrativa, usando linguagem natural e emojis.
    podendo destacar o benefício do produto, mas SEM MENCIONAR O PREÇO.
    

    Máximo:

    12 palavras
    usar emoji
    sem preço
    sem hashtags

    Produto:
        {product.get("title")}
    """