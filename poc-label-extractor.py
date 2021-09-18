# Required Modules
from bs4 import BeautifulSoup
import zipfile,fnmatch,os
import pandas as pd

def extract_visiofile():
    """
    This function is used to extract the vsdx file to get all the 
    nested xml files.    
    """
    rootPath = r"./"
    pattern = '*.vsdx'
    for root, dirs, files in os.walk(rootPath):
        for filename in fnmatch.filter(files, pattern):
            current_visio_file = filename.split(".")[0]
            zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))
    return current_visio_file

def extract_label_data():
    """
    This function is used to scrape the label values of icons from the 
    page1.xml file
    """
    with open(f"./{extract_visiofile()}/visio/pages/page1.xml","r",encoding="utf8") as diag_file:
        contents = diag_file.read()
    soup = BeautifulSoup(contents,'xml')
    titles = soup.find_all('Text')
    labels = []
    split_list = []
    host_names = []
    ip_addresses = []
    for title in titles:
        cur_label = title.get_text().rstrip("\n")
        labels.append(cur_label)
    while("" in labels):
        labels.remove("")
    for i in range(0,len(labels)):
        split_list.append((labels[i].split("\n")))
    for item in split_list:
        if len(item) > 1:
            host_names.append(item[0])
            ip_addresses.append(item[1])
    return host_names,ip_addresses

def create_csv():
    """
    This function is used to export a csv file of all the 
    label data in a table with asset hostname and ip_address as 
    columsn.   
    """
    host_names,ip_addresses = (extract_label_data())
    df = pd.DataFrame(list(zip(host_names,ip_addresses)),columns=['Host name','IP Address'])
    df.to_csv("Asset_List.csv",index=False)

if __name__ == '__main__':
    extract_visiofile()
    create_csv()