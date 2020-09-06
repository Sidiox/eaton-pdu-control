import unittest

from eaton.response_gen import (
    compute_sz_response, 
    compute_sz_response_value,
    gen_challenge_response
)

class ResponseTests(unittest.TestCase):

    def test_compute_sz_response(self):
        s2client = "37cd183617d59fc1878cf6067e3e15da"
        session_key = "e79f4720ca2a694a8c336aa9ae7eeab1"
        sz_nonce = "FStWrVq1a9evXr179uzYsGHDhgwYMGHChQoUKFCgQYM="
        sz_c_nonce = "FStWrVq1a9evXr179uzYsGHDhgwYMGHChQoUKFCgQYM="
        ui_nc_val = "00000001"
        sz_qop = "auth"
        sz_response = compute_sz_response(
            s2client=s2client,
            session_key=session_key,
            sz_nonce=sz_nonce,
            ui_nc_val=ui_nc_val,
            sz_c_nonce=sz_c_nonce,
            sz_qop=sz_qop
        )

        ref_sz_response = "b21281c0dedc98d69d223da601a86f16"

        assert(sz_response == ref_sz_response)


    def test_compute_sz_response_value(self):
        s2server = "e67eb7aad8c093103e223a9c9d362a32"
        session_key = "e79f4720ca2a694a8c336aa9ae7eeab1"
        sz_nonce = "FStWrVq1a9evXr179uzYsGHDhgwYMGHChQoUKFCgQYM="
        sz_c_nonce = "FStWrVq1a9evXr179uzYsGHDhgwYMGHChQoUKFCgQYM="
        ui_nc_val = "00000001"
        sz_qop = "auth"
        sz_response_value = compute_sz_response_value(
            s2server=s2server,
            session_key=session_key,
            sz_nonce=sz_nonce,
            ui_nc_val=ui_nc_val,
            sz_c_nonce=sz_c_nonce,
            sz_qop=sz_qop
        )

        ref_sz_response_value = "6ef78a572f12d9391ab41bb4ea3ff18b"

        assert(sz_response_value == ref_sz_response_value)


    def test_gen_challenge_response(self):
        
        data = ['epdu.local',"FStWrVq1a9evXr179uzYsGHDhgwYMGHChQoUKFCgQYM=","FStWrVq1a9evXr179uzYsGHDhgwYMGHChQoUKFCgQYM=",'local/epdu17.home.portegi.es','auth','1']
        session_key, sz_response, sz_response_value = \
            gen_challenge_response(
                user="admin",
                passwd="admin",
                session_id="860d1a35ecd8b16242850b17a952a449",
                data=data
            )
        
        ref_session_key = "e79f4720ca2a694a8c336aa9ae7eeab1"

        ref_sz_response = "b21281c0dedc98d69d223da601a86f16"

        ref_sz_response_value = "6ef78a572f12d9391ab41bb4ea3ff18b"

        assert(session_key == ref_session_key)
        assert(sz_response == ref_sz_response)
        assert(sz_response_value == ref_sz_response_value),\
            f"{sz_response_value} should be {ref_sz_response_value}"


if __name__ == "__main__":
    unittest.main()