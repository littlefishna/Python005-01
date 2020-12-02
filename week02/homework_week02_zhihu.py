#!/usr/bin/env python3

import requests
from lxml import etree


def getAnswer(myURL, header):
    response = requests.get(myURL, headers=header)
    selector = etree.HTML(response.text)
    match_answer = "//div[@class='RichContent-inner']/span/p/text()"

    answer_chunk = selector.xpath(match_answer)

    return answer_chunk, response.status_code


def wriFile(filename,answerList):
    with open(filename, "w+") as ret:
        for line in answerList:
            ret.write(line)


if __name__ == '__main__':
    targetURL = "https://www.zhihu.com/question/377547324/answer/1516614122"  # class = "ContentItem AnswerItem"

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    answer, repsStatus = getAnswer(targetURL, header)

    if repsStatus != 200:
        # retry or report Failed
        pass

    wriFile("answer.results",answerList=answer)
