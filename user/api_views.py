from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.db.models import Q
from django.db import models

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
        is_admin = request.query_params.get('is_admin') == 'true'
        is_branch = request.query_params.get('is_branch') == 'true'

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            if is_admin and user.role != 'super_admin':
                return custom_response(False, "Access denied. Not an admin.", None, status.HTTP_403_FORBIDDEN)

            if is_branch and user.role != 'branch_user':
                return custom_response(False, "Access denied. Not a branch user.", None, status.HTTP_403_FORBIDDEN)

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
# DASHBOARD API
# =========================================

@api_view(['GET'])
def dashboard_summary(request):
    from django.db.models import Sum, Count
    from django.utils import timezone
    from datetime import date

    today = date.today()
    this_month_start = today.replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    # Totals
    total_customers = Customer.objects.count()
    total_invoice_amount = Invoice.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_sessions = Slot.objects.count()
    total_booked = Slot.objects.aggregate(total=Sum('booked_count'))['total'] or 0
    total_capacity = Slot.objects.aggregate(total=Sum('total_slot'))['total'] or 0
    booking_rate = round((total_booked / total_capacity * 100), 2) if total_capacity > 0 else 0
    booking_rate = min(booking_rate, 100)

    # This month
    customers_this_month = Customer.objects.filter(created_at__date__gte=this_month_start).count()
    invoice_this_month = Invoice.objects.filter(date__gte=this_month_start).aggregate(total=Sum('amount'))['total'] or 0
    sessions_this_month = Slot.objects.filter(created_at__date__gte=this_month_start).count()
    booked_this_month = SlotBooking.objects.filter(booking_date__gte=this_month_start).count()
    capacity_this_month = Slot.objects.filter(created_at__date__gte=this_month_start).aggregate(total=Sum('total_slot'))['total'] or 0
    booking_rate_this_month = round((booked_this_month / capacity_this_month * 100), 2) if capacity_this_month > 0 else 0

    # Last month
    customers_last_month = Customer.objects.filter(created_at__date__gte=last_month_start, created_at__date__lte=last_month_end).count()
    invoice_last_month = Invoice.objects.filter(date__gte=last_month_start, date__lte=last_month_end).aggregate(total=Sum('amount'))['total'] or 0
    sessions_last_month = Slot.objects.filter(created_at__date__gte=last_month_start, created_at__date__lte=last_month_end).count()
    booked_last_month = SlotBooking.objects.filter(booking_date__gte=last_month_start, booking_date__lte=last_month_end).count()
    capacity_last_month = Slot.objects.filter(created_at__date__gte=last_month_start, created_at__date__lte=last_month_end).aggregate(total=Sum('total_slot'))['total'] or 0
    booking_rate_last_month = round((booked_last_month / capacity_last_month * 100), 2) if capacity_last_month > 0 else 0

    def growth(current, previous):
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round((current - previous) / previous * 100, 2)

    return Response({
        'total_customers': total_customers,
        'total_invoice_amount': total_invoice_amount,
        'total_sessions': total_sessions,
        'booking_rate': booking_rate,
        'customer_growth': growth(customers_this_month, customers_last_month),
        'invoice_growth': growth(float(invoice_this_month), float(invoice_last_month)),
        'session_growth': growth(sessions_this_month, sessions_last_month),
        'booking_rate_growth': growth(booking_rate_this_month, booking_rate_last_month),
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def dashboard_centerwise_performance(request):
    from django.db.models import Sum, Count

    centers = Center.objects.all()
    result = []

    for center in centers:
        customer_count = Customer.objects.filter(center=center).count()
        revenue = Invoice.objects.filter(center=center).aggregate(total=Sum('amount'))['total'] or 0
        slots = Slot.objects.filter(center=center)
        total_slots = slots.aggregate(total=Sum('total_slot'))['total'] or 0
        total_booked = slots.aggregate(total=Sum('booked_count'))['total'] or 0
        booking_rate = round((total_booked / total_slots * 100), 2) if total_slots > 0 else 0
        booking_rate = min(booking_rate, 100)

        result.append({
            'center_id': center.id,
            'center_name': center.center_name,
            'customers': customer_count,
            'booking_rate': booking_rate,
            'revenue': float(revenue),
        })

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def dashboard_revenue_overview(request):
    from django.db.models import Sum
    from datetime import date

    today = date.today()
    labels = []
    values = []

    for i in range(6, -1, -1):
        # calculate month going back i months from current
        month = today.month - i
        year = today.year
        while month <= 0:
            month += 12
            year -= 1

        revenue = Invoice.objects.filter(
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        labels.append(date(year, month, 1).strftime('%b'))
        values.append(float(revenue))

    return Response({'labels': labels, 'values': values}, status=status.HTTP_200_OK)


@api_view(['GET'])
def dashboard_membership_status(request):
    from django.db.models import Count

    plans = Plan.objects.all()
    result = []
    for plan in plans:
        customer_count = Customer.objects.filter(plan=plan).count()
        result.append({
            'plan_name': plan.plan_name,
            'customer_count': customer_count,
        })

    return Response(result, status=status.HTTP_200_OK)


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


# =========================================
# BRANCH DASHBOARD API
# =========================================

@api_view(['GET'])
def branch_dashboard(request):
    from django.utils import timezone
    from django.db.models import Count

    today = timezone.now().date()

    # Get center_id from query param or from logged-in user
    center_id = request.query_params.get('center_id')
    if not center_id and hasattr(request.user, 'center') and request.user.center:
        center_id = request.user.center.id

    if not center_id:
        return custom_response(False, "center_id is required", None, status.HTTP_400_BAD_REQUEST)

    try:
        center = Center.objects.get(pk=center_id)
    except Center.DoesNotExist:
        return custom_response(False, "Center not found", None, status.HTTP_404_NOT_FOUND)

    # Today's slots for this center
    slots = Slot.objects.filter(center=center)
    total_slots = slots.aggregate(total=models.Sum('total_slot'))['total'] or 0
    booked_today = SlotBooking.objects.filter(slot__center=center, booking_date=today).count()
    free_slots = total_slots - booked_today
    booking_rate = round((booked_today / total_slots * 100), 1) if total_slots > 0 else 0

    # Most purchased plan
    most_purchased = (
        Invoice.objects.filter(center=center)
        .values('plan__plan_name')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )
    most_purchased_plan = most_purchased['plan__plan_name'] if most_purchased else None

    # Today's slots detail
    today_slots = []
    for slot in slots.order_by('start_time'):
        booking = SlotBooking.objects.filter(slot=slot, booking_date=today).select_related('customer').first()
        today_slots.append({
            "id": slot.id,
            "start_time": slot.start_time.strftime('%I:%M %p'),
            "end_time": slot.end_time.strftime('%I:%M %p'),
            "status": "booked" if booking else "available",
            "customer_name": booking.customer.name if booking else None,
        })

    # Recent customers
    recent_customers = Customer.objects.filter(center=center).order_by('-created_at')[:10]
    recent_customers_data = []
    for c in recent_customers:
        diff = (today - c.created_at.date()).days
        if diff == 0:
            joined = "Today"
        elif diff == 1:
            joined = "Yesterday"
        else:
            joined = c.created_at.strftime('%d %b %Y')
        recent_customers_data.append({
            "id": c.id,
            "name": c.name,
            "plan": c.plan,
            "joined": joined,
        })

    return custom_response(True, "Branch dashboard fetched successfully", {
        "center_name": center.center_name,
        "center_email": center.email,
        "stats": {
            "slots_booked_today": booked_today,
            "total_slots": total_slots,
            "free_slots": free_slots,
            "booking_rate": f"{booking_rate}%",
            "most_purchased_plan": most_purchased_plan,
        },
        "today_slots": today_slots,
        "recent_customers": recent_customers_data,
    })
