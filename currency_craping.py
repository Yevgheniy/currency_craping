#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
from Tkinter import *
from tks.dates import DateEntry
from pandastable import Table
import csv

def get_html_from_site(currency, data1, data2):
    # url = 'http://old.kurs.com.ua/arhiv/tablicy/usd/uah/2017-03-27/2017-04-27/mezhbank'
    url = 'http://old.kurs.com.ua/arhiv/tablicy/' + currency + '/uah/' + data1 + '/' + data2 + '/mezhbank'
    r = requests.get(url)
    with open('answer.html', 'w') as output_file:
        output_file.write(r.text.encode('utf8'))

    return r.text

def parse_user_datafile_bs(html_answer):
    results = []
    # text = read_file(filename)

    soup = BeautifulSoup(html_answer, 'html.parser')
    curse_table = soup.find_all('tr')
    # print curse_table
    # curse_list = curse_table.find('td', {'class': 'date').text
    # print curse_list
    # soup_2 = BeautifulSoup(curse_table, 'html.parser')
    # curse_list = soup_2.find_all('tr')


    for curse_string in curse_table:
        curse_data = curse_string.find('td', {'class': 'date'})
        try:
           curse_data = curse_data.text.split(" ",1)[1]
        except AttributeError:
            curse_data = ''
        curse_bid = curse_string.find('td', {'class': 'bid'})
        try:
           curse_bid = curse_bid.text
        except AttributeError:
            curse_bid = ''
        curse_sale = curse_string.find('td', {'class': 'ask'})
        try:
           curse_sale = curse_sale.text
        except AttributeError:
            curse_sale = ''


        # print curse_data + ': ' + unicode("покупка ","utf-8") + curse_bid +  unicode(", продажа ","utf-8") + curse_sale
        if curse_data <> '':
            results.append({
                    '_data': curse_data,
                    'bid': curse_bid,
                    'sale': curse_sale
                })
    return results

# currency = 'eur'
# data1 = '2017-03-27'
# data2 = '2017-04-27'
# html_answer = get_html_from_site(currency, data1, data2)
# # print html_answer
# table_results = parse_user_datafile_bs(html_answer)
# print table_results
# keys = table_results[0].keys()
# with open('exchange_rates.csv', 'w') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(table_results)
# output_file.close()

# user_data_df = pd.DataFrame(table_results)
# user_data_df
class But_print:
    def __init__(self):
        self.but = Button(frame, width=10,height=2)
        self.but["text"] = "Показать"
        self.but.bind("<Button-1>", self.printer)
        self.but.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        # self.but.place(relx=0.5, rely=1.5, anchor=CENTER)

    def printer(self, event):
        # print table_results
        Data_show()
        # pass


root = Tk()
root.title("Курсы валют с сайта old.kurs.com.ua")
# root.geometry('500x700')
content = Frame(root)
frame = Frame(content, borderwidth=2, relief="groove", width=500, height=200)
data_frame = Frame(content, borderwidth=2, relief="groove", width=500, height=900)
content.grid(column=0, row=0)
frame.grid(column=0, row=0, columnspan=3, rowspan=3)
data_frame.grid(column=0, row=3, columnspan=3, rowspan=2)
# cvs_file = open('exchange_rates.csv', 'w')
# open file
def Data_show():
    currency = 'eur'
    data1 = data1_input.get()
    data2 = data2_input.get()
    html_answer = get_html_from_site(currency, data1, data2)
    # print html_answer
    table_results = parse_user_datafile_bs(html_answer)
    # print table_results
    keys = table_results[0].keys()
    with open('exchange_rates.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(table_results)
    with open("exchange_rates.csv") as file:
       reader = csv.reader(file)

       # r and c tell us where to grid the labels
       r = 0
       for col in reader:
          c = 0
          for row in col:
             # i've added some styling
             label = Label(data_frame, width = 10, height = 2, \
                                   text = row, relief = RIDGE)
             label.grid(row = r, column = c)
             c += 1
          r += 1


# pt = Table(data_frame)
# pt.show()
# pt.importCSV(cvs_file)
# pt.show()
# cvs_file.close()


# but_print = But_print()
data1_label = Label(frame, text='Введите начало периода в формате ГГГГ-ММ-ДД')
data1_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
data1_input = Entry(frame)
data1_input.grid(row=0, column=1, sticky=W, padx=5, pady=5)
data2_label = Label(frame, text='Введите конец периода в формате ГГГГ-ММ-ДД')
data2_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
data2_input = Entry(frame)
data2_input.grid(row=1, column=1, sticky=W, padx=5, pady=5)
data2_label = Label(frame, text='Введите конец периода в формате ГГГГ-ММ-ДД')
data2_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
r = ['Евро','Доллар','Рубль']
# optionList = ["Yes","No"]
# dropVar=StringVar()
# dropVar.set("Евро") # default choice
# dropMenu1 = OptionMenu(dropVar, *optionList)
# dropMenu1.grid(column=0,row=3)
# dropVar.trace("w",self.get_selection)
# print self.dropVar.get()
lis = Listbox(frame,selectmode=SINGLE,height=3)
for i in r:
     lis.insert(END,i)
lis.grid(row=2, column=1, padx=5, pady=5)
print_button = But_print()

# root.columnconfigure(0, weight=1)
root.mainloop()
