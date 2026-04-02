from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer


@api_view(['GET', 'POST'])
def customer_list_create(request):
    if request.method == 'GET':
        customers = Customer.objects.all().order_by('-id')
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Customer added successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(
            {"error": "Customer not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Customer updated successfully",
                    "data": serializer.data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        customer.delete()
        return Response(
            {"message": "Customer deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )