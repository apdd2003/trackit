from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, AddPostForm
from django.views.generic import ListView
from django.core.mail import send_mail
from .tasks import send_notification_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from taggit.models import Tag
import re
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib import messages


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'sayeem.shaikh@gmail.com',
                      [cd['to']])
            sent = True
        # ... send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
        # img_tags = []
        # for p in posts:
        #     html = p.body

        #     pattern = re.compile(r'<img\s+[^>]*src="([^"]+)"[^>]*>')
        #     match = pattern.search(html)

        #     if match:
        #         image_src = match.group(1)
        #         print(image_src)
        #         p.thumbnail = image_src
        #         # img_tags.append(image_src)
        #     else:
        #         p.thumbnail = "https://media.istockphoto.com/id/1147544810/vector/no-thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=2-ScbybM7bUYw-nptQXyKKjwRHKQZ9fEIwoWmZG9Zyg="

    except PageNotAnInteger:
     # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
     # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,

                             status=Post.Status.PUBLISHED, slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-publish')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post': post, 'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


def add_post(request):

    if request.method == 'POST':
        # Form was submitted
        author = get_object_or_404(User, id=1)
        form = AddPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
        # Assign the post to the comment
            post.author = author
            post.slug = slugify(post.title)

            tags = form.data['tags'].split(',')

            post.save()
            for tag in tags:

                post.tags.add(tag.strip())
            messages.success(
                request, 'The post has been added successfully. It will be visible once approved by admin')
            send_notification_mail.delay(post.title)
            return redirect('/')

    else:
        form = AddPostForm()
        # ... send email
    return render(request, 'blog/post/add_post.html',
                  {'form': form,
                   })
