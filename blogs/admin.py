from django.contrib import admin
from .models import Blog, Category, ContactRequest, Feedback, Question, Purpose, Language, SubCategory,Jobs
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html


# Register the Language, Purpose, and SubCategory models
admin.site.register(Language)
admin.site.register(SubCategory)

class PurposeAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('title','total_time','questions_count','created_at')
    list_filter = ('title','created_at')
    search_fields = ('title','total_time','created_at')
admin.site.register(Purpose,PurposeAdmin)


class JobsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('job_posted','job_title', 'application_begin','apply_before','application_fee', 'total_post')  # Corrected list_display
    list_filter = ('job_posted','application_begin','apply_before')
    search_fields = ('job_posted','job_title', 'application_begin','apply_before','application_fee', 'total_post')
admin.site.register(Jobs, JobsAdmin)

# --- Blog Admin ---
class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("title", "category", 'author', "published_date", "status")
    prepopulated_fields = {"slug": ["title"]}
    list_filter = ('category', 'author', 'language', 'status', 'created_at')  # Use created_at instead of published_date
    search_fields = ['title', 'category__name', 'author__username', 'content']

    def published_date(self, obj):
        return obj.created_at  # This method just displays created_at as "Published Date"
    published_date.admin_order_field = 'created_at'
    published_date.short_description = 'Published Date'
admin.site.register(Blog, BlogAdmin)

# --- Question Admin ---
@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('question', 'category', 'sub_category', 'language', 'purpose', 'difficulty', 'slug')
    list_filter = ('purpose', 'category', 'sub_category', 'language', 'difficulty')
    search_fields = ('question', 'category__name', 'sub_category__name', 'purpose__title', 'language__name')
    prepopulated_fields = {"slug": ['question']}
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('purpose', 'category', 'sub_category', 'language')

# --- Category Admin ---
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ['name']
    search_fields = ['name']
    prepopulated_fields = {"slug": ["name"]}
admin.site.register(Category, CategoryAdmin)

# --- Feedback Admin ---
class FeedbackAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["overall_experience", "content_quality", "design_quality", "issue_type", "created_at"]
    list_filter = ['overall_experience', 'content_quality', 'design_quality', 'issue_type', 'created_at']
    search_fields = ['user__username', 'additional_comment', 'improvement_suggestions', 'description_of_issue']
admin.site.register(Feedback, FeedbackAdmin)

# --- ContactRequest Admin ---
class ContactQueryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("subject", "name", "email", "status", "created_at")
    list_filter = ['status', 'created_at']
    search_fields = ["subject", "name", "email", "message"]
admin.site.register(ContactRequest, ContactQueryAdmin)

# Adding proper admin configuration for `User` model (for foreign key relations like Blog author)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
