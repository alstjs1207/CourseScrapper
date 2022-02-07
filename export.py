import csv
from db import db


def export(word):
    file = open("courses.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "description", "link"])
    courses = db.get(word)
    for course in courses:
        writer.writerow([course['title'], course['description'], course['link']])