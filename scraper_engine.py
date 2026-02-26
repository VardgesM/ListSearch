import csv
import time
import random
import re
import os
import json
from bs4 import BeautifulSoup
from curl_cffi import requests
from deep_translator import GoogleTranslator

def send_telegram_alert(message: str, token: str, chat_id: str):
    if not token or not chat_id:
        return {"success": False, "error": "Token or Chat ID not provided"}

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, impersonate="chrome")
        if response.status_code != 200:
            return {"success": False, "error": response.text}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def clean_price(price_str: str) -> tuple[int, str]:
    # Extract only the digits for the numerical value
    cleaned_num = re.sub(r'[^\d]', '', price_str)
    price_val = int(cleaned_num) if cleaned_num else 0
    
    # Extract currency symbol ($, ֏, €, etc) or letters
    currency_match = re.search(r'([$֏€₽£]|AMD|USD|RUB)', price_str, re.IGNORECASE)
    currency = currency_match.group(1) if currency_match else ""
    
    return price_val, currency

def init_csv(filename: str):
    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0
    if not file_exists:
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Price", "Link"])

def parse_list_am_generator(keyword: str, max_price: int, max_pages: int, crc: int, tg_token: str, tg_chat_id: str):
    csv_filename = "list_results.csv"
    init_csv(csv_filename)
    
    session = requests.Session(impersonate="chrome")
    session.headers.update({
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.list.am/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    })

    yield json.dumps({"type": "log", "message": f"[Info] Translating keyword '{keyword}' into 3 languages..."})
    keywords_to_search = set([keyword.lower()])
    
    # Translate keyword
    for lang in ['ru', 'en', 'hy']:
        try:
            translated = GoogleTranslator(source='auto', target=lang).translate(keyword)
            if translated:
                keywords_to_search.add(translated.lower())
        except Exception as e:
            yield json.dumps({"type": "error", "message": f"[Translation Error] {e}"})

    keywords_list = list(keywords_to_search)
    yield json.dumps({"type": "log", "message": f"[Start] Searching for keywords: {', '.join(keywords_list)}"})
    yield json.dumps({"type": "log", "message": f"[Settings] Max price: {max_price}, Pages per keyword: {max_pages}, Currency: {crc}"})

    seen_links = set()

    for current_keyword in keywords_list:
        yield json.dumps({"type": "log", "message": f"\n[Info] >>> Searching for keyword: '{current_keyword}' <<<"})
        
        for page in range(1, max_pages + 1):
            yield json.dumps({"type": "log", "message": f"[Info] Parsing page {page} of {max_pages} for '{current_keyword}'..."})
            
            # crc=0 (AMD), crc=1 (USD)
            url = f"https://www.list.am/category?price1=&price2={max_price}&crc={crc}&q={current_keyword}&pg={page}"
            
            try:
                response = session.get(url)
                
                if response.status_code == 403:
                    yield json.dumps({"type": "error", "message": "[Error] Received code 403. Cloudflare likely blocked the request. Try changing IP or increasing delays."})
                    break
                
                if response.status_code != 200:
                    yield json.dumps({"type": "error", "message": f"[Error] Page returned code {response.status_code}. Skipping."})
                    continue
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.select('a.fav-item-info-container')
                
                if not items:
                    yield json.dumps({"type": "log", "message": f"[Info] No products found on page for keyword '{current_keyword}'."})
                    break
                    
                for item in items:
                    try:
                        href = item.get('href')
                        link = f"https://www.list.am{href}" if href else "Link missing"
                        
                        # Deduplication check
                        if link in seen_links:
                            continue
                        
                        title_elem = item.select_one('div.dltitle')
                        title = title_elem.text.strip() if title_elem else "Untitled"
                        
                        price_wrapper = item.select_one('div.ad-info-line-wrapper')
                        price_str = ""
                        
                        if price_wrapper:
                            price_str = price_wrapper.text.strip()

                        price_val, currency = clean_price(price_str)
                        
                        if price_val > max_price:
                            continue
                            
                        # If passed filters, add to seen
                        seen_links.add(link)

                        with open(csv_filename, 'a', encoding='utf-8-sig', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([title, f"{price_val} {currency}".strip(), link])
                            
                        # Telegram
                        if tg_token and tg_chat_id:
                            message = (
                                f"🔥 <b>Match found!</b>\n"
                                f"<b>Title:</b> {title}\n"
                                f"<b>Price:</b> {price_val} {currency}\n"
                                f"<a href='{link}'>Go to listing</a>"
                            )
                            tg_res = send_telegram_alert(message, tg_token, tg_chat_id)
                            if not tg_res.get("success"):
                                yield json.dumps({"type": "error", "message": f"[Telegram Error] {tg_res.get('error')}"})
                        
                        # Yield item found to UI
                        yield json.dumps({
                            "type": "item",
                            "title": title,
                            "price": price_val,
                            "currency": currency,
                            "link": link,
                            "keyword": current_keyword
                        })
                        yield json.dumps({"type": "log", "message": f" [+] Found: {title} | Price: {price_val} {currency}"})
                        
                    except AttributeError as e:
                        yield json.dumps({"type": "error", "message": f"[Error] Product card HTML structure changed: {e}"})
                        continue
                    except Exception as e:
                        yield json.dumps({"type": "error", "message": f"[Error] Unexpected error processing product: {e}"})
                        continue
                        
            except Exception as e:
                yield json.dumps({"type": "error", "message": f"[Error] Network or unexpected error requesting page {page}: {e}"})
                break
                
            if page < max_pages:
                delay = random.uniform(4, 9)
                yield json.dumps({"type": "log", "message": f"[Info] Waiting {delay:.2f} sec before next page..."})
                time.sleep(delay)

    yield json.dumps({"type": "finish", "message": "\n[Info] Scraper finished. Results saved to list_results.csv"})