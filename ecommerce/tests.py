from django.test import TestCase
from ecommerce.models import OrderMaster, Product, Restaurant, Category, Customer, DeliveryStaff, ProductType
from ecommerce.views import CustomerListCreate


class EcommerceModuleTestCase(TestCase):
    """
    ecommerce  module test case
    """

    def setUp(self):
        try:
            # inserted data prepare
            self.data = {
                "restaurant_id": 1,
                "delivery_staff_id": 1,
                "delivered_date": "2022/04/06",
                "delivered_time": "12:00",
                "delivery_cost": 30,
                "foods": [
                    {"product_id": 1, "product_type_id": 1, "quantity": 1, "comment": ""},
                    {"product_id": 1, "product_type_id": 2, "quantity": 2, "comment": ""}
                ]
            }

            # prepare tables
            self.prepare_tables()
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def prepare_tables() -> None:
        """
        prepare tables
        """
        try:
            ProductType.objects.create(
                **{
                    "id": 1,
                    "name": "beef",
                    "active": 1,
                    "create_time": "2022/04/05 16:00:00",
                    "update_time": None,
                    "product_id": 1
                }
            )

            ProductType.objects.create(
                **{
                    "id": 2,
                    "name": "chicken",
                    "active": 1,
                    "create_time": "2022/04/05 16:00:00",
                    "update_time": None,
                    "product_id": 1
                }
            )

            DeliveryStaff.objects.create(
                **{
                    "id": 1,
                    "name": "Gary",
                    "active": 1,
                    "create_time": "2022/04/05 16:00:00",
                    "update_time": None
                }
            )

            Customer.objects.create(
                **{
                    "id": 1,
                    "name": "Client",
                    "address": None,
                    "coordinates": None,
                    "tel": None,
                    "active": 1,
                    "create_time": "2022/04/05 16:00:00",
                    "update_time": None
                }
            )

            Category.objects.create(
                **{
                    "id": 1,
                    "name": "Burger",
                    "active": 1,
                    "create_time": "2022/04/05 16:00:00",
                    "update_time": None
                }
            )

            Restaurant.objects.create(
                **{
                    "id": 1,
                    "name": "Burger Stall",
                    "district": None,
                    "address": None,
                    "tel": None,
                    "active": 1,
                    "remark": None,
                    "create_time": "2020/04/05 16:00:00",
                    "update_time": None,
                    "coordinates": None
                }
            )

            Product.objects.create(
                **{
                    "name": "Burger",
                    "remark": None,
                    "active": 1,
                    "category_id": 1,
                    "create_time": "2022/04/05 16:00:00",
                    "update_time": None,
                    "restaurant_id": 1,
                    "price": 100
                }
            )
        except  Exception as e:
            print(e)
            raise

    def test_order_create(self):
        try:
            CustomerListCreate().order_create(data=self.data, customer_id=1)
            master = OrderMaster.objects.all().count()

            self.assertEqual(master, 1)
        except Exception as e:
            print(e)
            raise
