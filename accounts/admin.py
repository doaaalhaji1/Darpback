from django.contrib import admin
from .models import User
from .models import User, PassengerProfile

class PassengerProfileInline(admin.StackedInline):

    model = PassengerProfile

    extra = 0

    can_delete = False

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'phone',
        'user_type',
        'gender'
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'phone'
    )

    list_filter = (
        'user_type',
    )

    inlines = [
        PassengerProfileInline
    ]

    def gender(self, obj):

        if hasattr(obj, 'passengerprofile'):
            return obj.passengerprofile.gender

        return '-'