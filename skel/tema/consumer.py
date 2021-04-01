"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from typing import Dict, List
from time import sleep

from tema.product import Product


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        super().__init__(name=kwargs['name'])

        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

        self.carts_of_customer: Dict[int, List[Dict[str, any]]] = dict(
            (marketplace.new_cart(), cart) for cart in carts)

    def run(self):
        for entry in self.carts_of_customer:

            for product in self.carts_of_customer[entry]:
                if product['type'] == 'add':
                    i: int = 0

                    while i < product['quantity']:
                        is_added: bool = self.marketplace.add_to_cart(entry, product['product'])

                        if is_added:
                            i += 1
                        else:
                            sleep(self.retry_wait_time)
                elif product['type'] == 'remove':
                    i: int = 0
                    while i < product['quantity']:
                        self.marketplace.remove_from_cart(entry, product['product'])
                        i += 1

            product_for_order: Dict[Product, int] = self.marketplace.place_order(entry)
            for product in product_for_order:
                for i in range(product_for_order[product]):
                    print(self.name + ' bought ' + str(product))
