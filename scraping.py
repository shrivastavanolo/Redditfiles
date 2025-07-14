import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://www.reddit.com"
HEADLESS_WAIT_TIME = 5

def get_username(url):
    return url.strip("/").split("/")[-1]

def init_driver(headless=True):
    """Initialize a Selenium Chrome WebDriver with custom headers."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    #Remove navigator.webdriver flag
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """
    })

    return driver

def get_rendered_html(driver, url):
    driver.get(url)
    time.sleep(HEADLESS_WAIT_TIME)
    return driver.page_source

def extract_post_text(driver, post_url):
    """Render and extract post content using Selenium."""
    full_url = urljoin(BASE_URL, post_url)
    driver.get(full_url)

    try:
        # Wait until any post content is visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='t3_']"))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Dynamically rendered content div
        content_divs = soup.select("div[id^='t3_']")
        for div in content_divs:
            paragraphs = div.find_all("p")
            if paragraphs:
                return "\n".join(p.get_text(strip=True) for p in paragraphs)

        return "[No post content found]"

    except Exception as e:
        return f"[Timeout or error while waiting for post content: {e}]"

def extract_comment_text(driver, comment_url):
    """Render and extract comment content using Selenium"""
    full_url = urljoin(BASE_URL, comment_url)
    html = get_rendered_html(driver, full_url)
    soup = BeautifulSoup(html, "html.parser")

    comment_div = soup.find("div", {"data-testid": "comment"})
    if comment_div:
        return comment_div.get_text(separator="\n").strip()

    return "[No comment found]"

def scrape_links(driver, url, selector, limit=10):
    """Render and extract post/comment links from a user page"""
    html = get_rendered_html(driver, url)
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a in soup.select(selector):
        href = a.get("href")
        if href and href.startswith("/r/") and len(links) < limit:
            links.append(href)

    return links

def get_user_content(profile_url, limit=10):
    username = get_username(profile_url)
    submitted_url = f"{BASE_URL}/user/{username}/submitted/"
    comments_url = f"{BASE_URL}/user/{username}/comments/"

    driver = init_driver()

    try:
        post_links = scrape_links(driver, submitted_url, "a.absolute.inset-0[href]", limit=limit)
        comment_links = scrape_links(driver, comments_url, "a[href*='/r/'][href*='/comments/']", limit=limit)

        content_items = []

        # Posts
        for link in post_links:
            print(f"[POST] Scraping: {link}")
            try:
                text = extract_post_text(driver, link)
                content_items.append({
                    "text": text,
                    "url": urljoin(BASE_URL, link)
                })
            except Exception as e:
                print(f"Failed to scrape post {link}: {e}")

        # Comments
        for link in comment_links:
            print(f"[COMMENT] Scraping: {link}")
            try:
                text = extract_comment_text(driver, link)
                content_items.append({
                    "text": text,
                    "url": urljoin(BASE_URL, link)
                })
            except Exception as e:
                print(f"Failed to scrape comment {link}: {e}")
        return username, content_items

    finally:
        driver.quit()
