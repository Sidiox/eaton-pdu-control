
import hashlib
import subprocess
import pathlib

"""
Conversion from the javascript implementations in the Eaton Shark.js
"""


def convert_to_8859_1(data):
    iso8859_1CharacterArray = {
        " ":"\x20", "!":"\x21", "\"":"\x22", "#":"\x23", "$":"\x24", "%":"\x25","&":"\x26",
        "'":"\x27", "(":"\x28", ")":"\x29", "*":"\x2A", "+":"\x2B", ",":"\x2C", "-":"\x2D",
        ".":"\x2E", "/":"\x2F", "0":"\x30", "1":"\x31", "2":"\x32", "3":"\x33", "4":"\x34",
        "5":"\x35", "6":"\x36", "7":"\x37", "8":"\x38", "9":"\x39", ":":"\x3A", ";":"\x3B",
        "<":"\x3C", "=":"\x3D", ">":"\x3E", "?":"\x3F", "@":"\x40", "A":"\x41", "B":"\x42",
        "C":"\x43", "D":"\x44", "E":"\x45", "F":"\x46", "G":"\x47", "H":"\x48", "I":"\x49",
        "J":"\x4A", "K":"\x4B", "L":"\x4C", "M":"\x4D", "N":"\x4E", "O":"\x4F", "P":"\x50",
        "Q":"\x51", "R":"\x52", "S":"\x53", "T":"\x54", "U":"\x55", "V":"\x56", "W":"\x57",
        "X":"\x58", "Y":"\x59", "Z":"\x5A", "[":"\x5B", "\\":"\x5C", "]":"\x5D", "^":"\x5E",
        "_":"\x5F", "`":"\x60", "a":"\x61", "b":"\x62", "c":"\x63", "d":"\x64", "e":"\x65",
        "f":"\x66", "g":"\x67", "h":"\x68", "i":"\x69", "j":"\x6A", "k":"\x6B", "l":"\x6C",
        "m":"\x6D", "n":"\x6E", "o":"\x6F","p":"\x70", "q":"\x71", "r":"\x72", "s":"\x73",
        "t":"\x74", "u":"\x75", "v":"\x76", "w":"\x77", "x":"\x78", "y":"\x79", "z":"\x7A",
        "{":"\x7B", "|":"\x7C", "}":"\x7D", "~":"\x7E","&nbsp;":"\xA0", "¡":"\xA1", "¢":"\xA2", 
        "£":"\xA3", "¤":"\xA4", "¥":"\xA5", "¦":"\xA6", "§":"\xA7", "¨":"\xA8", "©":"\xA9", 
        "ª":"\xAA", "«":"\xAB", "¬":"\xAC", "­":"\xAD", "®":"\xAE", "¯":"\xAF", "°":"\xB0", 
        "±":"\xB1", "²":"\xB2", "³":"\xB3", "´":"\xB4", "µ":"\xB5", "¶":"\xB6", "·":"\xB7", 
        "¸":"\xB8", "¹":"\xB9", "º":"\xBA", "»":"\xBB", "¼":"\xBC", "½":"\xBD", "¾":"\xBE", 
        "¿":"\xBF","À":"\xC0", "Á":"\xC1", "Â":"\xC2", "Ã":"\xC3", "Ä":"\xC4", "Å":"\xC5", 
        "Æ":"\xC6", "Ç":"\xC7", "È":"\xC8", "É":"\xC9", "Ê":"\xCA", "Ë":"\xCB", "Ì":"\xCC", 
        "Í":"\xCD", "Î":"\xCE", "Ï":"\xCF", "Ð":"\xD0", "Ñ":"\xD1", "Ò":"\xD2", "Ó":"\xD3", 
        "Ô":"\xD4", "Õ":"\xD5", "Ö":"\xD6", "×":"\xD7", "Ø":"\xD8", "Ù":"\xD9", "Ú":"\xDA", 
        "Û":"\xDB", "Ü":"\xDC", "Ý":"\xDD", "Þ":"\xDE", "ß":"\xDF","à":"\xE0", "á":"\xE1", 
        "â":"\xE2", "ã":"\xE3", "ä":"\xE4", "å":"\xE5", "æ":"\xE6", "ç":"\xE7", "è":"\xE8", 
        "é":"\xE9", "ê":"\xEA", "ë":"\xEB", "ì":"\xEC", "í":"\xED", "î":"\xEE", "ï":"\xEF", 
        "ð":"\xF0", "ñ":"\xF1", "ò":"\xF2", "ó":"\xF3", "ô":"\xF4", "õ":"\xF5", "ö":"\xF6",
        "÷":"\xF7", "ø":"\xF8", "ù":"\xF9", "ú":"\xFA", "û":"\xFB", "ü":"\xFC", "ý":"\xFD", 
        "þ":"\xFE", "ÿ":"\xFF"}

    hasNoIsoCharacter = False
    isoMessage = ""
    i=0
    while(not hasNoIsoCharacter and i < len(data)):
        if(data[i] in iso8859_1CharacterArray):
            isoMessage += iso8859_1CharacterArray[data[i]]
        else:
            hasNoIsoCharacter = True
        
        i += 1
    
    if hasNoIsoCharacter:
        return False
    return isoMessage


ref_session_key = "550b60655263ad7fd685f2a7af545d0"
ref_szResponseValue="4bd6239eab0cdff26e689d58c336aa50"
ref_szResponse="6df2ca5b5c8209bf74ce5d68dc1608b8"

def md5(data, raw=False):
    m = hashlib.md5()
    m.update(data.encode())

    if raw:
        return m.digest()
    else:
        return m.hexdigest()

def md5_shark(data, raw=False):
    pass

    shark_gen_path = pathlib.Path(__file__).parent / "shark_gen.js"
    res = subprocess.run(
        [
            "node",
            str(shark_gen_path),
            data,
            str(False)
        ],
        capture_output=True
    )
    # print("===========")
    # print(res)
    # print("====")
    # print(res.stdout.decode())
    # print("===========")
    return res.stdout.decode().strip()

def gen_challenge_response(user, passwd, session_id, data):
    sz_response = ""
    sz_response_value =""

    sz_realm = data[0]
    sz_nonce = data[1]
    sz_c_nonce = data[2]
    sz_uri = data[3]
    sz_qop = data[4]
    ui_nc_val = data[5]


    iso_user = convert_to_8859_1(user)
    login_challenge = iso_user
    iso_passwd = convert_to_8859_1(passwd)
    passwd_challenge = iso_passwd
    iso_sz_realm = convert_to_8859_1(sz_realm)

    sz_realm_challenge = iso_sz_realm

    while (len(ui_nc_val) < 8):
        ui_nc_val = "0" + ui_nc_val
    
    # Needs binary
    # print(f"login_challenge: {login_challenge}")
    # print(f"sz_realm_challenge: {sz_realm_challenge}")
    # print(f"passwd_challenge: {passwd_challenge}")

    a1 = md5(login_challenge + ":" + sz_realm_challenge + ":" + passwd_challenge, True)
    a1_str = a1.decode(encoding="iso8859_1")
    # print(f"a1 start: {a1_str}")
    a1 = a1.decode(encoding="iso8859_1") + ":" + sz_nonce + ":" + sz_c_nonce

    # a1 = "×ö]æxS°]ìR³-Æ¬:FStWrVq1a9evXr179uzYsGHDhgwYMGHChQoUKFCgQYM=:FStWrVq1a9evXr179uzYsGHDhgwYMGHChQoUKFCgQYM="
    session_key = md5_shark(a1, True)
    # print('=========')
    # print("Session key")
    # print("e79f4720ca2a694a8c336aa9ae7eeab1")
    # print(session_key)
    # print("========")

    a2client = "AUTHENTICATE:" + sz_uri
    if (sz_qop != "auth"):
        raise Exception("not implemented")

    s2client = md5_shark(a2client)
    # print("s2client")
    # print("37cd183617d59fc1878cf6067e3e15da")
    # print(s2client)
    sz_response = md5_shark(\
        session_key + ":" + sz_nonce + ":" + ui_nc_val + ":" + sz_c_nonce + ":" + sz_qop + ":" + s2client
        )

    sz_response = compute_sz_response(
            s2client=s2client,
            session_key=session_key,
            sz_nonce=sz_nonce,
            ui_nc_val=ui_nc_val,
            sz_c_nonce=sz_c_nonce,
            sz_qop=sz_qop
        )


    # s2
    a2server = ":" + sz_uri
    s2server = md5_shark(a2server)

    sz_response_value = compute_sz_response_value(
            s2server=s2server,
            session_key=session_key,
            sz_nonce=sz_nonce,
            ui_nc_val=ui_nc_val,
            sz_c_nonce=sz_c_nonce,
            sz_qop=sz_qop
        )

    return session_key, sz_response, sz_response_value

def compute_sz_response(
        session_key,
        sz_nonce,
        ui_nc_val,
        sz_c_nonce,
        sz_qop,
        s2client
    ):
    sz_response = md5_shark(
            session_key + ":" + sz_nonce + ":" + ui_nc_val + ":" + sz_c_nonce + ":" + sz_qop + ":" + s2client
        )

    return sz_response

def compute_sz_response_value(
        s2server,
        session_key,
        sz_nonce,
        ui_nc_val,
        sz_c_nonce,
        sz_qop,
    ):

    sz_response_value = md5_shark(
        session_key + ":" + sz_nonce + ":" + ui_nc_val\
        + ":" + sz_c_nonce + ":" + sz_qop + ":" + s2server
    )
    return sz_response_value



