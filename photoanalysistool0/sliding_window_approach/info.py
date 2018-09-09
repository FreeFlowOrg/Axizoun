import re
string = open('extracted_info.txt').read()
new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)
open('extracted_info.txt', 'w').write(new_str)
