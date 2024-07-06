import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os

load_dotenv()
def yahoo_crwaler(company_name):
    company_name = company_name
    # 目標 Yahoo 新聞 URL（可以根據需要調整）
    url = f'https://tw.news.search.yahoo.com/search?p={company_name}'

    # 存儲新聞的列表
    news_list = []

    # 發送 HTTP 請求
    response = requests.get(url)
    response.encoding = 'utf-8'
    # 確認請求是否成功
    if response.status_code == 200:
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # 找到所有新聞標題的標籤（根據 Yahoo 新聞網頁結構）
        articles = soup.find_all('h4', {'class': 's-title'})  # Adjust class name as per your actual HTML structure

        for article in articles:
            title = article.text.strip()  # 提取標題文字並去除多餘的空白
            url = article.a['href']  # 從 <h4> 元素內的 <a> 標籤的 'href' 屬性中提取 URL
            
            
            # 發送 HTTP 請求以獲取新聞內容
            response_text = requests.get(url)
            if response_text.status_code == 200:
                soup_text = BeautifulSoup(response_text.text, 'html.parser')
                # 找到新聞內容中的所有段落文字
                paragraphs = soup_text.find_all('p')
                content = '\n'.join([p.text.strip() for p in paragraphs])  # 將所有段落文字連接為一個字串
                doc="標題{title}/n連結:{url}/n內容:{content}/n"
                # 將新聞數據存入字典
                news_data = {
                    'title': title,
                    'url': url,
                    'content': content
                }
                news_list.append(news_data)
            else:
                print(f"無法獲取該新聞的內容: {url}")
    

    # 將新聞列表存儲為 JSON 檔案
    with open(os.getenv('MEWS_PATH'), 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
        print("新聞數據已成功存儲為 news_data.json 檔案。")



    
