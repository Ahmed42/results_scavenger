import re
import csv
import threading
from urllib.parse import urlencode
from urllib.request import Request, urlopen

def download_results(first_index, last_index, fname):
    url = 'http://result.sd/resfinal.php' # POST destination URL here
    pattern = r'<td>(.*)</td>.*<td>(.*)</td>.*<td>(.*)</td>.*<td>(.*)</td>' # For extracting the result from the page

    retries = 10

    results = []
    with open("sudanese_certificate_results" + fname + ".csv", 'w', newline='', encoding='utf-8') as csvfile:
        results_writer = csv.writer(csvfile)
        for index in range(first_index, last_index + 1):
            print('[' + fname + '] Retrieving index: ' + str(index))
            print('[' + fname + '] %{:0.2f} completed.'.format((index - first_index) / (last_index - first_index)*100))
            for i in range(retries):
                try:
                    index = bytes(ascii(index),'utf-8')
                    data = b'searchres1=' + index + b'&userAnswer=3&num1=1&operand=0&num2=2&search=%C8%DC%CD%DC%DC%DC%DC%DC%DC%CB'

                    request = Request(url, data)
                    result = urlopen(request).read().decode('windows-1256')
                
                    match = re.search(pattern, result, re.DOTALL)

                    index = match.group(1)
                    name = match.group(2).lstrip().strip("<b>")
                    mark = match.group(3).lstrip().strip("<br>")
                    is_pass = match.group(4)

                    #print(index + "," + name + "," + mark + "," + is_pass)
                    #results.append((index, name, mark, is_pass))
                    results_writer.writerow((index, name, mark, is_pass))
                    csvfile.flush()
                except ConnectionResetError as ex:
                    continue
                except Exception as ex:
                    print(ex)
                    break
                break


first_index = 100
last_index = 490138
threads_num = 10

thread_range = (last_index - first_index)//threads_num

threads = [threading.Thread(target = download_results,
                            args = (first_index + i*thread_range, first_index + (i + 1)*thread_range - 1, "_part_" + str(i+1)))
           for i in range(threads_num)]

for thread in threads:
    thread.start()
