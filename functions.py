import requests, json
from bs4 import BeautifulSoup
from db import db


def getSoupApi(url):
    headers = {
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'referer' : 'https://fastcampus.co.kr/'
    }
    response = requests.get(url, headers=headers).text
    return response

def getSoup(url):
    headers = {
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    }
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, "html.parser")


def scrapFastcampus(word):

    courses = []

    url = f"https://fastcampus.co.kr/.api/www/search?q={word}"
    results = json.loads(getSoupApi(url), strict=False)['data']

    for result in results:

        title = result['publicTitle']
        if not title:
            title = ""

        description = result['publicDescription']
        if not description:
            description = ""

        img = result['desktopCardAsset']
        if not img:
            img = ""
        
        link = result['slug']
        if not link:
            link = ""

        course = {
            "title": title,
            "description": description,
            "img": img,
            "link": f"https://fastcampus.co.kr/{link}",
        }

        courses.append(course)

    return courses


def scrapInflearn(word):

    courses = []

    url = f"https://www.inflearn.com/courses?s={word}"
    pages = getSoup(url).find("div", {"class": "pagination_container"}).find_all("a")
    lastPage = int(pages[-1].get_text(strip=True))

    for page in range(lastPage):

        url = f"https://www.inflearn.com/courses?s={word}&order=search&page={page}"
        results = getSoup(url).find_all("div", {"class": "course_card_item"})

        for result in results:
            
            courseInfo = result.find("div", {"class": "course_card_back"})

            title = courseInfo.find("p", {"class": "course_title"}).string
            if not title:
                title = ""
            
            description = courseInfo.find("p", {"class": "course_description"}).string
            if not description:
                description = ""
            
            link = courseInfo.find("a")['href']
            if not link:
                link = ""
            
            imgAndVideo = result.find("div", {"class":"card-image"})
            img = ""
            video = ""
            if imgAndVideo.find("img"):
                img = imgAndVideo.find("img")['src']
            else:
                video = imgAndVideo.find("video").find("source")['src']

            course = {
                "title": title,
                "description": description,
                "img": img,
                "video": video,
                "link": f"https://www.inflearn.com{link}",
            }

            courses.append(course)

    return courses


def getCourses(word):
    try:
        fastcampusCourses = scrapFastcampus(word)
        inflearnCourses = scrapInflearn(word)
        courses = fastcampusCourses + inflearnCourses

        db[word] = courses

        return courses
    except:
        return []
