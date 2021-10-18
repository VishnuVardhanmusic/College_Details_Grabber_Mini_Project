from django.shortcuts import render


# Create your views here.


def get_html_content(request):
    import requests
    clg_name = request.GET.get('clg_name')
    clg_name = clg_name.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=+{clg_name}').text
    return html_content


def home(request):
    result = None
    if 'clg_name' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')
        result = dict()
        # extract region
        result['clg'] = soup.find("div", attrs={"class": "BNeawe deIvCb AP7Wnd"}).text
        # extract temperature now
        result['desc'] = soup.find("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}).text
        # get the day, hour and actual weather
        result['map'] = soup.find('div',class_="skVgpb").a['href']
    return render(request, 'core/home.html', {'result': result})
