import sqlite3
from translate import Translator
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler
import os.path
import random as rnd

connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path0 = cursor_path.fetchall()

count_photo = 5

def get_photo(name_img: str, count=count_photo):
    translator = Translator(from_lang='ru', to_lang='en')
    name_image = translator.translate(name_img)
    index = rnd.randint(2, count_photo)

    name = f"00000{index}.jpg"
    name2 = f"00000{index}.png"
    name3 = f"00000{index}.jpeg"

    file_path = f"00000{index}.jpg"
    file_path2 = f"00000{index}.png"
    file_path3 = f"00000{index}.jpeg"

    print(f'{path0[0][0]}\output')
    google_crawler = BaiduImageCrawler(storage={'root_dir': f'{path0[0][0]}/output'}, downloader_threads=1)
    google_crawler.crawl(keyword=name_image,  max_num=count, min_size=(600,600), max_size=None)
    if count != 1:
      # for i in '2345':
      #     if i != index:
      #         for type in ['jpg', 'png', 'jpeg', 'svg']:
      #             if os.path.exists(f'00000{i}.{type}'):
      #               os.remove(f'00000{i}.{type}')
      #               break

      if os.path.exists(file_path):
          return name
      elif os.path.exists(file_path3):
          return name3
      elif os.path.exists(file_path2):
          return name2
    else:
        if os.path.exists("000001.jpg"):
            return "000001.jpg"
        elif os.path.exists("000001.png"):
            return "000001.png"
        else:
            return "000001.jpeg"

#print(get_photo(f'собаки - наши друзья. Виды собак',1))

#print(get_photo('cat'))

