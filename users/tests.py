from django.test import TestCase
from users.models import User
from locations.models import Area, Govern


# Create your tests here.
class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test User', username='testuser', gender='Male', credits=0)

    def test_refund_credits(self):
        user_balance = self.user.credits
        balance_to_add = 200
        self.user.refund_credits(balance_to_add)
        
        self.assertEqual(self.user.credits, balance_to_add + user_balance)
        
    
    def test_deduct_credits_exist(self):
        self.user.credits = 200
        user_balance = self.user.credits
        balance_to_deduct = 100
        self.user.deduct_credits(balance_to_deduct)
        
        self.assertEqual(self.user.credits, user_balance - balance_to_deduct)
    
    def test_deduct_credits_not_enough(self):
        self.user.credits = 50        
        with self.assertRaises(ValueError):
            self.user.deduct_credits(self.user.credits + 2)
    
    def test_update_notification_token(self):
        token = 'Hello'
        self.user.update_notification_token(token)
        
        self.assertEqual(self.user.notification_token, token)
    
    def test_remove_notification_token(self):
        self.user.remove_notification_token()
        self.assertIsNone(self.user.notification_token)