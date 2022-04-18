# Definitions of all class to deserialize json response

class Vendors:
    def __init__(self, response):
        self.status = response.status_code
        self.url = response.url
        self.error_code = None
        self.error_status = None
        self.message = None
        self.data = None
        self.vendor_hash = None
        self.exception = None
        if self.status == 200:
            res = response.json()
            self.error_code = res['ErrorCode']
            self.error_status = res['ErrorStatus']
            self.message = res['Message']
            if self.error_code == 1:
                try:
                    self.data = res['Response']
                    self.vendor_hash = res['Response']['vendors']['data']
                except Exception as ex:
                    print("Vendors class: 200 status and error_code 1 but there were no res['Response']")
                    print("Exception: {0}.\nType: {1}".format(ex, ex.__class__.__name__))
                    self.exception = ex.__class__.__name__

                # self.vendor_hash = res['vendorHash']
                # self.refresh_date = res['nextRefreshDate']
                # self.enable = res['enabled']
            else:
                print("No data returned for url: {0} with error code: {1}", self.url, self.error_code)
        else:
            print("Request failed for url: {0} with status: {1}", self.url, self.status)

    def __repr__(self):
        disp_header = "<" + self.__class__.__name__ + " instance>\n\n"
        disp_vendor_hash = ".vendor_hash: " + str(self.vendor_hash) + "\n"
        disp_url = ".url: " + str(self.url) + "\n"
        disp_msg = ".message: " + str(self.message) + "\n"
        disp_status = ".status: " + str(self.status) + "\n"
        disp_error_code = ".error_code: " + str(self.error_code) + "\n"
        disp_error_status = ".error_status: " + str(self.error_status) + "\n"
        disp_exception = ".exception: " + str(self.exception) + "\n"
        return disp_header + disp_vendor_hash + disp_url + disp_msg + disp_status + disp_error_code + disp_error_status + \
               disp_exception


class Player:
    def __init__(self, response):
        self.status = response.status_code
        self.url = response.url
        self.error_code = None
        self.error_status = None
        self.message = None
        self.exception = None
        self.characters_ids = []

        # Data about the user
        self.name = None
        self.name_code = None
        self.membership_types = []
        self.membership_ids = []
        if self.status == 200:
            res = response.json()
            self.error_code = res['ErrorCode']
            self.error_status = res['ErrorStatus']
            self.message = res['Message']
            if self.error_code == 1:
                try:
                    self.name = res['Response'][0]['bungieGlobalDisplayName']
                    self.name_code = res['Response'][0]['bungieGlobalDisplayNameCode']
                    for item in res['Response']:
                        self.membership_ids.insert(0, item['membershipId'])
                    for item in res['Response'][0]['applicableMembershipTypes']:
                        self.membership_types.insert(0, item)
                    self.membership_types = res['Response'][0]['applicableMembershipTypes']
                except Exception as ex:
                    print("Player 200 status and error_code 1 but no data to retrieve for fields")
                    print("Exception: {0}.\nType: {1}".format(ex, ex.__class__.__name__))
                    self.exception = ex.__class__.__name__
            else:
                print("No data returned for url: {0} with error code: {1}", self.url, self.error_code)
                self.exception = "Wrong error code"
        else:
            print("Request failed for url: {0} with status: {1}", self.url, self.status)
            self.exception = "Wrong status code"

    def __repr__(self):
        disp_header = "<" + self.__class__.__name__ + " instance>\n\n"
        disp_name = ".name: " + str(self.name) + "\n"
        disp_name_code = ".name_code: " + str(self.name_code) + "\n"
        disp_membership_types = ".membership_types: "
        if self.membership_types:
            for member in self.membership_types:
                disp_membership_types += str(member) + " "
        disp_membership_types += "\n"
        disp_membership_id = ".membership_id: " + str(self.membership_id) + "\n"

        disp_url = ".url: " + str(self.url) + "\n"
        disp_msg = ".message: " + str(self.message) + "\n"
        disp_status = ".status: " + str(self.status) + "\n"
        disp_error_code = ".error_code: " + str(self.error_code) + "\n"
        disp_error_status = ".error_status: " + str(self.error_status) + "\n"
        disp_exception = ".exception: " + str(self.exception) + "\n"
        return disp_header + disp_name + disp_name_code + disp_membership_types + disp_membership_id + disp_url + \
               disp_msg + disp_status + disp_error_code + disp_error_status + disp_exception
