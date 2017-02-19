import csv
import urllib.request
import re
import sys

SITES_COUNT = 0
LINKS_ARRAY = []
FILE = sys.argv[1]


def make_url_list_from_csv(input_file):
    with open(input_file, newline='') as links_list_csv:
        csv_list = csv.reader(links_list_csv, delimiter=' ', quotechar='|')
        all_links = []
        for row in csv_list:
            all_links.append(''.join(row))
        return all_links

LINKS_LIST = make_url_list_from_csv(FILE)
LEN_LINKS_LIST = len(LINKS_LIST)


def progress_bar(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    pr_bar = '#' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (pr_bar, percents, '%', status))
    sys.stdout.flush()


if __name__ == '__main__':
    if len(LINKS_LIST) > 1:
        while SITES_COUNT < len(LINKS_LIST):
            HTML_TEXT = urllib.request.urlopen(LINKS_LIST[SITES_COUNT]).read(
            )[:20000].decode('utf-8')
            LINKS = re.findall('Website</th>\n(.*)', HTML_TEXT)
            LINK = re.findall('href="(.*?)"', str(LINKS))
            LINKS_ARRAY += LINK
            progress_bar(SITES_COUNT, LEN_LINKS_LIST, status='Processing...')
            SITES_COUNT += 1
    else:
        sys.stdout.write('Input file is empty!')
    progress_bar(SITES_COUNT, LEN_LINKS_LIST, status='Processing...')


FINAL_DICT = dict(zip(LINKS_LIST, LINKS_ARRAY))

with open("wikipedia_answers.csv", 'w', newline='') as csv_file:
    CSV_WRITER = csv.writer(csv_file)
    FIRST_STRING = ["wikipedia_page, website"]
    CSV_WRITER.writerow(FIRST_STRING)
    for key, value in FINAL_DICT.items():
        CSV_WRITER.writerow([key, value])
