import base64
import time
import io

from selenium import webdriver
from PIL import Image, ImageOps
from pathlib import Path
from string import ascii_lowercase, digits
from random import randint as ri
from img_augmentation import img_oug
from ItemClass import Item
from generate_html import GenerateInvoice

charlist = ascii_lowercase + digits
driver = webdriver.PhantomJS()


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def get_invoices(out_directory="generatedImages", count=10, start=0):

    Path(out_directory).mkdir(parents=True, exist_ok=True)

    for i in range(count):

        t_start = time.time()
        fname = str(start)
        start += 1

        get_html = str(GenerateInvoice())

        base64_html = base64.b64encode(get_html.encode("UTF-8"))

        driver.get("data:text/html;base64," + base64_html.decode())
        driver.execute_script("document.body.style.zoom='200%'")
        el = driver.find_element_by_tag_name('body')
        data = el.screenshot_as_png

        # keylist must be updtaed for  other XML teplates
        keylist = ['KALEMTABLO', 'EARSIV', 'ETTN', 'v1_bilgitablo', 'v1_tutartablo', 'v1_nottablo', 'v2_gonderen',
                   'v2_gonderenVKN', 'v2_gonderenMERSISNO', 'v2_gonderenTCKN', 'v2_alici', 'v2_aliciVKN',
                   'v2_aliciTCKN', 'v2_faturaNo', 'v2_faturaTarih', 'v2_irsaliyeNo', 'v2_irsaliyeTarih',
                   'v2_toplamTutar', 'v2_toplamKDV', 'v2_iskonto']

        # image label
        # boxfile = open(out_directory + "/" + fname + ".txt", "w")

        imagedata = ImageOps.grayscale(Image.open(io.BytesIO(data)))

        right_left = ri(20, 150)
        top_bottom = ri(15, 90)

        top = top_bottom
        right = right_left + 10
        # bottom = top_bottom + 15
        left = right_left
        bottom = max(5, int(imagedata.width * (ri(140, 150) / 100) - imagedata.height))

        imagedata = add_margin(imagedata, top, right, bottom, left, 255)

        imagedata.save(out_directory + "/" + fname + ".jpg", quality=100)

        ek = 1
        ek_w = 2

        item_list = []
        for item in keylist:
            x1 = y1 = x2 = y2 = 0
            try:
                _function = "return myFunction('" + item + "')"

                """ # Multiple incoming cases (Ex: 2 TotalAmount)
                coors = driver.execute_script(_function)
                for coor in coors:

                    locs = list(map(round, (map(float, coor.split()))))
                    x1, y1, x2, y2 = locs[0], locs[1], locs[0] + locs[2], locs[1] + locs[3]

                    x1 = x1 * 2 + left - ek_w
                    y1 = y1 * 2 + top - ek
                    x2 = x2 * 2 + left + ek_w
                    y2 = y2 * 2 + top + ek

                    _str = item + " " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + "\n"
                    # boxfile.write(_str)

                """

                # Single incoming cases
                locs = list(map(round, (map(float, (driver.execute_script(_function)).split()))))
                x1, y1, x2, y2 = locs[0], locs[1], locs[0] + locs[2], locs[1] + locs[3]

                x1 = x1 * 2 + left - ek_w
                y1 = y1 * 2 + top - ek
                x2 = x2 * 2 + left + ek_w
                y2 = y2 * 2 + top + ek

                _str = item + " " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + "\n"
                #boxfile.write(_str)

                item_list.append(Item(item, x1, y1, x2, y2))

            except Exception as e:
                pass

        #boxfile.close()

        t = time.time() - t_start
        print(str(i + 1)+". invoice is generated  -->  ", f"{t:.3f}", 'sn', end="  ")

        img_oug(imagedata, item_list, fname)

    driver.close()
