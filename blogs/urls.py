from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.conf.urls.static import static 
from django.views.generic.base import TemplateView

# Import sitemaps
from .sitemaps import (
    StaticSitemap, BlogSitemap, JobsSitemap,
    CategorySitemap, SubCategorySitemap, PurposeSitemap,
    QuestionSitemap
)

# Admin Customization
admin.site.site_header = 'CRAMPT Administration'
admin.site.site_title = "CRAMPT Login"
admin.site.index_title = 'Welcome to this Crampt.in'

# Define sitemaps dictionary
sitemaps = {
    'static': StaticSitemap,                  # Static pages like about, contact, etc.
    'blogs': BlogSitemap,                     # Blog detail pages
    'jobs': JobsSitemap,                      # Job detail pages
    'categories': CategorySitemap,            # Categories
    'sub_categories': SubCategorySitemap,     # Sub-categories
    'purposes': PurposeSitemap,               # Purposes
    'questions': QuestionSitemap,             # Questions
}

# Define urlpatterns
urlpatterns = [
    # Job-related URLs
    path('vacancies', views.JobPostsList, name='joblist'),
    path('job-post-detail/<slug:slug>', views.JobPostInDetail, name='job_post_detail'),

    # Blog-related URLs
    path('', views.Blogs, name='blogs'),
    path('post/<slug:slug>/', views.BlogDetail, name='blog_post_detail'),

    # Category-related URLs
    path('category/<slug:slug>/', views.Categories, name='category'),
    path('category-wise-question/<slug:slug>/', views.CategoriesWiseQuestion, name='category-wise-question'),

    # Sub-category-related URLs
    path('all-sub-category-test/', views.SubCategoryList, name='sub-category-test'),
    path('sub-category-wise-question/<slug:slug>/', views.SubCategoryWiseQuestion, name='sub-category-wise-question'),

    # Purpose-related URLs
    path('purpose-wise-question/<slug:slug>/', views.PurposeWiseQuestion, name='purpose-wise-question'),

    # Test Series and Practice URLs
    path('all-test-series/', views.TestSeriesList, name='test-series'),
    path('endpractice/', views.ResultView, name='endpractice'),
    path('update-session-results/', views.UpdateSessionResults, name='update-session-results'),

    # Question-related URLs
    path('question/<uuid:uid>/<slug:slug>', views.RandomQuestion, name='ansthequestion'),

    # Universal Search URL ✅
    path('search-result', views.UniversalSearch, name='searched_universaly'),

    # Static Pages URLs
    path('contact/', views.Contact, name='contact'),
    path('about/', views.About, name='about'),
    path('declaration/', views.DeclarationPage, name='declaration'),
    path('privacy-policy/', views.PrivacyPolicy, name='privacyandpolicy'),
    path('feedback/', views.Feedback, name='feedback'),

    # Author URL
    path('author', views.AuthorDetail, name='author_detail'),

    # Sitemap URL
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robot.txt',content_type="text/plain"), name='robots_txt'),
    # Admin URL
    path('admin/', admin.site.urls),
]
