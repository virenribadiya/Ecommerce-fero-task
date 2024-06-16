from rest_framework import serializers
from .models import Customer,Product,Order,OrderItem
from datetime import date

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    # field level validation - checking the weight field
    def validate_weight(self, value):
            print("value",value)
            if value <= 0 and value > 25:
                raise serializers.ValidationError("Weight must be positive and less than or equal to 25 kg")
            return value
    

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    order_number = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id','order_number','customer', 'order_date', 'address', 'order_items']

    def validate(self, data):
        order_items_data = data.get('order_items')
        total_weight = 0
        for item in order_items_data:
            product_weight = item['product'].weight
            quantity = item['quantity']
            total_weight += product_weight * quantity
        if total_weight > 150:
            raise serializers.ValidationError("The cumulative weight of the order items exceeds 150kg.")
        return data
    
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        print(order_items_data)
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order
    
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items')
        
        instance.customer = validated_data.get('customer', instance.customer)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.address = validated_data.get('address', instance.address)
        
        instance.order_items.all().delete()

        for order_item_data in order_items_data:
            OrderItem.objects.create(order=instance, **order_item_data)

        instance.save()
        return instance

    def validate_order_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Order date cannot be in the past")
        return value
    

    
    
    
    
    