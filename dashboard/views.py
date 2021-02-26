from django.views.generic import TemplateView
from .models import Order
from functools import cached_property
from django.views.generic.list import ListView


class DashboardView(ListView):
    template_name = 'dashboard.html'
    queryset = Order.objects.all().values('product_line', 'quantity', 'order_date')
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        """

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        context = super(DashboardView, self).get_context_data()
        get_data = self.request.GET.copy()
        month = get_data.get('month', 2)
        year = get_data.get('year', 2005)
        sales_product_line_graph_data= Order.objects.filter(
            order_date__year=year, order_date__month=month).values('product_line', 'sales')

        sales_data= list(Order.objects.filter(order_date__year=year).values('order_date', 'sales'))

        sales_data = self.convert_month_num_to_name(sales_data)
        context['sales_graph_data'] = sales_data
        product_line_data = Order.objects.all().values('product_line', 'quantity', 'order_date')
        context['product_line_data'] = product_line_data
        context['sales_product_line_graph_data'] = sales_product_line_graph_data
        context['selected_year'] = year
        context['selected_month'] = int(month) if isinstance(month, str) else month
        context['month_name'] = self.month_num_and_name_mapping.get(int(month), '') if month else ''
        context['months_dictionary'] = self.month_num_and_name_mapping
        return context

    @staticmethod
    def convert_month_num_to_name(sales_data):
        """

        :param sales_data:
        :type sales_data:
        :return:
        :rtype:
        """
        converted_sales_data = dict()
        for record in sales_data:
            key = record.get('order_date').strftime("%B %Y")
            value = record.get('sales')
            converted_sales_data.update({key: value})
        return converted_sales_data

    @cached_property
    def month_num_and_name_mapping(self):
        """

        :return:
        :rtype:
        """
        return {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May'}
