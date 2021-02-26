from django.db import models


class DealChoice(models.TextChoices):
    LARGE = 'large'
    MEDIUM = 'medium'
    SMALL = 'small'


class Order(models.Model):

    order_number = models.TextField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    sales = models.PositiveIntegerField()
    product_line = models.CharField(max_length=100)
    deal_size = models.CharField(max_length=100, choices=DealChoice.choices)
    order_date = models.DateField()

    class Meta:
        db_table = 'Order'
        ordering = ['-order_date']
        constraints = [
            models.UniqueConstraint(fields=['order_number', 'order_date'], name='unique_order_per_month_year')
        ]

    def __str__(self):
        """

        :return:
        :rtype:
        """
        return str(self.order_number) + ' | ' + str(self.product_line)

    def save(self, *args, **kwargs):
        """

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        self.sales = self.quantity * self.price
        self.deal_size = self.deal_size.lower()
        super(Order, self).save(*args, **kwargs)
