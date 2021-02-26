from django.core.management.base import BaseCommand
import pandas as pd
import os
from dashboard.models import Order
from datetime import date

EXPECTED_CSV_HEADERS = ['OrderNumber', 'Quantity', 'Price Per Piece', 'SALES', 'MONTH_ID', 'YEAR_ID', 'PRODUCTLINE',
                        'DEALSIZE']


class Command(BaseCommand):
    args = 'PATH_TO_CSV'
    help = """
        Provide the absolute/relative path to the Sales data CSV File.
    """

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Indicates the path of csv')

    def handle(self, *args, **options):
        file_path = options.get('path')
        os.path.exists(file_path)
        if file_path and os.path.exists(file_path):
            try:
                dataFrame = pd.read_csv(file_path)
                all_records = dataFrame.to_dict(orient='records')
                if self._check_valid_headers(dataFrame):
                    for record in all_records:
                        record = self.strip_keys(record)

                        order_num = record.get('OrderNumber')
                        month = record.get('MONTH_ID')
                        year = record.get('YEAR_ID')
                        order_date = date(day=date.today().day, month=month, year=year)
                        order_obj = Order.objects.filter(order_number=order_num, order_date__month=order_date.month,
                                                         order_date__year=order_date.year)
                        if order_obj:

                            order_obj = order_obj.first()
                            order_obj = self.save_order(record, order_obj)
                        else:

                            order_obj = Order()
                            order_obj.order_number = order_num
                            order_obj.order_date = order_date
                            order_obj = self.save_order(record, order_obj)
                else:
                    return 'Invalid CSV headers.'

            except Exception as e:
                print(e, 'Exception thrown')
                return str(e)
        else:
            return 'Invalid file or file does not exist.'

    def _check_valid_headers(self, dataFrame):
        """
            Check if expected and received headers are same
        """

        csv_headers = set(map(lambda header: header.strip().lower(), dataFrame.keys()))
        expected_headers = set(map(lambda header: header.strip().lower(), EXPECTED_CSV_HEADERS))
        if csv_headers == expected_headers:
            return True
        return False

    def save_order(self, record, order_obj):
        """
            Save Order object
        """
        order_obj.quantity = record.get('Quantity')
        order_obj.price = record.get('Price Per Piece')
        order_obj.sales = record.get('SALES')
        order_obj.product_line = record.get('PRODUCTLINE')
        order_obj.deal_size = record.get('DEALSIZE')
        order_obj.save()
        return order_obj

    def strip_keys(self, record):
        """
            Strip headers
        """
        keys = record.keys()
        values = record.values()
        keys = list(map(lambda header: header.strip(), keys))
        return dict(zip(keys, values))


