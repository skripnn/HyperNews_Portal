from django.shortcuts import render
from django.views import View
from django.conf import settings
import json


class ComingSoon(View):
    def get(self, request):
        return render(request, 'news/coming_soon.html')


class Main(View):
    def get(self, request):
        return render(request, 'news/main.html')


class OneNews(View):
    template_name = 'news/one_news.html'

    def get(self, request, link):
        context = self.get_one_new(link)
        return render(request, self.template_name, context=context)

    def get_one_new(self, link):
        file_path = getattr(settings, 'NEWS_JSON_PATH')
        with open(file_path) as json_file:
            file = json.load(json_file)
            for dict_news in file:
                if dict_news['link'] == link:
                    return dict_news
            return None


class AllNews(View):
    template_name = 'news/all_news.html'

    def get(self, request):
        context = self.get_all_news()
        return render(request, self.template_name, context=context)

    def get_all_news(self):
        file_path = getattr(settings, 'NEWS_JSON_PATH')
        with open(file_path) as json_file:
            file = json.load(json_file)
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
