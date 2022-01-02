import requests

def send_request(file_name):
	url = "http://34.93.201.102:5000/upload/sanskar@api/ayushbits/NGMA/eng/hi"
	# NGMA -> project name
	payload={}
	files=[
	  ('files[]',(file_name,open(file_name,  'rb')))
	]
	headers = {}
	response = requests.request("POST", url, headers=headers, data=payload, files=files)
	print(response.text)


if __name__ == '__main__':
	send_request('/tmp/NGMA.pdf')
	# path of filename