from django.contrib import admin
from .models import Candidate, Vote, BlockchainCode, Profile, Election

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'election', 'votes')  # Display vote count in admin list view
    readonly_fields = ('votes',)  # Make vote count field read-only
    actions = None  # Disable actions for this model

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate')  # Display user and candidate in admin list view
    readonly_fields = ('user', 'candidate')  # Make vote and user fields read-only
    actions = None  # Disable actions for this model

class BlockchainCodeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False  # Disable adding blockchain codes through the admin interface

    def has_change_permission(self, request, obj=None):
        return False  # Disable changing existing blockchain codes

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(BlockchainCode, BlockchainCodeAdmin)
admin.site.register(Profile)
admin.site.register(Election)
