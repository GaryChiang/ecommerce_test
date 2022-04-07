from decimal import Decimal
from typing import Union
from datetime import datetime

from django.db import transaction
from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.response import Response

from ecommerce.models import OrderMaster, OrderDetail, Product
from ecommerce.serializers import OrderMasterCreateSerializer, OrderDetailCreateSerializer
from django.db.models import F


class OrderQuery:
    """
    Order query base class
    """

    @staticmethod
    def query_order(customer_id: Union[int, None], order_id: Union[int, None], restaurant_id: Union[int, None]) -> list:
        """
        query order info
        :param customer_id: table customer id field
        :param order_id: table order_master id field
        :param restaurant_id: table restaurant id field
        :return: order info list
        """
        try:
            # get the master info
            orders = OrderMaster.objects.filter(active=1)

            if restaurant_id is not None:
                orders = orders.filter(restaurant_id=restaurant_id)

            if customer_id is not None:
                orders = orders.filter(customer_id=customer_id)

            if order_id is not None:
                orders = orders.filter(id=order_id)

            orders = orders.order_by(
                '-delivered_date').values(
                'delivered_date',
                'delivered_time',
                'delivery_cost',
                'food_cost',
                'total',
                'id',
                delivery_staff_name=F('delivery_staff__name'),
                restaurnat_name=F('restaurant__name'))

            orders = list(orders)

            return orders
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def query_order_detail(orders: list) -> None:
        """
        query order detail - >"call by reference"
        """
        try:
            for order in orders:
                # get every master order detail info
                detail = list(OrderDetail.objects.filter(
                    order_master_id=order['id'],
                    active=1).values(
                    'quantity',
                    'comment',
                    'product',
                    'product_type',
                    product_name=F('product__name'),
                    product_type_name=F('product_type__name')
                ))

                order['food'] = detail

        except Exception as e:
            print(e)
            raise


class OrderList(generics.ListAPIView, OrderQuery):
    """
    common order query
    """

    def list(self, request, customer_id=None, order_id=None, *args, **kwargs):
        try:
            # to decide show detail order info or not
            detail = self.request.query_params.get('detail')
            detail = int(detail) if detail else 0

            # query orders
            orders = self.query_order(customer_id=customer_id, order_id=order_id, restaurant_id=order_id)

            # request order with detail info
            if detail == 1:
                self.query_order_detail(orders)

            if order_id is not None:
                orders = orders[0]

            return Response(orders)
        except Exception as e:
            print(e)
            raise


class CustomerListCreate(generics.ListCreateAPIView, OrderList):
    """
    Customer api
    """

    def create(self, request, customer_id=None, *args, **kwargs):
        try:
            return Response(self.order_create(data=request.data, customer_id=customer_id))
        except Exception as e:
            print(e)
            raise

    def order_create(self, data: dict, customer_id: int) -> dict:
        """
        order create
        :param data: order info
        :param customer_id: table customer id field
        :return: return created order
        """
        try:
            # order detail valid
            detail = data['foods']
            serializer = OrderDetailCreateSerializer(data=detail, many=True)
            serializer.is_valid(detail)

            # calculate food cost and total cost
            food_cost = self.cal_food_cost(detail)
            total = food_cost + data['delivery_cost']

            # order master valid
            data.pop('foods')
            data['customer_id'] = customer_id
            serializer = OrderMasterCreateSerializer(data=data)
            serializer.is_valid(data)
            order = data

            # generate order
            with transaction.atomic():
                order = OrderMaster.objects.create(**order, food_cost=food_cost, total=total, active=1, create_time=str(datetime.now()))
                detail = [OrderDetail(**item, active=1, order_master_id=order.id, create_time=str(datetime.now())) for item in detail]
                foods = OrderDetail.objects.bulk_create(detail)
                foods = [model_to_dict(food) for food in foods]

                order = model_to_dict(order)
                order['foods'] = foods

            return order
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def cal_food_cost(foods: list) -> Decimal:
        """
        calculate total food cost
        :param foods: foods in order
        :return: food cost
        """
        try:
            food_cost = 0
            for food in foods:
                product = Product.objects.get(id=food['product_id'])
                food_cost = food_cost + (product.price * food['quantity'])

            return food_cost
        except Exception as e:
            print(e)
            raise


class RestaurantList(generics.RetrieveAPIView, OrderQuery):
    """
    Restaurant api
    """

    def retrieve(self, request, query_type=None, restaurant_id=None, product_id=None, *args, **kwargs):
        try:
            if query_type == 'DeliveryCost':
                return Response({'deliver_cost': self.get_total_delivery_cost(restaurant_id=restaurant_id)})

            if query_type == 'AverageNumber':
                return Response({'average_number': self.get_average_number(restaurant_id=restaurant_id, product_id=product_id)})
        except Exception as e:
            print(e)
            raise

    def get_average_number(self, restaurant_id: int, product_id: int) -> float:
        """
        get average number of product
        :param restaurant_id: table restaurant id field
        :param product_id: table product id field
        :return: average number of burgers ordered by a customer
        """
        try:
            burger_orders = list(OrderMaster.objects.filter(
                active=1,
                restaurant_id=restaurant_id,
                orderdetail__product=product_id,
                orderdetail__active=1).values_list('orderdetail__quantity', flat=True))

            number_of_burger = sum([order for order in burger_orders])
            total_order = len(self.query_order(restaurant_id=restaurant_id, customer_id=None, order_id=None))
            return number_of_burger / total_order

        except Exception as e:
            print(e)
            raise

    def get_total_delivery_cost(self, restaurant_id: int) -> Decimal:
        """
        get restaurant total delivery cost
        :param restaurant_id: table restaurant id field
        :return: total delivery cost
        """
        try:
            orders = self.query_order(customer_id=None, restaurant_id=restaurant_id, order_id=None)
            total_deliver = sum([order['delivery_cost'] for order in orders])

            return total_deliver
        except Exception as e:
            print(e)
            raise
