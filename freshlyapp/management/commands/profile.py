from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from freshlyapp.models import Profile

class Command(BaseCommand):
    help = 'Create missing Profile objects for existing users'

    def handle(self, *args, **kwargs):
        users_without_profiles = 0
        profiles_created = 0

        # Fetch all user objects
        users = User.objects.all()
        total_users = users.count()
        print(f"Total users: {total_users}")

        for user in users:
            # Check if the user has a related profile object
            if not hasattr(user, 'profile'):
                users_without_profiles += 1
                # Create a profile object for the user with empty fields
                Profile.objects.create(user=user, location='', phone='')
                profiles_created += 1
                print(f"Profile created for user: {user.username}")

        print(f"Total users without profiles: {users_without_profiles}")
        print(f"Profiles created: {profiles_created}")
        print("Profile creation process completed.")
