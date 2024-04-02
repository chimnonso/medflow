from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib import messages


# Import your forms if you're going to test form validation
from .forms import CreationForm, LoginForm

User = get_user_model()

class RegisterUserTests(TestCase):
    def test_register_page_url(self):
        response = self.client.get("/accounts/register/")  # Adjust the URL as needed
        self.assertEqual(response.status_code, 200)

    def test_register_user_with_valid_data(self):
        response = self.client.post("/accounts/register/", {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'PA',
            # Add other fields as necessary
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_register_user_with_invalid_data(self):
        response = self.client.post("/accounts/register/", {})
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)  # Page reloads with form errors



class LoginUserTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.login_url = reverse('accounts:login')  # Replace 'your_login_url_name' with the actual name of your login view in urls.py

    def test_login_success(self):
        # Test login with valid credentials
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'}, follow=True)
        # Check that the user was redirected to the correct page
        self.assertRedirects(response, reverse('pages:index'))
        # Check for success message
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertIn('Welcome back testuser', str(messages_list[0]))

    def test_login_invalid_credentials(self):
        # Test login with invalid credentials
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'}, follow=True)
        # Check that the response contains an error message
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertIn('Invalid Credentials. Login Unsuccessful. Contact Admin', str(messages_list[0]))
        # Ensure that the login template was used for the response
        self.assertTemplateUsed(response, 'accounts/registration/login.html')

    def test_login_redirects_next_parameter(self):
        # Test that the 'next' parameter is respected
        next_page = reverse('pages:index')  # Replace 'some_other_view' with a valid view name
        response = self.client.post(f"{self.login_url}?next={next_page}", {'username': 'testuser', 'password': 'testpassword'}, follow=True)
        self.assertRedirects(response, next_page)

    
