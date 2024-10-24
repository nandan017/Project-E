from django.contrib import admin
from .models import Vote

class VoteAdmin(admin.ModelAdmin):
    # Define the fields to display in the admin list view
    list_display = ('student_id', 'timestamp', 'hash', 'previous_hash')

# Register the Vote model with the customized admin class
admin.site.register(Vote, VoteAdmin)
