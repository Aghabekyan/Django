from django.shortcuts import render
from blog.models import Content, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pprint
import urlparse
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response


news_line = Content.objects.filter().order_by('-pub_date')[:5]


def index(request):
    return render_to_response('base.html', {'news_line': news_line})


def category(request, cat_id):
    data = Content.objects.filter(category=cat_id)
    category = Category.objects.get(pk=cat_id)
    paginator = Paginator(data, 25) # Show 25 news per page
    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data = paginator.page(paginator.num_pages)
    print data
    return render_to_response('cat.html', {'data': data, 'category': category})


def article(request, article_id):
    res = Content.objects.get(pk=article_id)

    def youtubeUrlId(url):
        url_data = urlparse.urlparse(url)
        query = urlparse.parse_qs(url_data.query)
        try:
            video = query["v"][0]
        except:
            video = ''
        return video

    data = {
        'date': res.pub_date,
        'title': res.title,
        'desc': res.desc,
        'img': res.img.url,
        'video': youtubeUrlId(res.video),
        'url': request.get_full_path(),
    }
    return render_to_response('article.html', {'data': data, 'news_line': news_line})
