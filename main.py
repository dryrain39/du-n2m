import logging
import os
import time

from DU.Config import get_config
import json

from DU.DUParser import du_get_list, du_content_parser
from DU.Mail import send_mail

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)


def work(config, element):
    try:
        url = "https://www.daegu.ac.kr/article/DG159/detail/" + element[0]

        r = du_content_parser(url)
        logging.info(element[1] + " 데이터를 가져왔습니다.")

        mail_subject = r.title
        mail_html_body = r.html + f"<br>원본: <a href=\"{url}\">{url}</a>" + r.file_text

        send_mail(config, mail_subject, mail_html_body, r.text)
        logging.info(element[1] + " 메일을 보냈습니다.")
    except Exception as e:
        logging.error(e)
    pass


def main():
    config = get_config()
    memory = []

    memory_max = config["store_cnt"]
    no_get_page = config["no_get_page"]

    if os.path.exists("./memory.json"):
        memory = json.load(open("memory.json", 'r', encoding="utf-8"))

    for x in range(1, no_get_page + 1):
        current_list = du_get_list(x)

        for e in current_list:
            if e not in memory:
                if not config["first_run"]:
                    work(config, e)
                    logging.info(str(x) + " 완료 3초 대기...")
                    time.sleep(3)
                memory.append(e)

        logging.info(str(x) + " 페이지 완료 10초 대기...")
        time.sleep(10)

    if len(memory) > memory_max:
        memory = memory[len(memory) - memory_max:]
        logging.info("memory.json을 정리했습니다.")

    logging.info("memory.json 덤프 중...")
    json.dump(memory, open("memory.json", "w", encoding="utf-8"), ensure_ascii=False)

    logging.info("끝났습니다.")


if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)

