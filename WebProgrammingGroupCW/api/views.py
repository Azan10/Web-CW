from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import NewsArticle, Category, UserPreferences, Comment
from django.forms.models import model_to_dict



def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html')

@login_required
def profile(request):
    user_preferences, created = UserPreferences.objects.get_or_create(user=request.user)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
        user_preferences.favorite_categories.set(selected_categories)
        return JsonResponse({'success': True})
    
    return JsonResponse({'categories': list(categories.values()), 'user_preferences': user_preferences.favorite_categories.values()})




def news_list(request):
    try:
        user_preferences = UserPreferences.objects.get(user=request.user)
        favorite_categories = user_preferences.favorite_categories.values_list('id', flat=True)

        if not favorite_categories:
            # Handle the case where the user has not selected any favorite categories
            return JsonResponse({'articles': []})  # Return an empty list if no favorite categories

        articles = NewsArticle.objects.filter(category__in=favorite_categories)

    except UserPreferences.DoesNotExist:
        # Handle the case where UserPreferences does not exist for the user
        # You can create a default UserPreferences instance for the user or take other actions
        articles = NewsArticle.objects.all()  # Return all articles if UserPreferences does not exist

    return JsonResponse({'articles': list(articles.values())})


@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')

        if title and content and category_id:
            category = Category.objects.get(pk=category_id)

            new_article = NewsArticle.objects.create(
                title=title,
                content=content,
                category=category
            )
            return JsonResponse({'success': True, 'article_id': new_article.id})
        else:
            return JsonResponse({'success': False, 'errors': 'Invalid data'})
    else:
        categories = Category.objects.all()
        return render(request, 'add_article.html', {'categories': categories})

@login_required
def article_detail(request, article_id):
    print(f"Received article_id: {article_id}")
    try:
        article = NewsArticle.objects.get(pk=article_id)
        print(f"Found article: {article}")
    except NewsArticle.DoesNotExist:
        print(f"No article found with ID: {article_id}")
    article = get_object_or_404(NewsArticle, pk=article_id)
    
    comments = Comment.objects.filter(article=article, parent_comment=None).values()

    return JsonResponse({'article': model_to_dict(article), 'comments': list(comments)})

@require_POST
@login_required
def add_comment_to_article(request, article_id):
    article = get_object_or_404(NewsArticle, pk=article_id)
    content = request.POST.get('content')

    if content:
        new_comment = Comment.objects.create(
            content=content,
            user=request.user,
            article=article
        )

        return JsonResponse({'success': True, 'comment': model_to_dict(new_comment)})

    return JsonResponse({'success': False, 'errors': 'Invalid data'})

@require_POST
@login_required
def add_reply_to_comment(request, article_id, parent_comment_id):
    article = get_object_or_404(NewsArticle, pk=article_id)
    parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
    content = request.POST.get('content')

    if content:
        new_comment = Comment.objects.create(
            content=content,
            user=request.user,
            article=article,
            parent_comment=parent_comment
        )

        return JsonResponse({'success': True, 'comment': model_to_dict(new_comment)})

    return JsonResponse({'success': False, 'errors': 'Invalid data'})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST' and request.user == comment.user:
        content = request.POST.get('content')

        if content:
            comment.content = content
            comment.save()

            return JsonResponse({'success': True, 'comment': model_to_dict(comment)})

    return JsonResponse({'success': False, 'errors': 'Invalid data'})
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST' and request.user == comment.user:
        comment.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
