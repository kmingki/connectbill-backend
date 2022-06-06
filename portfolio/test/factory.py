'''
from connectBill.models import User
import factory
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    user_id = 'test_user'
    user_pw = 'testuserpassword'
    user_name = 'testuser'
    user_role = 'client'
    user_email = 'testuser@test.com'
'''