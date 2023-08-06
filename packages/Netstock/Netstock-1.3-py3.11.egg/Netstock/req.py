class HTTP_req_Exception(Exception):
    '''Built in Exception'''
    pass

class Req(object):
    def __init__(self, website: str) -> None:
        self.website = website

    def return_status_code(self):
        try:
            print(__import__("requests").get(self.website).status_code)
        except HTTP_req_Exception as still_a_error:
            print(still_a_error)


    def get_content(self):
        try:
            val = __import__("requests").get(self.website).content
            with open("index.html", 'wb') as wb:
                wb.write(val)
                wb.close()
        except HTTP_req_Exception as still_a_error:
            print(still_a_error)

