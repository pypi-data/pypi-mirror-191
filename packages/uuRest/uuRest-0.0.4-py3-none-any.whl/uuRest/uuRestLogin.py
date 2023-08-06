import uuRest


class uuRestLogin:
    def __init__(self):
        self.oidc_url = ""
        self.request_payload = {}

    def get_request_payload(self):
        raise Exception(f'Not implemented. Please use uuRestLoginGeneral.')


class uuRestLoginGeneral(uuRestLogin):
    def __init__(self, oidc_url: str, awid_owner1: str, awid_owner2: str, scope: str, method: uuRest.uuRestMethod = uuRest.uuRestMethod.POST):
        super().__init__()
        self.oidc_url = oidc_url
        self.awid_owner1 = awid_owner1
        self.awid_owner2 = awid_owner2
        self.scope = scope
        self.method = method

    def get_request_payload(self):
        result = {
            "grant_type": "password",
            "username": f"{self.awid_owner1}",
            "password": f"{self.awid_owner2}",
            "scope": f'openid {self.scope}'
        }
        return result