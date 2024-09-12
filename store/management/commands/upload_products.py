import os
import random
import re

import pandas as pd
from django.core.management.base import BaseCommand

from store.models import Category, Product


class Command(BaseCommand):
    help = "Upload initial data to database"
    # SELLERS = {"Ali", "Amazon", "eBay", "Etsy", "Walmart", "Shopify", "Magento", "WooCommerce", "PrestaShop",
    #            "BigCommerce", "OpenCart", "Volusion", "Wix", "Squarespace", "Weebly", "3dcart", "Big Cartel",
    #            "Ecwid", "Gumroad"}

    def add_arguments(self, parser):
        parser.add_argument("filepath", nargs=1, action="store", type=str)

    def handle(self, *args, **options):
        filepath = options["filepath"][0]

        # check file
        if not os.path.exists(filepath):
            self.stderr.write(f"File '{filepath}' does not exist.")
            return

        df = pd.read_excel(filepath)

        category_name = os.path.basename(filepath).split("Data")[0]
        # _ for the returned tuple
        category, _ = Category.objects.get_or_create(name=category_name)

        for index, row in df.iterrows():
            if row["Price"] and row["Name"]:
                price = float(re.findall(r"\d+\.\d+", str(row["Price"]))[0])
                Product.objects.create(
                    name=row["Name"],
                    price=price,
                    category=category,
                    # seller=self.generate_random_seller(),
                    quantity=self.generate_random_quantity(),
                    description="Producer : "
                    + row["Producer"]
                    + "\n"
                    + "Vram: "
                    + row["Vram"]
                    + "\n"
                    + "Boost Clock: "
                    + row["Boost Clock"]
                    + "\n"
                    + "TDP: "
                    + row["TDP"]
                    + "\n"
                    + "Memory Clock :"
                    + row["Memory Clock"]
                    + "\n"
                    + "DisplayPort: "
                    + row["DisplayPort"]
                    + "\n"
                    + "HDMI: "
                    + row["HDMI"]
                    + "\n"
                    + "Slots"
                    + row["Slots"]
                    + "\n"
                    + "Length: "
                    + row["Length"]
                    + "\n"
                    + "Width: "
                    + row["Width"]
                    + "\n"
                    + "Height: "
                    + row["Height"]
                    + "\n"
                    + "Weight: "
                    + row["Weight"]
                    + "\n"
                    + "Warranty: "
                    + row["Warranty"]
                    + "\n"
                    + "Price: "
                    + row["Price"],
                )

    # def generate_random_seller(self):
    #     return random.choice(list(self.SELLERS))

    @staticmethod
    def generate_random_quantity():
        return random.randint(1, 100)
