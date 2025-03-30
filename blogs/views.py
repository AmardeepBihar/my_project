from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.http import Http404
from .models import Blog,Category,SubCategory,ContactRequest,Feedback,Question,Purpose,Jobs
from .forms import FeedbackForm,ContactRequestForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone
import random
from django.db.models import Q
from django.http import Http404
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def Blogs(request):
    today = timezone.now().date()
    # Assuming 'created_at' is the correct field instead of 'published_date'
    blog_posts = Blog.objects.exclude(created_at__date=today).order_by('-created_at')
    # Adjust to use 'created_at' or another field, if necessary
    slides = Blog.objects.filter(created_at__date=today)
    pag = Paginator(blog_posts, 6)  # Paginator method
    page = request.GET.get('page')
    pages = pag.get_page(page)
    cat_manu = Category.objects.all()
    template = 'blog/index.html'
    data = {'cat_manu': cat_manu,'pages': pages, 'slides': slides}
    return render(request, template, data)

def BlogDetail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    cat_manu = Category.objects.all()
    # Change 'published_date' to 'created_at' for sorting
    excluded_blog = Blog.objects.exclude(uid=blog.uid).order_by('-created_at')[:5]  # Corrected line
    all_blogs = Blog.objects.all()
    random_blogs = random.sample(list(all_blogs), min(5, len(all_blogs)))  # For showing random blog
    template = 'blog/blog_detail.html'
    data = {'blog':blog, 'excluded_blog': excluded_blog, 'cat_manu': cat_manu, 'random_blogs': random_blogs}
    return render(request, template, data)
#quiz related view
def TestSeriesList(request):
    search_query = request.POST.get('search', '') 
    # Filter the Purpose model based on search query if provided
    if search_query:
        # Filter by title or description containing the search query
        test_series_list = Purpose.objects.filter(
            title__icontains=search_query
        ) | Purpose.objects.filter(
            description__icontains=search_query
        )
    else:
        # If no search query, get all test series
        test_series_list = Purpose.objects.all()
    
    # Get all questions for random selection and count
    all_mcq = Question.objects.all()
    num = all_mcq.count()
    next_question = random.choice(all_mcq) if num > 0 else None

    # Pagination
    pag = Paginator(test_series_list, 20)  # Paginate with 20 items per page
    page = request.GET.get('page')
    pages = pag.get_page(page)
    
    # Get categories for display (assuming you need them)
    cat_manu = Category.objects.all()
    
    # Prepare the data context for rendering the template
    data = {
        'test_series_list': test_series_list,
        'pages': pages,
        'cat_manu': cat_manu,
        'random_question': next_question,
        'total_question': num,
        'search_query': search_query,  # Include search query for maintaining search term
    }
    
    # Render the final template with the provided context
    return render(request, 'mcq/test-series-list.html', data)

def CategoriesWiseQuestion(request, slug):
    category = get_object_or_404(Category, slug=slug)
    questions = category.category_wise_questions.all()  # Adjusted to access the related questions
    current_question_id = request.GET.get('current_question', 0)
    try:
        current_question_id = int(current_question_id)
    except (ValueError, TypeError):  
        current_question_id = 0
    if current_question_id >= len(questions):
        return redirect('endpractice')  # Handle the end of practice
    next_question = questions[current_question_id]
    # Prepare options based on the updated model
    options = [next_question.option1, next_question.option2, next_question.option3, next_question.option4]
    random.shuffle(options)  # Randomize the order of options
    request.session['current_question'] = current_question_id
    if request.method == 'POST':
        selected_answer = request.POST.get('mcq_option')
        request.session['selected_answer'] = selected_answer
        
        # Save if the selected answer is correct or incorrect
        if selected_answer == getattr(next_question, next_question.correct_answer):  # Compare with the correct option
            request.session['is_answer_correct'] = True
        else:
            request.session['is_answer_correct'] = False

    next_question_id = current_question_id + 1
    cat_manu = Category.objects.all()
    
    template = 'mcq/categorywisequestion.html'
    
    return render(request, template, {
        'category': category,
        'cat_manu': cat_manu,
        'next_question': next_question,
        'options': options,
        'next_question_id': next_question_id,
        'selected_answer': request.session.get('selected_answer', None),
        'is_answer_correct': request.session.get('is_answer_correct', None),
        'explanation': next_question.explanation,  # Provide the explanation if needed
        'difficulty': next_question.difficulty,  # Provide the difficulty level
    })

def SubCategoryList(request):
    # Fetch all categories
    categories = Category.objects.all()
    
    # Get the search query from POST request
    search_query = request.POST.get('search', '')
    
    if search_query:
        # Filter subcategories based on name, description, or category title (if necessary)
        sub_categories_list = SubCategory.objects.filter(
            name__icontains=search_query
        ) | SubCategory.objects.filter(
            description__icontains=search_query
        ) | SubCategory.objects.filter(
            category__name__icontains=search_query  # Filter by category name if needed
        )
    else:
        # If no search query, get all subcategories
        sub_categories_list = SubCategory.objects.all()

    # Initialize a dictionary to store subcategories grouped by category
    category_subcategories = {}
    
    # Group subcategories by their category
    for category in categories:
        subcategories = sub_categories_list.filter(category=category)  # Filter subcategories for each category
        category_subcategories[category] = subcategories

    # Fetch all questions to calculate total number of questions
    all_mcq = Question.objects.all()
    num = all_mcq.count()  # Total number of questions
    next_question = random.choice(all_mcq) if num > 0 else None  # Random question for practice

    # Fetch categories for navigation (if needed)
    cat_manu = Category.objects.all()

    # Prepare context data for the template
    data = {
        'category_subcategories': category_subcategories,  # Grouped subcategories by category
        'cat_manu': cat_manu,
        'random_question': next_question,
        'total_question': num,
        'search_query': search_query  # Pass the search query to the template
    }

    # Return the response with the context data
    return render(request, 'mcq/Subcategory-list.html', data)

def SubCategoryWiseQuestion(request, slug):
    # Fetch the SubCategory by its slug
    subcategory = get_object_or_404(SubCategory, slug=slug)
    # Get all the questions related to the subcategory
    questions = subcategory.sub_catetory_wise_questions.all()  # Access questions related to subcategory
    # Get the current question index from the GET request (defaults to 0)
    current_question_id = request.GET.get('current_question', 0)
    try:
        current_question_id = int(current_question_id)
    except (ValueError, TypeError):  
        current_question_id = 0  
    
    # Check if the current question index exceeds the number of available questions
    if current_question_id >= len(questions):
        return redirect('endpractice')  # Redirect to the end practice page if there are no more questions
    
    # Get the next question based on the current question index
    next_question = questions[current_question_id]
    
    # Prepare the options and shuffle them
    options = [next_question.option1, next_question.option2, next_question.option3, next_question.option4]
    random.shuffle(options)
    
    # Calculate the next question ID
    next_question_id = current_question_id + 1
    
    # Fetch the categories for navigation
    cat_manu = Category.objects.all()
    
    # Template to render
    template = 'mcq/subcategoryewisequestion.html'
    
    # Return the rendered response with the context
    return render(request, template, {
        'subcategory': subcategory,
        'cat_manu': cat_manu,
        'next_question': next_question,  # Pass the current question
        'options': options,  # Pass the shuffled options
        'next_question_id': next_question_id,  # Pass the next question index
    })

def PurposeWiseQuestion(request, slug):
    purpose = get_object_or_404(Purpose, slug=slug)
    questions = purpose.purpose_wise_questions.all()  # Get all questions related to the purpose
    current_question_id = request.GET.get('current_question', 0)
    try:
        current_question_id = int(current_question_id)
    except (ValueError, TypeError):  
        current_question_id = 0  

    if current_question_id >= len(questions):
        return redirect('endpractice')  # If all questions are answered, redirect to end practice
    
    # Get the next question
    next_question = questions[current_question_id]
    options = [next_question.option1, next_question.option2, next_question.option3, next_question.option4]
    random.shuffle(options)
    
     # Meta tag data
    meta_data = {
        'meta_title': purpose.meta_title if purpose.meta_title else f"Practice Test - {purpose.title}",
        'meta_description': purpose.meta_description if purpose.meta_description else f"Test yourself with questions about {purpose.title}.",
        'meta_keyword': purpose.meta_keywords if purpose.meta_keywords else f"{purpose.title}, online test, quiz, practice"
    }
    # Calculate the current question number (1-based index)
    current_question_number = current_question_id + 1

    cat_manu = Category.objects.all()  # Get all categories for the sidebar
    template = 'mcq/purposewisequestion.html'
    
    return render(request, template, {
        'purpose': purpose,
        'meta_data':meta_data,
        'cat_manu': cat_manu,
        'next_question': next_question,  # Pass the current question
        'options': options,  # Pass the shuffled options
        'next_question_id': current_question_id + 1,  # Pass the next question index
        'current_question_number': current_question_number,  # Pass the current question number
        'total_questions': purpose.questions_count  # Pass the total number of questions in the test
    })

def RandomQuestion(request, uid,slug):
    # Fetch the question by UID (use 'uid' here instead of 'uuuid')
    ans = get_object_or_404(Question, uid=uid,slug=slug)  # Assuming 'uid' is the primary key or unique identifier for the question
    all_mcq = Question.objects.exclude(uid=uid,slug=slug)  # Exclude the current question from the list

    # Fetch categories for navigation
    cat_manu = Category.objects.all()

    # If there are no more questions left, redirect to the 'endpractice' page
    if not all_mcq.exists():
        return redirect('endpractice')  # Adjust the name of this view as needed

    # Prepare the options and shuffle them
    options = [ans.option1, ans.option2, ans.option3, ans.option4]
    random.shuffle(options)

    # Get the position of the correct answer after shuffling the options
    correct_answer_position = options.index(ans.correct_answer)

    # Get the next random question (if any)
    next_question = random.choice(all_mcq)

    # Initialize session variables if not already present
    if 'attempted_questions' not in request.session:
        request.session['attempted_questions'] = 0
        request.session['correct_answers'] = 0
        request.session['incorrect_answers'] = 0

    # Sample 5 random questions excluding the current one, or all available questions if fewer than 5
    random_questions = random.sample(list(all_mcq), min(5, len(all_mcq)))

    # Prepare data for the template
    data = {
        'ans': ans,
        'next_question': next_question,
        'options': options,
        'correct_answer_position': correct_answer_position,
        'random_question': random_questions,
        'cat_manu': cat_manu,
    }

    # Render the template with the context data
    return render(request, 'mcq/mix-queston.html', data)

@csrf_exempt # this view is only to capture the session of the broweser to make the report of quiz.
def UpdateSessionResults(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_answer = data.get('selected_answer')
        correct_answer = data.get('correct_answer')

        # Initialize session data if not present
        if 'attempted_questions' not in request.session:
            request.session['attempted_questions'] = 0
            request.session['correct_answers'] = 0
            request.session['incorrect_answers'] = 0

        # Increment the attempted questions count
        request.session['attempted_questions'] += 1
        
        # Check if the selected answer is correct and update session accordingly
        if selected_answer == correct_answer:
            request.session['correct_answers'] += 1
        else:
            request.session['incorrect_answers'] += 1
        
        request.session.modified = True  # Ensure the session is saved
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def ResultView(request):
    all_mcq = Question.objects.all()
    next_question = random.choice(all_mcq)
    cat_manu = Category.objects.all()

    # Retrieve session data
    attempted = request.session.get('attempted_questions', 0)
    correct = request.session.get('correct_answers', 0)
    incorrect = request.session.get('incorrect_answers', 0)
    
    print(f"Session Data - Attempted: {attempted}, Correct: {correct}, Incorrect: {incorrect}")

    # Calculate the percentage
    percentage = (correct / attempted * 100) if attempted > 0 else 0

    result = {
        'attempted': attempted,
        'correct': correct,
        'incorrect': incorrect,
        'percentage': percentage,
        'next_question': next_question,
        'cat_manu': cat_manu
    }
    
    # Reset session after showing result
    request.session.flush()
    
    return render(request, 'mcq/result.html', result)


    post = get_object_or_404(BlogsModel,slug=slug)
    post.delete()
    messages.info(request,'Post deleted successful.')
    return redirect('home')

def Categories(request,slug):
    catogere = get_object_or_404(Category,slug=slug)
    post = catogere.categoryby.all() #here posts is the related field of blog model.
    p = Paginator(post,6)  #pagination applied
    page = request.GET.get('page')
    pages = p.get_page(page)
    cat_manu = Category.objects.all()
    template = 'blog/category.html'
    return render(request,template,{'category':catogere,'cat_manu':cat_manu,'pages':pages})

def UniversalSearch(request):
    if request.method == 'POST':
        search = request.POST.get('search', '').strip()  # Get search input and strip whitespace
        model_type = request.POST.get('model_type', 'both')  # Default to 'both' to search across all models

        if not search:  # Check if the search term is empty
            return redirect('blogs')  # Redirect to home or a fallback page

        # Initialize results for both Blog and Question models
        blog_results = []
        question_results = []

        if model_type in ['blog', 'both']:
            # Search in Blog: title and content fields
            blog_query = Q(title__icontains=search) | Q(content__icontains=search)
            blog_results = Blog.objects.filter(blog_query, status='published')

        if model_type in ['question', 'both']:
            # Search in Question: question text, options, and explanation
            question_query = Q(question__icontains=search) | Q(explanation__icontains=search) | \
                             Q(option1__icontains=search) | Q(option2__icontains=search) | \
                             Q(option3__icontains=search) | Q(option4__icontains=search)
            question_results = Question.objects.filter(question_query)

        # Apply pagination for both results
        paginator_size = 6
        blog_paginator = Paginator(blog_results, paginator_size)
        blog_page = request.GET.get('page')
        blog_pages = blog_paginator.get_page(blog_page)

        question_paginator = Paginator(question_results, paginator_size)
        question_page = request.GET.get('page')
        question_pages = question_paginator.get_page(question_page)

        # Fetch categories for the menu
        cat_manu = Category.objects.all()

        # Prepare context to pass to the template
        data = {
            'search': search,
            'cat_manu': cat_manu,
            'blog_pages': blog_pages,
            'question_pages': question_pages,
            'model_type': model_type,
            'blog_results': blog_results,
            'question_results': question_results,
        }

        # Use a single template
        return render(request, 'mcq/content_search.html', data)

    else:
        # For GET requests, return an empty search page
        return render(request, 'mcq/content_search.html', {})

def Contact(request):
    cat_manu = Category.objects.all()
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact_request = form.save(commit=False)
            contact_request.status = 'new'  # Set the status manually
            contact_request.save()
            messages.success(request, 'Your query has been submitted successfully! Thanks for your time.')
            return redirect('contact')  # Redirect to the same contact page to prevent re-post on refresh
        else:
            messages.error(request, 'There is a problem with the form, please resubmit it. Thank you!')
            return render(request, 'contact-us/contact.html', {'form': form, 'cat_manu': cat_manu})
    else:
        form = ContactRequestForm()

    return render(request, 'contact-us/contact.html', {'form': form, 'cat_manu': cat_manu})

def About(request):
    cat_manu = Category.objects.all()
    template = 'about-us/about.html'
    return render(request, template,{"cat_manu":cat_manu})

def DeclarationPage(request):
    cat_manu = Category.objects.all()
    template = 'other-app/declaration.html'
    return render(request,template,{"cat_manu":cat_manu})

def PrivacyPolicy(request):
    cat_manu = Category.objects.all()
    template = 'other-app/privacy-policy.html'
    return render(request,template,{"cat_manu":cat_manu})

def Feedback(request):
    cat_manu = Category.objects.all()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for submitting your valuable feedback with us!')
            return redirect('blogs')  # Redirect to home or success page after form submission
        else:
            # Debugging step to print form errors to console
            print(form.errors)
            messages.error(request, 'There was an error submitting the form. Please try again.')
            return render(request, 'other-app/feedback.html', {'form': form, 'cat_manu': cat_manu})
    else:
        form = FeedbackForm()

    return render(request, 'other-app/feedback.html', {'form': form, 'cat_manu': cat_manu})

def AuthorDetail(request):
    template = 'admin/authordetail.html'
    return render(request, template)

def JobPostsList(request):
    # job = Jobs.objects.all().order_by('job_posted')
    cat_manu = Category.objects.all()
    data = {'cat_manu':cat_manu}
    template = 'jobs/job_list.html'
    return render(request,template,data)

def JobPostInDetail(request,slug):
    # job = get_object_or_404(Jobs,slug=slug)
    # cat_manu = Category.objects.all()
    # template = 'jobs/job_post_detail.html'
    # data = {'job':job,'cat_manu':cat_manu}
    # return render(request,template,data)
    raise Http404("Page Not found!")

