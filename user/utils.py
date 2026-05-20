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
