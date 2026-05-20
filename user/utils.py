from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(customer):
    """Send welcome email to new customer"""
    
    subject = f'Welcome to {settings.PROJECT_NAME}'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #4CAF50;">Hi {customer.name},</h2>
            <p>Welcome to <strong>{settings.PROJECT_NAME}</strong></p>
            <p>Your account has been successfully registered.</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Here are your account details:</h3>
                <p><strong>Name:</strong> {customer.name}</p>
                <p><strong>Email:</strong> {customer.email}</p>
                <p><strong>Mobile:</strong> {customer.mobile}</p>
                <p><strong>Center:</strong> {customer.center.center_name if customer.center else 'N/A'}</p>
                <p><strong>Plan:</strong> {customer.plan.plan_name if customer.plan else 'N/A'}</p>
            </div>
            
            
            <p style="margin-top: 30px; color: #666; font-size: 14px;">
                If you did not create this account, please ignore this email or contact our support team.
            </p>
            
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            
            <p style="color: #666; font-size: 14px;">
                Thank you,<br>
                <strong>Team {settings.PROJECT_NAME}</strong>
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
Hi {customer.name},

Welcome to {settings.PROJECT_NAME}

Your account has been successfully registered.

Here are your account details:
Name: {customer.name}
Email: {customer.email}
Mobile: {customer.mobile}
Center: {customer.center.center_name if customer.center else 'N/A'}
Plan: {customer.plan.plan_name if customer.plan else 'N/A'}


If you did not create this account, please ignore this email or contact our support team.

Thank you,
Team {settings.PROJECT_NAME}
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_slot_booking_email(booking):
    """Send slot booking confirmation email to customer"""
    
    customer = booking.customer
    
    if not customer.email:
        return False
    
    subject = f'Slot Booking Confirmation - {settings.PROJECT_NAME}'
    
    # HTML email content
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #4CAF50;">Hi {customer.name},</h2>
            <p>Your slot has been <strong>successfully booked</strong>! 🎉</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Booking Details:</h3>
                <p><strong>Booking ID:</strong> #{booking.id}</p>
                <p><strong>Date:</strong> {booking.booking_date.strftime('%d/%m/%Y')}</p>
                <p><strong>Time:</strong> {booking.slot.start_time.strftime('%I:%M %p')} - {booking.slot.end_time.strftime('%I:%M %p')}</p>
                <p><strong>Center:</strong> {booking.center.center_name if booking.center else 'N/A'}</p>
                <p><strong>Status:</strong> {booking.status.upper()}</p>
            </div>
            
            <p style="margin-top: 30px; color: #666; font-size: 14px;">
                Please arrive 10 minutes before your scheduled time.
            </p>
            
            <p style="margin-top: 30px; color: #666; font-size: 14px;">
                If you need to reschedule or cancel, please contact us.
            </p>
            
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            
            <p style="color: #666; font-size: 14px;">
                Thank you,<br>
                <strong>Team {settings.PROJECT_NAME}</strong>
            </p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version (fallback)
    plain_message = f"""
Hi {customer.name},

Your slot has been successfully booked!

Booking Details:
Booking ID: #{booking.id}
Date: {booking.booking_date.strftime('%d/%m/%Y')}
Time: {booking.slot.start_time.strftime('%I:%M %p')} - {booking.slot.end_time.strftime('%I:%M %p')}
Center: {booking.center.center_name if booking.center else 'N/A'}
Status: {booking.status.upper()}

Please arrive 10 minutes before your scheduled time.

If you need to reschedule or cancel, please contact us.

Thank you,
Team {settings.PROJECT_NAME}
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending booking email: {str(e)}")
        return False
