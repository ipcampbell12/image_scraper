from selenium import webdriver
from selenium.webdriver.common.by import By

# allows us to make HTTP requests to url
import requests
import io
from PIL import Image
import time

# path to folder with chromedriver
PATH = "/Users/iancampbell/Desktop/image_scraper/chromedriver"

# add path to executable file
wd = webdriver.Chrome(PATH)

#image_url = 'https://i.natgeofe.com/k/e7ba8001-23ac-457f-aedb-abd5f2fdda62/moms5_4x3.png'


def get_images_from_google(wd, delay, max_images):
    # click on thumbnails and grab image source
    # scroll down to bottom of pages
    def scroll_down(wd):
        # exectue javascript
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    # url for page you want to scrape
    search = input("Enger an animal: ")
    url = f"https://www.google.com/search?q={search}s&tbm=isch"

    # get url for web search
    wd.get(url)

    # store all the urls we have found
    image_urls = set()
    skips = 0

    # runs untils we have reach maxed
    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        # get any tags that contain that class name
        thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')

        # loop through thumbnails and click on them
        for img in thumbnails[len(image_urls)+skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            # look for image in popped up window
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                # check to make sure has src attribute with valide source for the image
                if image.get_attribute('src') and "http" in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}!")

    return image_urls


# This part doesn't work
""" def download_image(download_path, url, file_name):
    try:
        # send get request to url
        image_content = requests.get(url).content

        # store image content in memory
        image_file = io.BytesIO(image_content)

        # convert to image
        image = Image.open(image_file)

        # generate path to save the file
        file_path = download_path + file_name

        # save the image to the file as a jpeg
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print('Sucess')
    except Exception as e:
        print("FAILED -", e) """


#download_image("", image_url, "test.jpg")

urls = get_images_from_google(wd, 1, 5)
print(urls)

# loop through all image urls
""" for i, url in enumerate(urls):

    # download to images folder
    download_image("imgs/", url, str(i) + ".jpg") """

# close chrome window
wd.quit()
