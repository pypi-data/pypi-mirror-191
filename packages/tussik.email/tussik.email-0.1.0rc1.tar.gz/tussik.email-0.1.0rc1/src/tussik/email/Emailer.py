import logging
import re
import smtplib
import ssl
from email.headerregistry import Address
from email.message import EmailMessage as SmtpMsg
from typing import Optional, Union, List

logger = logging.getLogger("tussik.email")

#
# incase there is an issue with the external library just go on without it
# this library only assists in catching domain issues earlier. It is not essential
#
try:
    from tld import is_tld
except:

    def is_tld(s):
        return True


    logger.error("tussik.email: unable to import optional tld library")


class Emailer:
    __slots__ = ['__to', '__cc', '__bcc', '__replyto', '__sender', '__errormsg',
                 '__subject', '__html', '__text', '__attach', '__headers', '__headers_raw',
                 '__host', '__port', '__username', '__password']
    __g_host: Optional[str] = None
    __g_port: int = 587
    __g_username: Optional[str] = None
    __g_password: Optional[str] = None

    def __init__(self, host: Optional[str] = None,
                 port: Optional[int] = None,
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        self.__host: Optional[str] = host
        self.__port: Optional[int] = port
        self.__username: Optional[str] = username
        self.__password: Optional[str] = password
        self.__to = list()
        self.__cc = list()
        self.__bcc = list()
        self.__replyto = None
        self.__sender = None
        self.__subject = ""
        self.__html = None
        self.__text = None
        self.__attach = list()
        self.__headers: dict = {}
        self.__headers_raw: dict = {}
        self.__errormsg: Optional[str] = None

    @classmethod
    def setDefault(cls, host: str, port: int = 587,
                   username: Optional[str] = None,
                   password: Optional[str] = None):
        cls.__g_host: str = host
        cls.__g_port: int = port
        cls.__g_username: Optional[str] = username
        cls.__g_password: Optional[str] = password

    def _explode(self, s: str, multiple: bool = True, as_array: bool = False) -> Union[str, List[str]]:
        parts = re.split(';|,| ', str(s))
        parts = [str(item).strip().lower() for item in parts]
        parts = [item for item in parts if item.count("@") == 1 and "." in item]

        emails = []
        for item in parts:
            tld = item.split(".")[-1]
            if not is_tld(tld):
                continue
            n = item.index("@")
            if n > 0 and n < len(item):
                emails.append(item)
                if not multiple:
                    break
        emails = list(set(emails))

        if as_array:
            return emails
        if len(emails) == 0:
            return ""
        return ", ".join(emails)

    def parse_addresses(self, s: str) -> List[str]:
        return self._explode(s, True, True)

    def __address(self, address: str, name: Optional[str] = None):
        addr = address.split('@')
        if name is None:
            return Address(addr[0], addr[0], addr[1])
        else:
            return Address(name, addr[0], addr[1])

    def clear_to(self):
        self.__to = list()

    def clear_cc(self):
        self.__cc = list()

    def clear_bcc(self):
        self.__bcc = list()

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def errormsg(self) -> Optional[str]:
        return self.__errormsg

    @subject.setter
    def subject(self, line: str):
        self.__subject = line

    def sender(self, address: str, name: Optional[str] = None):
        addresses = self._explode(address, multiple=True, as_array=True)
        if len(addresses) > 0:
            self.__sender = self.__address(addresses[0], name)
        else:
            self.__sender = None

    def replyto(self, address: Optional[str] = None):
        addresses = self._explode(address or "", multiple=True, as_array=True)
        if len(addresses) > 0:
            self.__replyto = addresses[0]
        else:
            self.__replyto = None

    def to(self, address: str, name: Optional[str] = None):
        for email in self._explode(address, multiple=True, as_array=True):
            self.__to.append(self.__address(email, name))

    def cc(self, address: str, name: Optional[str] = None):
        for email in self._explode(address, multiple=True, as_array=True):
            self.__cc.append(self.__address(email, name))

    def bcc(self, address: str, name: Optional[str] = None):
        for email in self._explode(address, multiple=True, as_array=True):
            self.__bcc.append(self.__address(email, name))

    def references(self, val: str):
        if "References" in self.__headers_raw:
            self.__headers_raw["References"] += f" <{val}>"
        else:
            self.__headers_raw["References"] = f"<{val}>"

    def header(self, key: str, val: str, raw: bool = False):
        if raw:
            self.__headers_raw[key] = val
        else:
            self.__headers[key.upper()] = val

    @property
    def html(self) -> str:
        return self.__html

    @html.setter
    def html(self, html: str):
        self.__html = html

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text

    def clear_attachments(self):
        self.__attach = list()

    def attachment(self, filename: str, alias: Optional[str] = None, contenttype: Optional[str] = None, content=None):
        self.__attach.append({
            'alias': alias if isinstance(alias, str) else None,
            'filename': str(filename),
            'content': content,
            'type': contenttype if isinstance(contenttype, str) else 'application/octet-stream'
        })

    def send(self,
             host: Optional[str] = None,
             port: Optional[int] = None,
             username: Optional[str] = None,
             password: Optional[str] = None) -> bool:

        self.__errormsg = None
        msg = SmtpMsg()
        recipients = list()

        for key, val in self.__headers_raw.items():
            msg[key] = val

        for key, val in self.__headers.items():
            msg[f"X-{key}"] = val

        if self.__replyto:
            msg['Reply-To'] = self.__replyto

        if self.__sender:
            msg['From'] = self.__sender

        if self.__subject:
            msg['Subject'] = self.__subject

        if len(self.__to) > 0:
            msg['To'] = tuple(self.__to)
            recipients += self.__to

        if len(self.__cc) > 0:
            msg['Cc'] = tuple(self.__cc)
            recipients += self.__cc

        if len(self.__bcc) > 0:
            msg['Bcc'] = tuple(self.__bcc)
            recipients += self.__bcc

        if self.__text:
            msg.set_content(self.__text)

        if self.__html:
            msg.add_alternative(self.__html, subtype='html')

        try:
            for attach in self.__attach:
                data = attach['content']
                maintype, subtype = attach['type'].split('/', 1)
                msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=attach['filename'])
        except Exception as e:
            logger.exception("adding attachment")
            self.__errormsg = f"failed adding attachment: {str(e.args)}"

        # current vs instance vs global
        if host is None:
            host = self.__host
        if host is None:
            host = Emailer.__g_host
        if host is None:
            raise Exception("host is required")

        # current vs instance vs global
        if port is None:
            port = self.__port
        if port is None:
            port = Emailer.__g_port

        # current vs instance vs global
        if username is None:
            username = self.__username
        if username is None:
            username = Emailer.__g_username

        # current vs instance vs global
        if password is None:
            password = self.__password
        if password is None:
            password = Emailer.__g_password

        try:
            if port in [587, 2587]:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                with smtplib.SMTP(host, port) as s:
                    s.ehlo()
                    s.starttls(context=context)
                    s.ehlo()
                    if username:
                        s.login(username, password)
                    s.send_message(msg)
            else:
                with smtplib.SMTP(host, port) as s:
                    if username:
                        s.login(username, password)
                    s.send_message(msg)
            return True
        except Exception as e:
            msg = "tussik.email send({}:{})".format(str(host), str(port))
            logger.exception(msg)
            self.__errormsg = f"failed sending email: {str(e.args)}"
            return False
