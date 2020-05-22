from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import json
from datetime import datetime


class ComingSoon(View):
    def get(self, request):
        return render(request, 'news/coming_soon.html')


class Main(View):
    def get(self, request):
        return redirect('news/')


class OneNews(View):
    def get(self, request, link):
        context = self.get_one_new(link)
        return render(request, 'news/one_news.html', context=context)

    def get_one_new(self, link):
        file_path = getattr(settings, 'NEWS_JSON_PATH')
        with open(file_path) as json_file:
            file = json.load(json_file)
            for dict_news in file:
                if dict_news['link'] == link:
                    return dict_news
            return None


class AllNews(View):
    def get(self, request):
        q = request.GET.get('q', None)
        filter_news = None
        if q is not None:
            filter_news = self.search(q)
        context = self.get_all_news(filter_news)
        return render(request, 'news/all_news.html', context=context)

    def search(self, q):
        file_path = getattr(settings, 'NEWS_JSON_PATH')
        with open(file_path) as json_file:
            file = json.load(json_file)
            result = []
            for dict_news in file:
                if q in dict_news['title'] or q in dict_news['text']:
                    result.append(dict_news)
        return result

    def get_all_news(self, filter_news):
        if filter_news is None:
            file_path = getattr(settings, 'NEWS_JSON_PATH')
            with open(file_path) as json_file:
                file = json.load(json_file)
        else:
            file = filter_news
        dates = []
        for dict_news in file:
            date = dict_news['created'][:10]
            int_date = int(date.replace('-', ''))
            if date in dates:
                continue
            dates.append(int_date)
        dates.sort(reverse=True)

        new_dict = {}
        for date in dates:
            key = f'{str(date)[:4]}-{str(date)[4:6]}-{str(date)[6:]}'
            value = []
            for dict_news in file:
                if dict_news['created'][:10] == key:
                    value.append((dict_news['link'], dict_news['title']))
            new_dict[key] = dict(value)
        result = {'news': new_dict}
        return result


class CreateNews(View):
    def get(self, request):
        return render(request, 'news/create_news.html')

    def post(self, request):
        file_path = getattr(settings, 'NEWS_JSON_PATH')
        with open(file_path) as json_file:
            file = json.load(json_file)
        links = [dic['link'] for dic in file]
        link = max(links) + 1
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title = request.POST.get('title')
        text = request.POST.get('text')
        dictionary = {'created': date,
                      'text': text,
                      'title': title,
                      'link': link}
        file.append(dictionary)

        with open(file_path, 'w') as json_file:
            json.dump(file, json_file)

        return redirect('/news/')
