import win32crypt
import binascii


def encrypt_psswd(username, password, filename):
    # encrypt the password with DPAPI.
    crypted_password = win32crypt.CryptProtectData(
        password.encode(), None, None, None, None, 0
    )
    # Do some magic to return the password in the exact same format as if you would use Powershell.
    password_secure_string = binascii.hexlify(crypted_password).decode()

    # Use the same xml format as for powershells Export-Clixml, just replace values for username and password.
    xml = f"""<Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">
    <Obj RefId="0">
        <TN RefId="0">
        <T>System.Management.Automation.PSCredential</T>
        <T>System.Object</T>
        </TN>
        <ToString>System.Management.Automation.PSCredential</ToString>
        <Props>
        <S N="UserName">{username}</S>
        <SS N="Password">{password_secure_string}</SS>
        </Props>
    </Obj>
    </Objs>"""

    with open(filename, 'w') as f:
        f.write(xml)


def decrypt_psswd(filename):

    with open(filename, "r", encoding="utf-8") as f:
        xml = f.read()

        # Extract username and password from the XML since that's all we care about.
        username = xml.split('<S N="UserName">')[1].split("</S>")[0]
        password_secure_string = xml.split('<SS N="Password">')[1].split("</SS>")[0]

        # CryptUnprotectDate returns two values, description and the password,
        # we don't care about the description, so we use _ as variable name.
        _, decrypted_password_string = win32crypt.CryptUnprotectData(
            binascii.unhexlify(password_secure_string), None, None, None, 0
        )
        return username, decrypted_password_string.decode(encoding='utf-8')
