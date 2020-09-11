import logging

import requests
import htmlmin
from bs4 import BeautifulSoup


class ParserResult:
    def __init__(self, success=False, title="", html="", text="", files=None, file_text="", error=None):
        if files is None:
            files = []
        self.success = success
        self.html = html
        self.title = title
        self.text = text
        self.files = files
        self.file_text = file_text
        self.error = error


def du_content_parser(url):
    try:
        r = requests.get(url)
        logging.info(url + " 데이터를 가져옵니다...")

        bs = BeautifulSoup(r.text, 'html.parser')

        images = bs.find_all("img")
        for i in range(len(images)):
            images[i]["src"] = "https://www.daegu.ac.kr" + images[i]["src"]

        content = bs.find("td", class_="contentArea")

        output_html = htmlmin.minify(str(content))
        output_content = ""
        output_files = []
        title = bs.find("th", class_="view_title").text

        # 첨부파일 구하기
        output_files_text = "<hr>[첨부파일]<ul>"
        no_files = 0
        for tag in bs.find_all("a"):
            if "download" in tag.attrs:
                no_files += 1
                output_files.append([tag.text.strip(), "https://www.daegu.ac.kr" + tag["href"]])
                output_files_text += f"<li><a href=\"https://www.daegu.ac.kr{tag['href']}\">{tag.text.strip()}</a></li>"
        output_files_text += "</ul>"

        # 첨부파일 없으면 태그 다 지움
        if no_files == 0:
            output_files_text = ""

        # 글 내용 공백 잘라내기
        for line in content.text.split("\n"):
            output_content += line.replace("  ", " ").strip() + " "


        return ParserResult(
            success=True,
            title=title,
            html=output_html.replace("font-family: 굴림체;", "").replace("font-family: 굴림;", ""),
            text=output_content,
            files=output_files,
            file_text=output_files_text
        )
    except Exception as e:
        logging.error(e)
        return ParserResult(success=False, error=e)


def du_get_list(page=1):
    try:
        r = requests.get(f"https://www.daegu.ac.kr/article/DG159/list?pageIndex={page}&searchCondition=TA.SUBJECT")
        bs = BeautifulSoup(r.text, 'html.parser')

        article_list = []

        for x in bs.find_all("a"):
            if "onclick" in x.attrs and "goDetail" in x["onclick"]:
                current_article_number = x["onclick"].split("(")[1].split(")")[0]
                current_article_title = x.text.strip().split("\n")[0].strip()

                logging.info(str(page) + " 페이지의 " + current_article_number + " " + current_article_title + " 를 찾았습니다.")
                article_list.append([current_article_number, current_article_title])

        return article_list
    except Exception as e:
        logging.error(e)
        return []
