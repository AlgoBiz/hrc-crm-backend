from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

from .models import Customer, Center, Slot, SlotBooking, Plan, Invoice, User
from .serializers import (
    CustomerSerializer, LoginSerializer, UserSerializer,
    CenterSerializer, SlotSerializer, SlotBookingSerializer,
    PlanSerializer, InvoiceSerializer,
)


def custom_response(success=True, message="", data=None, status_code=200):
    return Response({
        "success": success,
        "message": message,
        "data": data
    }, status=status_code)


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

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(qs, many=True)
        return custom_response(True, "Users fetched successfully", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(True, "User fetched successfully", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(True, "User created successfully", serializer.data, status.HTTP_201_CREATED)
        return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return custom_response(True, "User updated successfully", serializer.data)
        return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return custom_response(True, "User deleted successfully")

    @action(detail=False, methods=['get'], url_path='by-role/(?P<role>[^/.]+)')
    def by_role(self, request, role=None):
        users = self.get_queryset().filter(role=role)
        serializer = self.get_serializer(users, many=True)
        return custom_response(True, f"Users with role '{role}' fetched successfully", serializer.data)


# =========================================
# CUSTOMER API
# =========================================

@api_view(['GET'])
def wave_choices(request):
    choices = [{'value': k, 'label': v} for k, v in Customer.WAVE_CHOICES]
    return custom_response(True, "Wave choices fetched successfully", choices)


@api_view(['GET'])
def customer_list(request):
    qs = Customer.objects.all().order_by('-id')
    search = request.query_params.get('search')
    center = request.query_params.get('center')
    date = request.query_params.get('date')
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(mobile__icontains=search))
    if center:
        qs = qs.filter(center_id=center)
    if date:
        qs = qs.filter(created_at__date=date)
    serializer = CustomerSerializer(qs, many=True)
    return custom_response(True, "Customers fetched successfully", serializer.data)


@api_view(['POST'])
def customer_create(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Customer created successfully", serializer.data, status.HTTP_201_CREATED)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return custom_response(False, "Customer not found", None, status.HTTP_404_NOT_FOUND)
    return custom_response(True, "Customer fetched successfully", CustomerSerializer(customer).data)


@api_view(['PUT'])
def customer_update(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return custom_response(False, "Customer not found", None, status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Customer updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def customer_partial_update(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return custom_response(False, "Customer not found", None, status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Customer updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def customer_delete(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return custom_response(False, "Customer not found", None, status.HTTP_404_NOT_FOUND)
    customer.delete()
    return custom_response(True, "Customer deleted successfully")


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
            return custom_response(True, "Login successful", {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "center": user.center.center_name if user.center else None,
                },
                "redirect_to": "admin_dashboard" if user.role == "super_admin" else "branch_dashboard",
            })
        return custom_response(False, "Invalid credentials", serializer.errors, status.HTTP_400_BAD_REQUEST)


# =========================================
# CENTER API
# =========================================

@api_view(['GET'])
def center_list(request):
    qs = Center.objects.all().order_by('-id')
    search = request.query_params.get('search')
    if search:
        qs = qs.filter(Q(center_name__icontains=search) | Q(location__icontains=search) | Q(mobile__icontains=search))
    return custom_response(True, "Centers fetched successfully", CenterSerializer(qs, many=True).data)


@api_view(['POST'])
def center_create(request):
    serializer = CenterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Center created successfully", serializer.data, status.HTTP_201_CREATED)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def center_detail(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        return custom_response(False, "Center not found", None, status.HTTP_404_NOT_FOUND)
    return custom_response(True, "Center fetched successfully", CenterSerializer(center).data)


@api_view(['PUT'])
def center_update(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        return custom_response(False, "Center not found", None, status.HTTP_404_NOT_FOUND)
    serializer = CenterSerializer(center, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Center updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def center_partial_update(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        return custom_response(False, "Center not found", None, status.HTTP_404_NOT_FOUND)
    serializer = CenterSerializer(center, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Center updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def center_delete(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        return custom_response(False, "Center not found", None, status.HTTP_404_NOT_FOUND)
    center.delete()
    return custom_response(True, "Center deleted successfully")


# =========================================
# PLAN API
# =========================================

@api_view(['GET'])
def plan_list(request):
    qs = Plan.objects.all().order_by('-id')
    search = request.query_params.get('search')
    if search:
        qs = qs.filter(plan_name__icontains=search)
    return custom_response(True, "Plans fetched successfully", PlanSerializer(qs, many=True).data)


@api_view(['POST'])
def plan_create(request):
    serializer = PlanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Plan created successfully", serializer.data, status.HTTP_201_CREATED)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def plan_detail(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return custom_response(False, "Plan not found", None, status.HTTP_404_NOT_FOUND)
    return custom_response(True, "Plan fetched successfully", PlanSerializer(plan).data)


@api_view(['PUT'])
def plan_update(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return custom_response(False, "Plan not found", None, status.HTTP_404_NOT_FOUND)
    serializer = PlanSerializer(plan, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Plan updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def plan_partial_update(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return custom_response(False, "Plan not found", None, status.HTTP_404_NOT_FOUND)
    serializer = PlanSerializer(plan, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Plan updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def plan_delete(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return custom_response(False, "Plan not found", None, status.HTTP_404_NOT_FOUND)
    if Invoice.objects.filter(plan=plan).exists():
        return custom_response(False, "Cannot delete plan. It is used in invoices.", None, status.HTTP_400_BAD_REQUEST)
    plan.delete()
    return custom_response(True, "Plan deleted successfully")


# =========================================
# SLOT API
# =========================================

@api_view(['GET'])
def slot_list(request):
    slots = Slot.objects.all().order_by('-id')
    return custom_response(True, "Slots fetched successfully", SlotSerializer(slots, many=True).data)


@api_view(['POST'])
def slot_create(request):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Slot created successfully", serializer.data, status.HTTP_201_CREATED)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def slot_detail(request, pk):
    try:
        slot = Slot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return custom_response(False, "Slot not found", None, status.HTTP_404_NOT_FOUND)
    return custom_response(True, "Slot fetched successfully", SlotSerializer(slot).data)


@api_view(['PUT'])
def slot_update(request, pk):
    try:
        slot = Slot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return custom_response(False, "Slot not found", None, status.HTTP_404_NOT_FOUND)
    serializer = SlotSerializer(slot, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Slot updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def slot_partial_update(request, pk):
    try:
        slot = Slot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return custom_response(False, "Slot not found", None, status.HTTP_404_NOT_FOUND)
    serializer = SlotSerializer(slot, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Slot updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def slot_delete(request, pk):
    try:
        slot = Slot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return custom_response(False, "Slot not found", None, status.HTTP_404_NOT_FOUND)
    slot.delete()
    return custom_response(True, "Slot deleted successfully")


# =========================================
# SLOT BOOKING API
# =========================================

@api_view(['GET'])
def slot_booking_list(request):
    bookings = SlotBooking.objects.all().order_by('-id')
    return custom_response(True, "Slot bookings fetched successfully", SlotBookingSerializer(bookings, many=True).data)


@api_view(['POST'])
def slot_booking_create(request):
    serializer = SlotBookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Slot booking created successfully", serializer.data, status.HTTP_201_CREATED)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def slot_booking_detail(request, pk):
    try:
        booking = SlotBooking.objects.get(pk=pk)
    except SlotBooking.DoesNotExist:
        return custom_response(False, "Slot booking not found", None, status.HTTP_404_NOT_FOUND)
    return custom_response(True, "Slot booking fetched successfully", SlotBookingSerializer(booking).data)


@api_view(['PUT'])
def slot_booking_update(request, pk):
    try:
        booking = SlotBooking.objects.get(pk=pk)
    except SlotBooking.DoesNotExist:
        return custom_response(False, "Slot booking not found", None, status.HTTP_404_NOT_FOUND)
    serializer = SlotBookingSerializer(booking, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Slot booking updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def slot_booking_partial_update(request, pk):
    try:
        booking = SlotBooking.objects.get(pk=pk)
    except SlotBooking.DoesNotExist:
        return custom_response(False, "Slot booking not found", None, status.HTTP_404_NOT_FOUND)
    serializer = SlotBookingSerializer(booking, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Slot booking updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def slot_booking_delete(request, pk):
    try:
        booking = SlotBooking.objects.get(pk=pk)
    except SlotBooking.DoesNotExist:
        return custom_response(False, "Slot booking not found", None, status.HTTP_404_NOT_FOUND)
    booking.delete()
    return custom_response(True, "Slot booking deleted successfully")


# =========================================
# INVOICE API
# =========================================

@api_view(['GET'])
def invoice_list(request):
    qs = Invoice.objects.all().order_by('-id')
    search = request.query_params.get('search')
    center = request.query_params.get('center')
    date = request.query_params.get('date')
    plan = request.query_params.get('plan')
    if search:
        qs = qs.filter(Q(customer__name__icontains=search) | Q(invoice_number__icontains=search))
    if center:
        qs = qs.filter(center_id=center)
    if date:
        qs = qs.filter(date=date)
    if plan:
        qs = qs.filter(plan_id=plan)
    return custom_response(True, "Invoices fetched successfully", InvoiceSerializer(qs, many=True).data)


@api_view(['POST'])
def invoice_create(request):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Invoice created successfully", serializer.data, status.HTTP_201_CREATED)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def invoice_detail(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return custom_response(False, "Invoice not found", None, status.HTTP_404_NOT_FOUND)
    return custom_response(True, "Invoice fetched successfully", InvoiceSerializer(invoice).data)


@api_view(['PUT'])
def invoice_update(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return custom_response(False, "Invoice not found", None, status.HTTP_404_NOT_FOUND)
    serializer = InvoiceSerializer(invoice, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Invoice updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def invoice_partial_update(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return custom_response(False, "Invoice not found", None, status.HTTP_404_NOT_FOUND)
    serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return custom_response(True, "Invoice updated successfully", serializer.data)
    return custom_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def invoice_delete(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return custom_response(False, "Invoice not found", None, status.HTTP_404_NOT_FOUND)
    invoice.delete()
    return custom_response(True, "Invoice deleted successfully")
