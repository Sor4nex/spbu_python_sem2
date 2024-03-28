from typing import Optional, Iterator


class Product:
    def __init__(self, name: str, price: int, rating: float = 5.0, available_count: int = 1) -> None:
        self.name: str = name
        self.price: float = price
        self.rating: float = rating
        self.available_count: int = available_count

    def __repr__(self) -> str:
        return "name:{}|price:{}|rating:{}|available:{}".format(self.name, self.rating, self.rating, self.available_count)


class Basket:
    def __init__(self) -> None:
        self.basket_interior: set = set()
        self.summary_price: float = 0.0

    def __iter__(self) -> Iterator:
        return self.basket_interior.__iter__()

    def add_to_basket(self, product_name: str, shop: "Shop") -> None:
        if product_name in shop:
            self.basket_interior.add(product_name)
            self.summary_price += shop.get_product(product_name).price


class Shop:
    def __init__(self) -> None:
        self.all_products: dict[str, Product] = {}
        self.products_statistics: dict[str, tuple[Optional[str], Optional[float]]] = {
            "min_rating": (None, None),
            "max_rating": (None, None),
            "min_price": (None, None),
            "max_price": (None, None)
        }

    def __contains__(self, product_name: str) -> bool:
        result = self.get_product(product_name)
        if result is None:
            return False
        return bool(result.available_count)

    def add_product(self, product: Product) -> None:
        if product.name in self:
            raise KeyError(f"product with name {product.name} already exist in this shop")
        self.all_products[product.name] = product
        if self.products_statistics["min_rating"] is None or self.products_statistics["min_rating"][1] > product.rating:
            self.products_statistics["min_rating"] = product.name, product.rating
        if self.products_statistics["max_rating"] is None or self.products_statistics["max_rating"][1] < product.rating:
            self.products_statistics["max_rating"] = product.name, product.rating
        if self.products_statistics["min_price"] is None or self.products_statistics["min_price"][1] > product.price:
            self.products_statistics["min_price"] = product.name, product.price
        if self.products_statistics["max_price"] is None or self.products_statistics["max_price"][1] > product.price:
            self.products_statistics["max_price"] = product.name, product.price

    def buy_basket(self, basket: Basket) -> None:
        for product_name in basket:
            product = self.get_product(product_name)
            if product is None or product.available_count < 1:
                raise ValueError(f"cannot buy, {product} not presented in this shop")
        for product_name in basket:
            self.get_product(product_name).available_count -= 1
        basket.basket_interior = set()
        basket.summary_price = 0.0
        return None

    def get_product(self, product_name: str) -> Product:
        return self.all_products[product_name]

    def get_product_min_rating(self) -> Product:
        return self.get_product(self.products_statistics["min_rating"][0])

    def get_product_max_rating(self) -> Product:
        return self.get_product(self.products_statistics["max_rating"][0])

    def get_product_min_price(self) -> Product:
        return self.get_product(self.products_statistics["min_price"][0])

    def get_product_max_price(self) -> Product:
        return self.get_product(self.products_statistics["max_price"][0])


if __name__ == "__main__":
    shop1, shop2 = Shop(), Shop()
    banana, grape, knife, notebook, python = Product("banana", 10, 4.6, 2), Product("grape", 13, 3.4, 3), Product(
        "knife", 20, 5.0, 1), Product("notebook", 90, 4.6, 10), Product("python", 1000)
    shop1.add_product(banana)
    shop1.add_product(grape)
    shop1.add_product(knife)
    shop2.add_product(python)
    shop2.add_product(notebook)
    print(f"shop 1 minimal rating: {shop1.get_product_min_rating()}")
    print(f"shop 2 maximal price: {shop2.get_product_max_price()}")
    basket1, basket2 = Basket(), Basket()
    basket1.add_to_basket("banana", shop1)
    basket1.add_to_basket("knife", shop1)
    shop1.buy_basket(basket1)
    basket2.add_to_basket("grape", shop1)
    basket2.add_to_basket("python", shop2)
    try:
        shop2.buy_basket(basket2)
    except ValueError:
        print("ow, we dont have this in 2 shop :(")
