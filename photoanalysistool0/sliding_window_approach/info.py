import re
import os

def main():
	os.chdir('/photoanalysistool0/sliding_window_approach')
	filename = "extracted_info.txt"

	file_ptr = open(filename, "r")

	write_temp_ptr = open("ref_temp.txt","w")

	write_ptr = open("ref.txt","w")

	line_count = 0

	line_list = []

	regex = re.compile('[@_!#$%^&*()<>?/\|}{~:©«¥\`~:;.,]')

	for line in file_ptr:
		try:
			line_count += 1
			line_text = line.split("\n")
			if(((re.match('^[a-zA-Z]+', line) is not None) and (regex.search(line) is None) and (line.isdigit())) or ((line[0].isdigit()) and (line[2] == "\'"))):
				if(line[-2]=="\""):
					line_list = [line_count-1] + [line_count] + line_list
				#write_ptr.write(line_text[0]+'\n')
		except IndexError:
			continue

	file_ptr.close()

	file_ptr = open(filename, "r")
	line_count = 0

	for line in file_ptr:
		line_count += 1
		#line = line.replace("\'","")
		#line = line.replace("\"","")
		if(line_count in line_list):
			write_temp_ptr.write(line)

	line_list = []
	file_ptr.close()
	write_temp_ptr.close()

	write_temp_ptr = open("ref_temp.txt","r")

	for line in write_temp_ptr:
		if(line in line_list):
			continue

		line_list += [line]
		write_ptr.write(line)

	print(line_list)

	write_ptr.close()
	write_temp_ptr.close()
	os.remove("ref_temp.txt")
	#print(line_list, len(line_list))

if __name__ == '__main__':
	main()
