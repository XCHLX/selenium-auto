import requests
from lxml import etree

base_url = "https://www.bqg5.com"


def main(page_url):

    url = base_url + page_url
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding

    html = resp.text
    print(resp.status_code)  # 状态码
    tree = etree.HTML(html)

    h1 = tree.xpath("string(//h1)").strip()
    print(h1)
    if "、" in h1:
        num, title = h1.split("、", 1)
    else:
        num, title = h1, h1

    next_url = tree.xpath('//div[@class="bottem1"]/a[contains(text(),"下一章")]/@href')

    if next_url:
        next_url = next_url[0]
    else:
        next_url = None

    result = tree.xpath('//div[@id="content"]/text()')
    with open("out.txt", "a", encoding="utf-8") as f:
        f.write(f"第 {num} 章 {title}" + "\n")
        for div in result:
            content = "".join(div).strip()
            if content:  # 筛选出非空的内容
                # print(content)
                f.write(content + "\n")

        f.write(next_url + "\n" + "\n" + "\n" + "\n")
    if next_url:  # 递归调用
        main(next_url)
    else:
        print("下载完成")


if __name__ == "__main__":
    main("/1_1384/378616.html")
