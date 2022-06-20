import glob
import os
import re
from collections import namedtuple
import dateutil.parser

OUTPUT_FOLDER = 'output'


class ShoppingListEntries:

    def __init__(self):
        self.shop_name = None
        self.purchase_date = None
        self.total_items = None
        self.amount_paid = None
        self.items = namedtuple('Item', 'item_name item_price')

    def is_valid_item(self, row):
        row = re.sub(r'^x', '', row)
        pattern = r'^([A-Z0-9]+ .*?) (\d+.\d{2})$'
        res = re.search(pattern, row)
        if res:
            self.items.item_name.append(res[1])
            self.items.item_price.append(res[2])
            return True
        return False


class ShopTemplate:

    def __init__(self):
        self.shop_name = None
        self.order_line_start = None
        self.total_items = None


def get_root_dir():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    root_dir, _ = os.path.split(dir_path)
    return root_dir


def check_if_not_empty_folder(user: str) -> bool:
    user_dir = os.path.join(get_root_dir(), OUTPUT_FOLDER, user)
    if os.path.isdir(user_dir):
        if not os.listdir(user_dir):
            return False
        else:
            return True
    else:
        return False


def files_generator(user):
    user_dir = os.path.join(get_root_dir(), OUTPUT_FOLDER, user, '*.txt')
    files = glob.glob(user_dir)
    for file in files:
        yield file


def get_shopping_list_fields(file):
    text = open(file).read().encode(encoding="ascii", errors="ignore").decode('utf-8')
    supermarkets = ["m&s", "m&", "waitrose", "sainsbury's", "tesco"]
    # total items, total paid after coupons etc, line number
    template = {
        "m&s": [(r'(\w+): (\d+) (.+?)(\d+.+)', 2), (r'(\w+): (\d+) (.+?)(\d+.+)', 4), 9],
        "waitrose": [(r'(\d+) items', 1), (r'(\d+\S+)(\nCHANGE)', 1), 5],
        "sainsbury's": [(r'\n(\d+) (B.+?)(\d+.+?)\n', 1), (r'\n(\d+) (B.+?)(\d+.+?)\n', 3), 8], # might not reflect amount saved
        "tesco": [None, (r'(\w+): (\W{1})(\S+)', 3), 6]  # might not reflect amount saved
    }
    text_list = text.split('\n')
    entries = ShoppingListEntries()
    if text_list[0].lower() in supermarkets:
        entries.shop_name = text_list[0].lower()
    date_pattern = r'(\d+/\d+/\d{2,4})|(\d+(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\d{2,4})'
    # TODO: add error handling
    entries.purchase_date = dateutil.parser.parse(re.search(date_pattern, text).group(0), dayfirst=True)
    # items purchased
    Shop = namedtuple('Shop', ('ttl_items', 'money_paid', 'first_item'))
    shop = Shop(*template[entries.shop_name])
    entries.total_items = re.search(shop.ttl_items[0], text).group(shop.ttl_items[1])
    entries.amount_paid = re.search(shop.money_paid[0], text).group(shop.money_paid[1])
    num_parsed = 0
    for row in text_list[shop.first_item:]:
        row = row.strip()
        if entries.is_valid_item(row):
            num_parsed += 1
            if num_parsed == entries.total_items:
                break



