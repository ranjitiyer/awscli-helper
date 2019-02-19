import requests
from bs4 import BeautifulSoup
from bs4 import element
import os
import io
from typing import List
import os
from concurrent import futures

ListOfTuples = List[tuple]

parent='./db'
description_extension = '.des'
synopsis_extension = '.syn'
examples_extension = '.exmpl'

commands_file = 'commands'
history = []
HIST_FILE = '.history'

services = []
def get_all_services() -> ListOfTuples:
	if len(services) == 0:
		service_url = f'https://docs.aws.amazon.com/cli/latest/reference/index.html'
		service_home = requests.get(service_url).text
		soup = BeautifulSoup(service_home)

		commands_div=soup.find(id='available-services')
		cmd_list = commands_div.find_all('li')
		for item in cmd_list:
			service = item.find('a').text
			service_url = item.find('a')['href']
			services.append((service, service_url))
	return services	

def get_all_commands(service_name:str) -> ListOfTuples:
	return_value = []
	service_url = f'https://docs.aws.amazon.com/cli/latest/reference/{service_name}/index.html'
	service_home = requests.get(service_url).text
	soup = BeautifulSoup(service_home)

	commands_div=soup.find(id='available-commands')
	cmd_list = commands_div.find_all('li')
	for item in cmd_list:
		anchor = item.find('a')
		return_value.append((anchor.text, anchor['href']))
	return return_value	

def write_description(service, command, description):
	filename = os.path.join(parent, service, command)  + description_extension
	with io.open(filename, 'w') as f:
		f.write(description)

def write_synopsis(service, command, synopsis):
	filename = os.path.join(parent, service, command) + synopsis_extension
	with io.open(filename, 'w') as f:
		f.write(synopsis)

def write_examples(service, command, examples):
	filename = os.path.join(parent, service, command) + examples_extension
	with io.open(filename, 'w') as f:
		f.write(examples)

def write_command_summary(service_name, command, command_url) -> str:
	history_lookup_key = '.'.join([service_name, command])
	print(history_lookup_key)

	if history_lookup_key not in history:
		print(f'Downloading synopsis for {service_name} : {command}')

		# if service_name == "acm" and command == "get-certificate":
		# 	raise RuntimeError("runimr error")

		url = f'https://docs.aws.amazon.com/cli/latest/reference/{service_name}/{command_url}'
		response = requests.get(url).text
		soup = BeautifulSoup(response)

		# get description
		description_div = soup.find(id='description')
		description = description_div.find_all('p')[0].text

		# get synopsis
		synopsis_div=soup.find(id='synopsis')
		if synopsis_div is not None:
			code_div = synopsis_div.find('div', class_='highlight-python')
			synopsis = code_div.text
			write_description(service_name, command, description)
			write_synopsis(service_name, command, synopsis)
		
		# get examples
		examples_strio = io.StringIO()
		examples_div = soup.find(id='examples')
		if examples_div is not None:
			for item in examples_div:
				if not isinstance(item, element.NavigableString):
					examples_strio.write(item.text)
					examples_strio.write("\n")

			examples_str = examples_strio.getvalue()
			examples_strio.close()
			write_examples(service_name, command, examples_str)

		return history_lookup_key
		# update in-mem history
		#history.append(history_lookup_key)
	else:
		print(f'Found {service_name} : {command} in history, hence skipping')

def write_commands(service_name:str, commands:ListOfTuples):
	# build output string
	output = io.StringIO()
	for command_tuple in commands:
		cmd = command_tuple[0]
		output.write(cmd + '\n')
	
	# write
	filename = os.path.join(parent, service_name, commands_file)
	with io.open(filename, 'w') as f:
		f.write(output.getvalue())
		output.close()

def write_service_summaries():
	services = get_all_services()
	# services = services[:25]
	for service_tuple in services:
		service_name = service_tuple[0]

		# all commands for the service
		commands = get_all_commands(service_name)
		write_commands(service_name, commands)

		# process commands on threadpool
		ex = futures.ThreadPoolExecutor(max_workers=10)
		future_results = []
		for command_tuple in commands:
			cmd = command_tuple[0]
			cmd_url = command_tuple[1]
			future_results.append(ex.submit(write_command_summary,
				service_name, cmd, cmd_url))

		# gather results		
		for f in future_results:
			try:
				# completed
				history_lookup_key = f.result()
				if history_lookup_key is not None:
					history.append(f.result())
			except RuntimeError as e:
				# failed
				print(e)

		# finally, shutdown the threadpool
		ex.shutdown()	

def create_folder_structures():
	services = get_all_services()
	for service_tuple in services:
		service_name = service_tuple[0]
		os.makedirs(os.path.join(parent, service_name), exist_ok=True)

if '__main__' == __name__:
	try:
		if os.path.isfile(HIST_FILE):
			with io.open(HIST_FILE, 'r') as hist_file:
				history = hist_file.read().split(' ')
		create_folder_structures()
		write_service_summaries()

		# delete history file
		# os.remove(HIST_FILE)
	#except RuntimeError:
	finally:
		print(*history)
		with io.open(HIST_FILE, 'w') as hist_file:
			hist_file.write(' '.join(history))