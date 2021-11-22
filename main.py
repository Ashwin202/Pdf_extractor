import re
import requests
import pdfplumber
import pandas as pd
from collections import namedtuple

Inv = namedtuple('Inv', 'vend_num vend_name inv_dt due_dt inv_amt net_amt description')
def download_file(url):
    local_filename = url.split('/')[-1]
    
    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)
        
    return local_filename
ap_url = 'https://www.tabs3.com/support/sample/apreports.pdf'
ap = download_file(ap_url)
with pdfplumber.open(ap) as pdf:
    pages = pdf.pages
    print("PAges",pages)

with pdfplumber.open(ap) as pdf:
    page = pdf.pages[16]
    text = page.extract_text()
print(text)
file1 = open("Demo.txt","a")
file1.write(text)

new_vend_re = re.compile(r'^\d{3} [A-Z].*')
for line in text.split('\n'):
    if new_vend_re.match(line):
        print("Line \n",line)
for line in text.split('\n'):
    if new_vend_re.match(line):
        vend_num, *vend_name = line.split()
        vend_name = ' '.join(vend_name)
print(vend_num)
print(vend_name)
inv_line_re = re.compile(r'(\d{6}) (\d{6}) ([\d,]+\.\d{2}) [\sP]*([\d,]+\.\d{2}) [YN ]*\d (.*?) [*\s\d]')
line_items = []
for line in text.split('\n'):
    if new_vend_re.match(line):
        vend_num, *vend_name = line.split()
        vend_name = ' '.join(vend_name)    
    
    line = inv_line_re.search(line)
    if line:
        inv_dt = line.group(1)
        due_dt = line.group(2)
        inv_amt = line.group(3)
        net_amt = line.group(4)
        desc = line.group(5)
        line_items.append(Inv(vend_num, vend_name, inv_dt, due_dt, inv_amt, net_amt, desc))