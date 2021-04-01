"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from typing import Dict, Deque
from collections import deque

from tema.product import Product


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        # Mapping the producer to the produced quantities
        self.number_of_products_per_producer: Dict[int, int] = {}

        # Mapping a product to the list of apparitions, according to the producer ID
        self.products_evidence: Dict[Product, Deque[int]] = {}

        # Mapping a cart to the contained products, arranged by the producers ID
        self.cart_evidence: Dict[int, Dict[Product, Deque[int]]] = {}

        # Listing for ID assignments
        self.id_producer: int = 0
        self.id_cart: int = 0

        # Max size allocated for the shelf of each producer
        self.queue_size_per_producer: int = queue_size_per_producer

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        current_val: int

        # Increment and assign an ID for a producer
        current_val = self.id_producer
        self.number_of_products_per_producer[current_val] = 0
        self.id_producer += 1

        return current_val

    def publish(self, producer_id, product) -> bool:
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        # Fail in case there is no space left
        if self.number_of_products_per_producer[producer_id] >= self.queue_size_per_producer:
            return False

        # Increment in the evidence mapping
        self.number_of_products_per_producer[producer_id] += 1
        if product in self.products_evidence:
            self.products_evidence[product].append(producer_id)
        else:
            self.products_evidence[product] = deque([producer_id])

        return True

    def new_cart(self) -> int:
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        current_val: int

        # Increment and assign an ID for each cart
        current_val = self.id_cart
        self.id_cart += 1
        self.cart_evidence[current_val] = {}

        return current_val

    def add_to_cart(self, cart_id, product) -> bool:
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        # Fail in case the product is not on stock
        if product not in self.products_evidence or len(self.products_evidence[product]) == 0:
            return False

        # Get the ID of the producer for the next product in line
        producer_of_product: int = self.products_evidence[product].popleft()

        # Add the product to the cart evidence and take out from market evidence
        if product in self.cart_evidence[cart_id]:
            self.cart_evidence[cart_id][product].append(producer_of_product)
        else:
            self.cart_evidence[cart_id][product] = deque([producer_of_product])

        self.number_of_products_per_producer[producer_of_product] -= 1

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        # Take out prom cart evidence and republish
        producer_of_product: int = self.cart_evidence[cart_id][product].popleft()

        # The product already existed on the evidence ot the market
        # As there is no need for an additional check as done before
        self.products_evidence[product].append(producer_of_product)
        self.number_of_products_per_producer[producer_of_product] += 1

    def place_order(self, cart_id) -> Dict[Product, int]:
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # Return the mapping inside the cart
        # Producers of the specific kind of product no longer an interest factor
        # Quantity is the main interest now
        return dict(
            (prod, len(self.cart_evidence[cart_id][prod])) for prod in self.cart_evidence[cart_id])
