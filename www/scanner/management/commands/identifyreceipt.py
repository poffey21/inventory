from decimal import Decimal
import json

from django.core.management.base import BaseCommand, CommandError

from scanner.models import Receipt
from scanner.models import Item
from scanner.apis import VisionApi

MARGIN_OF_ERROR = 20

class Command(BaseCommand):
    help = 'Go through each receipt and identify its items.'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)
    
    def convert_price_for_aldi(self, price=None):
        ### fix it without .
        if price is not None:
            price = price.replace(',', '.')
            if '.' not in price:
                price = '.' + price
            if price.startswith('.'):
                price = '1' + price
            price = Decimal(price)
        return price
        
    
    def find_words_in_line_for_aldi(self, receipt, min_y, max_y):
        starting_x = None
        starting_y = None
        ending_x = None
        ending_y = None
        words = {}
        y_history = {}
        for item in self.data:
            vertices = [x['y'] for x in item['boundingPoly']['vertices']]
            if max(vertices) <= max_y and min(vertices) >= min_y:
                min_x = min([x['x'] for x in item['boundingPoly']['vertices']])
                max_x = max([x['x'] for x in item['boundingPoly']['vertices']])
                y_history[min_x] = min(vertices), max(vertices)
                words[min_x] = item['description']
                if starting_x is None or min_x < starting_x:
                    starting_x = min_x
                if starting_y is None or min(vertices) < starting_y:
                    starting_y = min(vertices)
                if ending_x is None or max_x > ending_x:
                    ending_x = min_x
                if ending_y is None or max(vertices) > ending_y:
                    ending_y = max(vertices)
                
        if words:
            ordered_words = [words[x] for x in sorted(words)]
            #print(' '.join(ordered_words))
            #print(', '.join(['{}: {}'.format(x, y_history[x]) for x in sorted(y_history)]))
            item_price = self.convert_price_for_aldi(ordered_words[-2])
            # print('FULL SIZE: {},{} ({}x{})'.format(starting_x, starting_y, ending_x-starting_x, ending_y-starting_y))
            Item.objects.get_or_create(
                receipt=receipt, given_name=' '.join(ordered_words[:2]), amount=item_price,
                x_from_left=starting_x, y_from_top=starting_y,
                x_size=ending_x-starting_x, y_size=ending_y-starting_y,
            )
            return item_price

    def handle(self, *args, **options):
        vision = None
        receipts = Receipt.objects.all()
        
        empty_receipts = {x.image.url: x for x in receipts.filter(json_data__iexact='')}
        if empty_receipts:
            print('Reading text from {} receipts'.format(len(empty_receipts)))
            vision = VisionApi()
            results = vision.detect_text(empty_receipts)
            for filename in results.keys():
                obj = empty_receipts[filename]
                obj.json_data = json.dumps(results[filename])
                obj.save()
        
        for receipt in receipts.filter(store__isnull=False, pk=1):
            store = receipt.store.franchise.name.lower()
            if hasattr(self, 'find_words_in_line_for_{}'.format(store)):
                total_price = Decimal(0.00)
                self.data = json.loads(receipt.json_data)
                print('###########################################')
                print(receipt.image.url)
                print('###########################################')
                for item in self.data:
                    if item['description'].endswith('NC') or item['description'].endswith('FB'):
                        vertices = [x['y'] for x in item['boundingPoly']['vertices']]
                        min_y = min(vertices) - MARGIN_OF_ERROR
                        max_y = max(vertices) + MARGIN_OF_ERROR
                        #print("looking for items between: {} and {}".format(min_y, max_y))
                        conversion = getattr(self, 'find_words_in_line_for_{}'.format(store))
                        total_price += conversion(receipt, min_y, max_y)
                print('Total Price: {}'.format(total_price))
