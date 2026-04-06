from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer, Center, Slot, SlotBooking, Plan, Invoice
from .serializers import (
    CustomerSerializer,
    LoginSerializer,
    CenterSerializer,
    SlotSerializer,
    SlotBookingSerializer,
    PlanSerializer,
    InvoiceSerializer,
)


# =========================================
# CUSTOMER API
# =========================================

@api_view(['GET', 'POST'])
def customer_list_create(request):
    if request.method == 'GET':
        customers = Customer.objects.all().order_by('-id')
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()
        return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# =========================================
# LOGIN API
# =========================================

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            return Response(
                {
                    "message": "Login successful",
                    "user_id": user.id,
                    "username": user.username,
                    "role": user.role,
                    "center": user.center.center_name if user.center else None,
                    "redirect_to": "admin_dashboard" if user.role == "super_admin" else "branch_dashboard",
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================
# CENTER API
# =========================================

class CenterListCreateAPIView(APIView):
    def get(self, request):
        centers = Center.objects.all().order_by("-id")
        serializer = CenterSerializer(centers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        many = isinstance(request.data, list)
        serializer = CenterSerializer(data=request.data, many=many)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Center(s) created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CenterDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Center.objects.get(pk=pk)
        except Center.DoesNotExist:
            return None

    def get(self, request, pk):
        center = self.get_object(pk)
        if not center:
            return Response({"message": "Center not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CenterSerializer(center)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        center = self.get_object(pk)
        if not center:
            return Response({"message": "Center not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CenterSerializer(center, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Center updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        center = self.get_object(pk)
        if not center:
            return Response({"message": "Center not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CenterSerializer(center, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Center updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        center = self.get_object(pk)
        if not center:
            return Response({"message": "Center not found"}, status=status.HTTP_404_NOT_FOUND)

        center.delete()
        return Response(
            {"message": "Center deleted successfully"},
            status=status.HTTP_200_OK
        )


# =========================================
# PLAN API
# =========================================

@api_view(['GET', 'POST'])
def plan_list_create(request):
    if request.method == 'GET':
        plans = Plan.objects.all().order_by('-id')
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def plan_detail(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PlanSerializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        plan.delete()
        return Response({'message': 'Plan deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# =========================================
# SLOT API
# =========================================

class SlotListCreateAPIView(APIView):
    def get(self, request):
        slots = Slot.objects.all().order_by("-id")
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        many = isinstance(request.data, list)
        serializer = SlotSerializer(data=request.data, many=many)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Slot(s) created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlotDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Slot.objects.get(pk=pk)
        except Slot.DoesNotExist:
            return None

    def get(self, request, pk):
        slot = self.get_object(pk)
        if not slot:
            return Response({"message": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SlotSerializer(slot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        slot = self.get_object(pk)
        if not slot:
            return Response({"message": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Slot updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        slot = self.get_object(pk)
        if not slot:
            return Response({"message": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SlotSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Slot updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        slot = self.get_object(pk)
        if not slot:
            return Response({"message": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)

        slot.delete()
        return Response(
            {"message": "Slot deleted successfully"},
            status=status.HTTP_200_OK
        )


# =========================================
# SLOT BOOKING API
# =========================================

class SlotBookingListCreateAPIView(APIView):
    def get(self, request):
        bookings = SlotBooking.objects.all().order_by("-id")
        serializer = SlotBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        many = isinstance(request.data, list)
        serializer = SlotBookingSerializer(data=request.data, many=many)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Slot booking(s) created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlotBookingDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return SlotBooking.objects.get(pk=pk)
        except SlotBooking.DoesNotExist:
            return None

    def get(self, request, pk):
        booking = self.get_object(pk)
        if not booking:
            return Response({"message": "Slot booking not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SlotBookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        booking = self.get_object(pk)
        if not booking:
            return Response({"message": "Slot booking not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SlotBookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Slot booking updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        booking = self.get_object(pk)
        if not booking:
            return Response({"message": "Slot booking not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SlotBookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Slot booking updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booking = self.get_object(pk)
        if not booking:
            return Response({"message": "Slot booking not found"}, status=status.HTTP_404_NOT_FOUND)

        booking.delete()
        return Response(
            {"message": "Slot booking deleted successfully"},
            status=status.HTTP_200_OK
        )


# =========================================
# INVOICE API
# =========================================

@api_view(['GET', 'POST'])
def invoice_list_create(request):
    if request.method == 'GET':
        invoices = Invoice.objects.all().order_by('-id')
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def invoice_detail(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        invoice.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)