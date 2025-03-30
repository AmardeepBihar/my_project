from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Blog, Jobs, Category, SubCategory, Purpose, Question


# 1️⃣ Static Sitemap for Static Pages
class StaticSitemap(Sitemap):
    priority = 1.00
    changefreq = "daily"

    def items(self):
        return [
            'blogs', 'contact', 'about', 'privacyandpolicy',
            'declaration', 'test-series', 'sub-category-test'
        ]

    def location(self, item):
        return reverse(item)

# 2️⃣ Blog Sitemap
class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Blog.objects.all()

    def location(self, item):
        return reverse('blog_post_detail', args=[item.slug])


# 3️⃣ Job Sitemap
class JobsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Jobs.objects.all()

    def location(self, item):
        return reverse('job_post_detail', args=[item.slug])


# 4️⃣ Category Sitemap
class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def location(self, item):
        return reverse('category', args=[item.slug])


# 5️⃣ Sub-Category Sitemap
class SubCategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return SubCategory.objects.all()

    def location(self, item):
        return reverse('sub-category-wise-question', args=[item.slug])


# 6️⃣ Purpose Sitemap
class PurposeSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Purpose.objects.all()

    def location(self, item):
        return reverse('purpose-wise-question', args=[item.slug])


# 7️⃣ Question Sitemap
class QuestionSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Question.objects.all()

    def location(self, item):
        return reverse('ansthequestion', args=[item.uid, item.slug])  # Use UUID for unique URL

