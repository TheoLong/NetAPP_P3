"""
This script will be used to demonstrate your custom API.

You should be using python requests.

At least two POST requests should be demonstrated.
At least two GET requests should be demonstrated.

Print all HTTP Client Request Headers and Bodies
Print HTTP Server Response Headers and Bodies

If you are doing some kind of file uploading/downloading and it can be verified by a file,
the initial request and response should be printed but the subsequent requests and responses do not need to be printed.

Your API can be as basic or as complicated as you want it to be 
as long as none of your APIs replicate functionality already defined in the assignment.

Remember to also create a "custom.pdf" API Documentation. 
Use the Canvas/LED API documentation as a template/example for how you should format your API documentation.
"""
import requests

sever_addr = "http://raspberry2.local:8081"
def print_tests(response,i):
    print("Test"+ str(i))
    print("Status code: ", end='')
    print(response.status_code)
    print("Header: ", end='')
    print(response.headers['content-type'])
    print("contents: ", end='')
    print(response.text)

#print test1 - post
response = requests.post(sever_addr+'/t1_update', files={'text':'hello_test1'}, auth=('theo', 'theo'))
print_tests(response,str(1))

#print test2 -post
response = requests.post(sever_addr+'/t2_update', files={'text':'hello_test2'}, auth=('theo', 'theo'))
print_tests(response,str(2))

#print test3 -get
response = requests.get(sever_addr+'/t1',auth=('theo', 'theo'))
print_tests(response,str(3))

#print test4 -get
response = requests.get(sever_addr+'/t2',auth=('theo', 'theo'))
print_tests(response,str(4))
