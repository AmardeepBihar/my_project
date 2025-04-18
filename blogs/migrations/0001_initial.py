# Generated by Django 5.0.7 on 2025-02-26 16:15

import django.db.models.deletion
import tinymce.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=60, unique=True)),
                ('meta_title', models.CharField(blank=True, max_length=70)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=500)),
                ('status', models.CharField(choices=[('new', 'New'), ('in_progress', 'In Progress'), ('resolved', 'Resolved')], default='new', max_length=11)),
            ],
            options={
                'verbose_name': 'Contact Request',
                'verbose_name_plural': 'Contact Requests',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=300)),
                ('job_posted', models.DateField()),
                ('description', models.TextField(max_length=1000)),
                ('application_begin', models.DateField()),
                ('apply_before', models.DateField()),
                ('application_fee', models.TextField()),
                ('age_limit', models.TextField()),
                ('total_post', models.CharField(max_length=100)),
                ('how_to_fill', models.TextField()),
                ('apply_url', models.URLField(default='None')),
                ('post_detail', models.FileField(blank=True, null=True, upload_to='jobs/job_post_details/')),
                ('notification', models.FileField(blank=True, null=True, upload_to='jobs/job_notifications/')),
                ('slug', models.SlugField(default='', unique=True)),
                ('meta_title', models.CharField(blank=True, max_length=100, null=True)),
                ('meta_keyword', models.CharField(blank=True, max_length=100, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(choices=[('EN', 'English'), ('HI', 'Hindi')], max_length=2, unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='Purpose',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(max_length=100)),
                ('slug', models.SlugField(max_length=60, unique=True)),
            ],
            options={
                'verbose_name': 'Purpose',
                'verbose_name_plural': 'Purposes',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blog_title_or_question', models.CharField(blank=True, max_length=300, null=True)),
                ('overall_experience', models.IntegerField(choices=[(5, 'Excellent'), (4, 'Good'), (3, 'Average'), (2, 'Poor'), (1, 'Very Poor')], default=5)),
                ('content_quality', models.IntegerField(choices=[(5, 'Excellent'), (4, 'Good'), (3, 'Average'), (2, 'Poor'), (1, 'Very Poor')], default=5)),
                ('design_quality', models.IntegerField(choices=[(5, 'Excellent'), (4, 'Good'), (3, 'Average'), (2, 'Poor'), (1, 'Very Poor')], default=5)),
                ('issue_type', models.CharField(choices=[('design', 'Design Problem'), ('content', 'Content Error'), ('technical', 'Technical Issue'), ('other', 'Other'), ('None', 'None')], default='None', max_length=15)),
                ('description_of_issue', models.TextField(blank=True, max_length=300)),
                ('additional_comment', models.TextField(blank=True, max_length=300)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Feedback',
                'verbose_name_plural': 'User Feedback',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=100)),
                ('slug', models.SlugField(max_length=70, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='blogs.category')),
            ],
            options={
                'verbose_name': 'Subcategory',
                'verbose_name_plural': 'Subcategories',
                'unique_together': {('category', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('content', tinymce.models.HTMLField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=9)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('featured_image', models.ImageField(upload_to='blogs/images/%Y/%m/')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='blogs/pdfs/%Y/%m/')),
                ('meta_title', models.CharField(blank=True, max_length=70)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('meta_keyword', models.CharField(blank=True, max_length=225)),
                ('slug', models.SlugField(max_length=110, unique=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authorby', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categoryby', to='blogs.category')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='languageby', to='blogs.language')),
            ],
            options={
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Posts',
                'indexes': [models.Index(fields=['slug', 'status'], name='blogs_blog_slug_5a4154_idx'), models.Index(fields=['created_at', 'status'], name='blogs_blog_created_a8bbcf_idx')],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.TextField(max_length=300)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('option1', models.CharField(max_length=50, null=True)),
                ('option2', models.CharField(max_length=50, null=True)),
                ('option3', models.CharField(max_length=50, null=True)),
                ('option4', models.CharField(max_length=50, null=True)),
                ('correct_answer', models.CharField(max_length=50)),
                ('explanation', tinymce.models.HTMLField()),
                ('difficulty', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=6)),
                ('meta_title', models.CharField(blank=True, max_length=70)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('meta_keyword', models.CharField(blank=True, max_length=225)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_wise_questions', to='blogs.category')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogs.language')),
                ('purpose', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purpose_wise_questions', to='blogs.purpose')),
                ('sub_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_catetory_wise_questions', to='blogs.subcategory')),
            ],
            options={
                'verbose_name': 'MCQ Question',
                'verbose_name_plural': 'MCQ Questions',
                'indexes': [models.Index(fields=['slug', 'difficulty'], name='blogs_quest_slug_0aab35_idx'), models.Index(fields=['category', 'sub_category'], name='blogs_quest_categor_c365af_idx')],
            },
        ),
    ]
