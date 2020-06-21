import re

from lxml import html

from Response import send_request

if __name__ == '__main__':
    urls = [
        'https://volgograd.hh.ru/search/vacancy?area=24&st=searchVacancy&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&fromSearch=true',
    ]

    for url in urls:
        response = send_request(url)
        page_tree = html.document_fromstring(response.content)
        blocks = page_tree.xpath("//div[@class='clusters-group clusters-group_expand']")

        total_count = re.sub(r'[^0-9]+', r'', ''.join(page_tree.xpath("//h1/text()")))
        print(total_count)

        for block in blocks:
            try:
                html_string = html.tostring(
                    block, encoding='unicode', method='html', with_tail=False
                )
                block_tree = html.document_fromstring(html_string)

                if 'Зарплата' in block_tree.xpath("//div[@data-qa='serp__cluster-group-title']/text()"):
                    elements = block_tree.xpath("//a[@class='clusters-value']")

                    for element in elements:
                        html_string = html.tostring(
                            element, encoding='unicode', method='html', with_tail=False
                        )
                        element_tree = html.document_fromstring(html_string)

                        label = re.sub(r'[^0-9]+', r'', ''.join(element_tree.xpath("//span[1]/text()")))
                        value = ''.join(element_tree.xpath("//span[2]/text()"))

                        if label:
                            print(label, value)

            except:
                continue
