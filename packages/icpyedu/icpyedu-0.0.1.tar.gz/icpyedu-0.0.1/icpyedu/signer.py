import sys
import datetime
import re

from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
from cryptography import x509

from endesive import pdf
from endesive.pdf import cms
from OpenSSL import crypto

class Sign():

    def __init__(self) -> None:
        pass

    def setEmail(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            print("Valid Email")
            return True
        else:
            print("Invalid Email")
            # raise Exception("Email inválido")
            return False    
    
    # Verificador se a senha está em branco
    def setPassword(self, password):
        if len(password) > 0: 
            print("Valid Input")
            return True
        else:
            print("Invalid Input")
            return False

    def certificadoContainsExtension(self, certificatePath):
        if('.p12' in certificatePath):
            return certificatePath
        else:
            return certificatePath + '.p12'

    def pdfContainsExtension(self, filePath):
        if('.pdf' in filePath):
            return filePath
        else:
            return filePath + '.pdf'
            
    def signFile(self, email, password, filePath, certificatePath):
        isValidEmail = self.setEmail(email)
        isValidPassword = self.setPassword(password)
        if (not isValidEmail) or (not isValidPassword):
            print("ALGO ERRADO NA SENHA")
            raise Exception("Email inválido")

        certificatePath = self.certificadoContainsExtension(certificatePath)
        filePath = self.pdfContainsExtension(filePath)

        date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
        date = date.strftime('%Y%m%d%H%M%S+00\'00\'')
        
  
        aux_p12 = crypto.load_pkcs12(open(certificatePath, "rb").read(), password.encode("ascii"))
        pem_data = crypto.dump_certificate(crypto.FILETYPE_PEM, aux_p12.get_certificate())
        cert = x509.load_pem_x509_certificate(pem_data, default_backend())

        common_name = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value
        country_name = cert.subject.get_attributes_for_oid(x509.OID_COUNTRY_NAME)[0].value
        organization_name = cert.subject.get_attributes_for_oid(x509.OID_ORGANIZATION_NAME)[0].value
        
        
        class User:
            full_name = common_name
            user_email = email
            company = organization_name
        user = User()

        dct = {
            "aligned": 0,
            "sigflags": 3,
            "sigflagsft": 132,
            "sigpage": 0,
            "sigbutton": True,
            "sigfield": "Signature1",
            "auto_sigfield": True,
            "signform": False,
            "sigandcertify": True,
            "signaturebox": (40, 110, 260, 190),
            "signature_manual": [
                ['text_box', f'Assinado de forma digital por: \n{user.full_name}\nEmail: {user.user_email}\nData: {date}\nAutoridade Certificadora: {user.company}',
                    'default', 5, 10, 270, 40, 7, True, 'left', 'top'],
                ['fill_colour', 0.4, 0.4, 0.4],
                ['rect_fill', 0, 50, 250, 1],
                ['fill_colour', 0, 0, 0],
                ['text_box', user.full_name,
                    'DancingScript', 7, 25, 270, 50, 12, True, 'left', 'top', 1.2],
                ],
            # "signature_img": "image.jpg",
            'contact': email,
            'location': country_name,
            'signingdate': date,
            'reason': user.full_name,
            "password": password,
        }

        with open(certificatePath, 'rb') as fp:
            p12 = pkcs12.load_key_and_certificates(
                fp.read(), 
                password.encode("ascii"), 
                backends.default_backend()
            )

        datau = open(filePath, "rb").read()
        datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
        with open('arquivo-assinado.pdf', "wb") as fp:
            fp.write(datau)
            fp.write(datas)

        return fp


class Verifier():
    def __init__(self) -> None:
        pass

    def pdfContainsExtension(self, filePath):
        if('.pdf' in filePath):
            return filePath
        else:
            return filePath + '.pdf'

    def verifySignature(self, filePath, ac1, ac2):
        filePath = self.pdfContainsExtension(filePath)
        # trusted_cert_pems = (
        #     open("./ac/ac-pessoa.cer", "rb").read(), 
        #     open("./ac/ac-raiz-v3.cer", "rb").read(),
        # )
        trusted_cert_pems = (
            open(ac1, "rb").read(), 
            open(ac2, "rb").read(),
        )
        pdf_file_path = filePath
        data = open(pdf_file_path, "rb").read()

        for (signatureok, hashok, certok) in pdf.verify(
                data, trusted_cert_pems
            ):
                print("*" * 20)
                print("signature ok?", signatureok)
                print("hash ok?", hashok)
                print("cert ok?", certok)
                return True
        return False