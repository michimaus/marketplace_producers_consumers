"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """

        # Initializing the thread
        super().__init__(name=kwargs['name'], daemon=kwargs['daemon'])

        # Injecting the market reference and setting the assigned waiting time
        # And production capabilities
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        # Assign a unique ID
        self.producer_id = marketplace.register_producer()

    def run(self):
        # Start producing according to the assigned production list
        while True:
            for entry in self.products:
                i: int = 0
                while i < entry[1]:
                    is_added = self.marketplace.publish(self.producer_id, entry[0])

                    # Publish a product as long as there is space on the market
                    if is_added:
                        sleep(entry[2])
                        i += 1
                    else:
                        sleep(self.republish_wait_time)
