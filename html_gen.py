'''
  - HTML 파일 만들기 
'''

from bs4 import BeautifulSoup
import requests 

url = 'https://wikidocs.net'
book_list = []
docfile = r"publish/rec.html"

def show(books):
  for book in books:
    for b in book.items():
      print(f"{b[0]}: {b[1]}")
    print('\n')

def save(books, filename):
  head = '''
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>위키독의 추천책</title>
  </head>
  <body>
    <h1>위키독의 베스트북</h1>
  '''
  tail = '''
  </body>
  </html>
  '''
  table_open = '    <div>\n      <table>\n'   # <tr><td>책제목</td><td>파이썬....</td><tr>
  table_close = '      </table>\n    </div>\n    <hr>\n'

  f = open(filename, "wt", encoding='utf-8')
  f.write(head)
  body = ''
  for book in books:
    body += table_open
    for b in book.items():
      # print(f"{b[0]}: {b[1]}")
      if b[0] == '북커버':
        pass
        body += f'      <tr><td>{b[0]}</td><td><img src=\'{b[1]}\'></td></tr>\n'
      else:
        body += f'      <tr><td>{b[0]}</td><td>{b[1]}</td></tr>\n'
    body += table_close
  f.write(body)
  f.write(tail)
  f.close()


response = requests.get(url)
if response.status_code == 200:
    htmlsource = response.content 
    soup = BeautifulSoup(htmlsource, 'html.parser')
    ms = soup.find_all(class_='media')
    for m in ms:
      img = m.find(class_='media-left').find('img').attrs['src']
      title = m.find(class_='media-heading').find('a').text
      divs = m.find(class_='book-detail').find_all('div')
      author = divs[0].text.replace('\n','').replace(' ','').replace('-','')
      pubd = divs[1].text.replace('\n','').replace(' ','').replace('-','')
      book = {}
      book['책제목'] = title
      book['작가'] = author
      book['출판날짜'] = pubd
      book['북커버'] = url + img
      book_list.append(book)
    show(book_list) 
    save(book_list, docfile)
else:
    print("web response error :", response.status_code)
  
