from django.test import TestCase, Client
from django.urls import reverse

# basic smoke tests for the newly added feedback "featured" feature
from .models import Feedback

class FeedbackFeatureTests(TestCase):
	def setUp(self):
		self.client = Client()
		# create a sample feedback entry
		self.feedback = Feedback.objects.create(
			name='Tester',
			email='tester@example.com',
			mobile_number='9999999999',
			rating=4,
			feedback='Sample feedback'
		)

	def test_toggle_featured_view(self):
		# toggling should flip the boolean and redirect back
		url = reverse('feedback:toggle_featured_feedback', args=[self.feedback.id])
		resp = self.client.post(url)
		self.feedback.refresh_from_db()
		self.assertTrue(self.feedback.featured)
		# second POST should unset
		resp = self.client.post(url)
		self.feedback.refresh_from_db()
		self.assertFalse(self.feedback.featured)

	def test_homepage_includes_featured_feedback(self):
		# mark as featured and load the index page
		self.feedback.featured = True
		self.feedback.save()
		resp = self.client.get(reverse('user_panel:index'))
		self.assertEqual(resp.status_code, 200)
		# testimonial heading should appear
		self.assertContains(resp, 'Hear <i>from them</i>')
		# feedback text must appear
		self.assertContains(resp, 'Sample feedback')


class LoginValidationTests(TestCase):
	"""Ensure the admin login form only accepts an email address."""

	def setUp(self):
		self.client = Client()
		# create user with known email/username
		self.user = User.objects.create_user(
			username='supercreator',
			email='admin@whitehouse.com',
			password='admin123'
		)

	def test_successful_login_with_email(self):
		resp = self.client.post(reverse('admin_panel:login'), {
			'email': 'admin@whitehouse.com',
			'password': 'admin123'
		})
		# login should redirect to otp verification page
		self.assertRedirects(resp, reverse('admin_panel:verify_otp'))

	def test_fails_with_username(self):
		resp = self.client.post(reverse('admin_panel:login'), {
			'email': 'supercreator',
			'password': 'admin123'
		})
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'Invalid credentials')

	def test_otp_flow_and_verification(self):
		# successful login should generate an OTP and redirect to verify page
		resp = self.client.post(reverse('admin_panel:login'), {
			'email': 'admin@whitehouse.com',
			'password': 'admin123'
		})
		self.assertRedirects(resp, reverse('admin_panel:verify_otp'))
		# OTP stored in session
		otp = self.client.session.get('admin_otp')
		self.assertIsNotNone(otp)
		self.assertEqual(self.client.session.get('admin_username'), 'supercreator')

		# wrong OTP shows error and does not log in
		resp2 = self.client.post(reverse('admin_panel:verify_otp'), {'otp': '000000'})
		self.assertEqual(resp2.status_code, 200)
		self.assertContains(resp2, 'Invalid OTP')
		self.assertIsNone(self.client.session.get('admin_logged_in'))

		# correct OTP redirects to dashboard and sets login flag
		resp3 = self.client.post(reverse('admin_panel:verify_otp'), {'otp': str(otp)})
		self.assertRedirects(resp3, reverse('admin_panel:dashboard'))
		self.assertTrue(self.client.session.get('admin_logged_in'))

	def test_case_insensitive_email_login(self):
		# uppercase email should still work
		resp = self.client.post(reverse('admin_panel:login'), {
			'email': 'ADMIN@WHITEHOUSE.COM',
			'password': 'admin123'
		})
		self.assertRedirects(resp, reverse('admin_panel:verify_otp'))
	def test_resend_otp_replaces_previous_code(self):
		# initiate login to set session values
		self.client.post(reverse('admin_panel:login'), {
			'email': 'admin@whitehouse.com',
			'password': 'admin123'
		})
		first_otp = self.client.session.get('admin_otp')
		# call resend endpoint
		self.client.get(reverse('resend_otp'))
		second_otp = self.client.session.get('admin_otp')
		self.assertIsNotNone(second_otp)
		self.assertNotEqual(first_otp, second_otp)

