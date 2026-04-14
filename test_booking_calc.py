from datetime import date

today = date(2026, 4, 14)
booking_labels, booked_values, free_values = [], [], []
total_capacity = 40

for i in range(6, -1, -1):
    month = today.month - i
    year = today.year
    while month <= 0:
        month += 12
        year -= 1
    
    # Simulate bookings (6 in April, 0 in others)
    month_bookings = 6 if (year == 2026 and month == 4) else 0
    
    # Calculate free slots
    free = max(total_capacity - month_bookings, 0)
    
    booking_labels.append(date(year, month, 1).strftime('%b'))
    booked_values.append(month_bookings)
    free_values.append(free)

print('Labels:', booking_labels)
print('Booked:', booked_values)
print('Free:', free_values)
