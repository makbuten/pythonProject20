from celery import shared_task
import datetime
from .models import PostCategory, Post, Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@shared_task
def message_monday():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in_comment__gte=last_week)  # last_week
    categories = set(posts.values_list('categories__category', flat=True))  # ('categories__post', flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribers__email', flat=True))#'subscribers__username', flat=True))
    subscribers_emails = list(filter(None, subscribers))
    print(categories, subscribers, subscribers_emails)
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': 'http://127.0.0.1:8000',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email='djtest26@mail.ru',
        to=subscribers_emails
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def send_create_message(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    title = post.title
    subscribers = []
    for category in categories:
        subscribers_user = category.subscribers.all()
        for sub_user in subscribers_user:
            subscribers.append(sub_user.email)
    html_content = render_to_string(
        'message.html',
        {
            'link': f'http://127.0.0.1:8000/{pk}',
            'posts': post.preview,
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='djtest26@mail.ru',
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()