from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer, Center, Slot, SlotBooking, Plan, Invoice, User
from .serializers import (
    CustomerSerializer,
    LoginSerializer,
    UserSerializer,
    CenterSerializer,
    SlotSerializer,
    SlotBookingSerializer,
    PlanSerializer,
    InvoiceSerializer,
)


# =========================================
# USER API (ModelViewSet)
# =========================================

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_queryset(self):
        qs = super().get_queryset()
        role = self.request.query_params.get('role')
        if role:
            qs = qs.filter(role=role)
        return qs

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='by-role/(?P<role>[^/.]+)')
    def by_role(self, request, role=None):
        users = self.get_queryset().filter(role=role)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


# =========================================
# CUSTOMER API
# =========================================

@api_view(['GET'])
def wave_choices(request):
    choices = [{'value': k, 'label': v} for k, v in Customer.WAVE_CHOICES]
    return Response(choices, status=status.HTTP_200_OK)


@api_view(['GET'])
def customer_list(request):
    customers = Customer.objects.all().order_by('-id')
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def customer_create(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def customer_update(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def customer_partial_update(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def customer_delete(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    customer.delete()
    return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# =========================================
# LOGIN API
# =========================================

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
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

@api_view(['GET'])
def center_list(request):
    centers = Center.objects.all().order_by('-id')
    serializer = CenterSerializer(centers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def center_create(request):
    serializer = CenterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def center_detail(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        return Response({'error': 'Center not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CenterSerializer(center)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def center_update(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        return Response({'error': 'Center not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CenterSerializer(center, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def center_partial_update(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        return Response({'error': 'Center not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CenterSerializer(center, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def center_delete(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        return Response({'error': 'Center not found'}, status=status.HTTP_404_NOT_FOUND)
    center.delete()
    return Response({'message': 'Center deleted successfully'}, status=status.HTTP_200_OK)


# =========================================
# PLAN API
# =========================================

@api_view(['GET'])
def plan_list(request):
    plans = Plan.objects.all().order_by('-id')
    serializer = PlanSerializer(plans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def plan_create(request):
    serializer = PlanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def plan_detail(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlanSerializer(plan)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def plan_update(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlanSerializer(plan, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def plan_partial_update(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlanSerializer(plan, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def plan_delete(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
    if Invoice.objects.filter(plan=plan).exists():
        return Response({'error': 'Cannot delete plan. It is used in invoices.'}, status=status.HTTP_400_BAD_REQUEST)
    plan.delete()
    return Response({'message': 'Plan deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# =========================================
# SLOT API
# =========================================

@api_view(['GET'])
def slot_list(request):
    slots = Slot.objects.all().order_by('-id')
    serializer = SlotSerializer(slots, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def slot_create(request):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def slot_detail(request, pk):
    try:
        slot = Slot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return Response({'error': 'Slot not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SlotSerializer(slot)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def slot_update(request, pk):
    try:
        slot = Slot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return Response({'error': 'Slot not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SlotSerializer(slot, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def slot_partial_update(request, pk):
    try:
        slot = Slot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return Response({'error': 'Slot not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SlotSerializer(slot, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def slot_delete(request, pk):
    try:
        slot = Slot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return Response({'error': 'Slot not found'}, status=status.HTTP_404_NOT_FOUND)
    slot.delete()
    return Response({'message': 'Slot deleted successfully'}, status=status.HTTP_200_OK)


# =========================================
# SLOT BOOKING API
# =========================================

@api_view(['GET'])
def slot_booking_list(request):
    bookings = SlotBooking.objects.all().order_by('-id')
    serializer = SlotBookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def slot_booking_create(request):
    serializer = SlotBookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def slot_booking_detail(request, pk):
    try:
        booking = SlotBooking.objects.get(pk=pk)
    except SlotBooking.DoesNotExist:
        return Response({'error': 'Slot booking not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SlotBookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def slot_booking_update(request, pk):
    try:
        booking = SlotBooking.objects.get(pk=pk)
    except SlotBooking.DoesNotExist:
        return Response({'error': 'Slot booking not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SlotBookingSerializer(booking, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def slot_booking_partial_update(request, pk):
    try:
        booking = SlotBooking.objects.get(pk=pk)
    except SlotBooking.DoesNotExist:
        return Response({'error': 'Slot booking not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SlotBookingSerializer(booking, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def slot_booking_delete(request, pk):
    try:
        booking = SlotBooking.objects.get(pk=pk)
    except SlotBooking.DoesNotExist:
        return Response({'error': 'Slot booking not found'}, status=status.HTTP_404_NOT_FOUND)
    booking.delete()
    return Response({'message': 'Slot booking deleted successfully'}, status=status.HTTP_200_OK)



# =========================================
# INVOICE API
# =========================================

@api_view(['GET'])
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-id')
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def invoice_create(request):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def invoice_detail(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = InvoiceSerializer(invoice)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def invoice_update(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = InvoiceSerializer(invoice, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def invoice_partial_update(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def invoice_delete(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
    invoice.delete()
    return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)