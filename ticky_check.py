#!/usr/bin/env python3

import sys
import re
import csv
import operator

error = dict()
per_user = dict()

column_names_error = ['Error', 'Count']
column_names_user = ['Username', 'INFO', 'ERROR']

search_info = r"ticky: INFO ([\w \[#\]']*)([\(])([\w\.]*)" #group(3) is the username
search_error = r"ticky: ERROR ([\w \[#\]']*)([\(])([\w\.]*)" #group(1) is error message, group(3) is the username

def find_error(search_result, error_dict):
  if search_result.group(1)[:-1] in error:
    error_dict[search_result.group(1)[:-1]] += 1
  else:
    error_dict[search_result.group(1)[:-1]] = error_dict.get(search_result.group(1)[:-1],0) + 1

def split_per_user(search_result, per_user_dict):
  if search_result.group(0).find("ERROR") != -1:
    if search_result.group(3) in per_user_dict:
      per_user_dict[search_result.group(3)][1] += 1
    else:
      per_user_dict[search_result.group(3)] = [0,1]
  elif search_result.group(0).find("INFO") != 1:
    if search_result.group(3) in per_user_dict:
      per_user_dict[search_result.group(3)][0] += 1
    else:
      per_user_dict[search_result.group(3)] = [1,0]

def write_to_csv(file_path, column_headers, dict_to_write, are_dict_values_lists):
  with open(r + file_path, "a+") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(column_headers)
    if are_dict_values_lists:
      for row in dict_to_write:
        writer.writerow((row[0], *row[1])) #argument unpacking since the values are lists
    else:
      for row in dict_to_write:
        writer.writerow(row)

def main():
  with open(sys.argv[1], "r") as file:
    for line in file:
      search_result_error = re.search(search_error, line)
      search_result_info = re.search(search_info,line)
      if search_result_error:
        find_error(search_result_error, error)
        split_per_user(search_result_error, per_user)
      elif search_result_info:
        split_per_user(search_result_info, per_user)

  error = sorted(error.items(), key = operator.itemgetter(1), reverse=True)
  per_user = sorted(per_user.items())

  def write_to_csv("../user_statistics.csv", column_names_user, per_user, True)
  def write_to_csv("../error_messages.csv", column_names_error, error, False)

if __name__ == "__main__":
  main()