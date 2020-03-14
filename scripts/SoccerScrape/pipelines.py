# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv, unidecode
from scrapy.exceptions import DropItem

class PlayerPipeline(object):
    def process_item(self, item, spider):
        exception_2006  = ['sr', 'so', 'jr', 'se', 'ju', 'grad']
        exception_2007 = ['sr', 'se', 'jr', 'ju', 'grad']
        exception_2008 = ['sr', 'se', 'grad']
        decode = unidecode.unidecode #decodes to closes ascii character

        attributes = ['firstName', 'lastName', 'homeTown', 'state_or_country', 'highSchool',  'previousSchool', 'Years_Started']

        for atr in attributes:
            item[atr] = decode(item[atr])

        flag = False

        if item['number'] == '--':
            item['number'] = 'NA'
        if '*' in item['number']:
            item['number'] = item['number'][0:item['number'].index('*')]

        if type(item['rosterYear']) == list and item['college'] == 'Boston College':
            item['rosterYear'] = '2006'

        with open('../data/roster_data.csv', 'a', newline='\n') as f: #appending student item data to 'roster_data.csv'
            row = [item['rosterYear'], item['number'], item['firstName'], item['lastName'],  item['classYear'],
                   item['position'],   item['height'], item['weight'],item['homeTown'],  item['state_or_country'],
                   item['highSchool'], item['previousSchool'], item['college'],   item['collegeLeague'],
                   item['profileLink']]

            writer = csv.writer(f, lineterminator = "\n")

            roster_year = int(item['rosterYear'])
            class_year  = item['classYear'].lower()

            if roster_year == 2006:
                for string in exception_2006:
                    if string in class_year:
                        flag = True
                        break
            if roster_year == 2007:
                for string in exception_2007:
                    if string in class_year:
                        flag = True
                        break
            if roster_year == 2008:
                for string in exception_2008:
                    if string in class_year:
                        flag=True
                        break

            if roster_year < 2006: #change value to go back further years
                flag = True

            if flag:
                raise DropItem("Class year exception for 2006, 2007, or 2008 roster")
            else:
                writer.writerow(row)
                return item

class StarterPipeline(object):
    def process_item(self, item, spider):

        decode = unidecode.unidecode #decodes to closes ascii character

        attributes = ['firstName',  'lastName']

        for atr in attributes:
            item[atr] = decode(item[atr])

        if item['isStarter'] == 'NA':
            raise DropItem("NA for isStarter")

        else:
            with open('../data/incoming_starter_data.csv', 'a', newline='\n') as f: #appending student item data to 'starter_data.csv'
                row = [item['rosterYear'], item['number'], item['firstName'], item['lastName'],
                      item['potentialStarts'], item['plays'], item['starts'], item['isStarter'],
                      item['school']]

                writer = csv.writer(f, lineterminator = "\n")
                writer.writerow(row)
                return item

class IncomingPlayerPipeline(object):
    def process_item(self, item, spider):
        exception_2006  = ['sr', 'so', 'jr', 'se', 'ju', 'grad']
        exception_2007 = ['sr', 'se', 'jr', 'ju', 'grad']
        exception_2008 = ['sr', 'se', 'grad']
        decode = unidecode.unidecode #decodes to closes ascii character

        attributes = ['firstName', 'lastName', 'homeTown', 'state_or_country', 'highSchool',  'previousSchool']

        for atr in attributes:
            item[atr] = decode(item[atr])

        flag = False

        if item['number'] == '--':
            item['number'] = 'NA'
        if '*' in item['number']:
            item['number'] = item['number'][0:item['number'].index('*')]

        if type(item['rosterYear']) == list and item['college'] == 'Boston College':
            item['rosterYear'] = '2006'

        with open('../data/incoming_roster_data.csv', 'a', newline='\n') as f: #appending student item data to 'roster_data.csv'
            row = [item['rosterYear'], item['number'], item['firstName'], item['lastName'],  item['classYear'],
                   item['position'],   item['height'], item['weight'],item['homeTown'],  item['state_or_country'],
                   item['highSchool'], item['previousSchool'], item['college'],   item['collegeLeague'],
                   item['profileLink']]

            writer = csv.writer(f, lineterminator = "\n")

            roster_year = int(item['rosterYear'])
            class_year  = item['classYear'].lower()

            if roster_year == 2006:
                for string in exception_2006:
                    if string in class_year:
                        flag = True
                        break
            if roster_year == 2007:
                for string in exception_2007:
                    if string in class_year:
                        flag = True
                        break
            if roster_year == 2008:
                for string in exception_2008:
                    if string in class_year:
                        flag=True
                        break

            if roster_year < 2006: #change value to go back further years
                flag = True

            if flag:
                raise DropItem("Class year exception for 2006, 2007, or 2008 roster")
            else:
                writer.writerow(row)
                return item
