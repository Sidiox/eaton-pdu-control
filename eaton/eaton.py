from typing import Type, List, Dict
import requests
import json
import yaml
import hjson
import base64

from .response_gen import gen_challenge_response

class Eaton():
    """
    Supports the `with` syntax, to make sure users are logged out
    """
    def __init__(self,
        host,
        user,
        passwd):

        self._host = host
        self._user = user
        self._user_encoded = base64.b64encode(self._user.encode()).decode()
        self._passwd = passwd


    def __enter__(self):
        self._authenticate()

    def __exit__(self, *args):
        self._logout()

    def _logout(self):

        uri = f"{self._host}/config/gateway?page=cgi_logout&sessionId={self._session_id}"
        res = requests.get(uri)

    def _authenticate(self):
        """
        Authenticate the current session
        """
        res = requests.get(
            f"{self._host}/config/gateway?page=cgi_authentication&login={self._user_encoded}"
        )
        res_content = res.content.decode()
        res_content = hjson.loads(res_content)
        res_data = res_content['data']


        self._session_id = res_data[0]

        session_key, sz_response, sz_response_value = \
        gen_challenge_response(
            self._user,
            self._passwd,
            self._session_id,
            res_data[6]
        )
        uri = f"{self._host}/config/gateway?page=cgi_authenticationChallenge&sessionId={self._session_id}&login={self._user_encoded}&sessionKey={session_key}&szResponse={sz_response}&szResponseValue={sz_response_value}"

        res = requests.get(uri)

        res_content = res.content.decode()
        res_content = hjson.loads(res_content)
        if "error" in res_content:
            if res_content["error"] == 3334:
                raise Exception("Error Max Users")




    def get_pdu_information(self):
        uri = f"{self._host}/config/gateway?page=cgi_pdu_information&sessionId={self._session_id}"

        res = requests.get(uri)

        return hjson.loads(res.content.decode())

    def get_overview(self):
        uri = f"{self._host}/config/gateway?page=cgi_overview&sessionId={self._session_id}&index_pdu=0"
        res = requests.get(uri)

        tmp = res.content.decode()
        # Replacement because sometimes there is an empty list, not correctly formatted
        tmp = tmp.replace("[,,]", "['','','']")
        tmp = hjson.loads(tmp)

        return tmp

    def get_outlets(self):

        overview = self.get_overview()

        outlets = overview["data"][0]
        return outlets

    def get_outlet_by_index(self, index : int):
        """
        Find outlet, non zero indexed
        Return outlet information list
        """

        outlets = self.get_outlets()
        return outlets[index]


    def get_outlet_by_name(self, outletname):
        """
        @return index, branch, branch_index

        Not zero indexed
        for example, B1: 13, 2, 1
        """
        outlets = self.get_outlets()

        cur_branch = 1
        branch_index = 0
        for i, outlet in enumerate(outlets):
            if cur_branch == outlet[2]:
                branch_index += 1
            else:
                cur_branch = outlet[2]
                branch_index = 1
            # print(outlet)
            name = outlet[0]
            # branch 
            if name == outletname:
                return (i+1, cur_branch, branch_index)

        return (-1, -1, -1)


    def control_outlets(self, outlets, action="ON", delay=0):
        """
        @param outlet: outletname, example "B2"
        """
        uri = f"{self._host}/config/set_object_mass.xml?sessionId={self._session_id}"

        if action == "ON":
            delaybefore = "Startup"
        elif action == "OFF":
            delaybefore = "Shutdown"
        else:
            raise Exception(f"Unknown action {action}")


        indices = []
        outlet_strs = []
        for outlet in outlets:
            index, branch, branch_index = self.get_outlet_by_name(outlet)
            if index == -1:
                raise Exception(f"Unknown outlet {outlet}")

            outlet_str = f"<OBJECT name='PDU.OutletSystem.Outlet[{index}].DelayBefore{delaybefore}'>{delay}</OBJECT>"

            outlet_strs.append(outlet_str)
        
        # Join all elements
        outlets_str = "\n".join(outlet_strs)

        data = f"""<SET_OBJECT>
{outlets_str}
</SET_OBJECT>
"""

        res = requests.post(uri,data= data)

        if res.content.decode() != '<?xml version="1.0" encoding="UTF-8"?>\r\n<SET_OBJECT result="OK"/>\r\n':
            raise Exception(f"Outlet control failed:\n{res.content}")



    def set_outlet_off(self, outlet, shutdown_delay=0):
        self.control_outlets([outlet], action="OFF", delay=shutdown_delay)

    def set_outlets_off(self, outlets, shutdown_delay=0):
        self.control_outlets(outlets, action="OFF", delay=shutdown_delay)

    def set_outlet_on(self, outlet, startup_delay=0):
        self.control_outlets([outlet], action="ON", delay=startup_delay)

    def set_outlets_on(self, outlets, startup_delay=0):
        self.control_outlets(outlets, action="ON", delay=startup_delay)


    def get_devices(self):
        #http://pdu.home.portegi.es/config/gateway?page=cgi_pdu_itEquipment&sessionId=c0810307ce9c387123478e1dfbf6ecd9&_dc=1598811827431
        pass
        uri = f"{self._host}/config/gateway?page=cgi_pdu_itEquipment&sessionId={self._session_id}"

        res = requests.get(uri)

        res_content = hjson.loads(res.content.decode())

        data = res_content['data']

        devs = data[1]

        return devs
