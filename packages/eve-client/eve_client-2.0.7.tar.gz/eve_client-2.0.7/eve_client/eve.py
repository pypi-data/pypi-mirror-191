import json
import logging
import re
from asyncio import exceptions
from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from urllib.parse import urljoin

import dateutil.parser
import nacl.encoding
import nacl.exceptions
import nacl.public
import nacl.utils
import requests

from typing import Union

from eve_client.helper import notify, verify_email

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
LOG = logging.getLogger("EVE Client")


class EVEClientAnonymous:
    """Class EVEClientAnonymous communicates with the Exodus API anonymously.

    This module allows to retrieve cve information anonymously from
    Exodus Intelligence API.

        Example initiate connection:

        >>> from eve_client import eve
        >>> exodus_api = eve.EVEClientAnonymous()
        >>> exodus_api.get_cve("CVE-2021-44228")

    Returns:
        JSON Object: CVE information available to the anonymous user.
    """

    def __init__(self):
        self.url = (
            "https://eve.exodusintel.com/vpx-api/v1/anonymous/vulnerability/"
        )

    def get_cve(self, identifier: str) -> dict:
        """Retrieve a Common Vulnerabilities and Exposures identifier.

        :param identifier: CVE identifier
        :type identifier: str
        :return: A dictionary containing fields for the anonymous tier.
        :rtype: dict
        """

        if not re.match(r"CVE-\d{4}-\d{4,7}", identifier, re.IGNORECASE):
            return {"error": "Invalid CVE Identifier", "ok": False}

        try:
            response = requests.get(urljoin(self.url, identifier))
            return response.json()
        except (KeyError, requests.exceptions.ConnectionError):
            return notify(404, f"Vulnerability {identifier} not found.")


class EVEClient:
    """Class EVEClient allows communication with the Exodus API.

        Module to connect and interact with the Exodus Intelligence API.

        :param email: Email address registered with Exodus Intelligence.
        :type email: str
        :param password: User password
        :type password: str
        :param key: Exodus Intelligence API key, defaults to None
        :type key: str, optional
        :param url: Exodus Intelligence API domain,\
             defaults to "https://eve.exodusintel.com"
        :type url: _type_, optional
        :param api_version: Version number ie: v1 or v2, defaults to "v1"
        :type api_version: str, optional
        :param proxy_protocol: Proxy protocol type, defaults to "http"
        :type proxy_protocol: str, optional
        :param proxy_url: Proxy Url, defaults to None
        :type proxy_url: str, optional
        :param proxy_port: Proxy Port, defaults to 3128
        :type proxy_port: int, optional

        Example instantiate the class:

        >>> from eve_client import eve
        >>> exodus_api = eve.EVEClient( 'abc@def.com',
                                        'MyPassword',
                                        'APRIVATEKEY')
        """

    def __init__(
        self,
        email,
        password,
        key=None,
        url="https://eve.exodusintel.com",
        api_version="v1",
        proxy_protocol="http",
        proxy_address="",
        proxy_port=3128,
    ) -> None:

        self.url = url
        if not self.url.lower().startswith(
            "http://",
        ) and not self.url.lower().startswith("https://"):
            self.url = "https://" + self.url

        if verify_email(email):
            self.email = email
        self.session = requests.Session()
        self.password = password
        self.private_key = key

        if api_version not in ["v1", "v2"]:
            self.api_version = "v1"
        else:
            self.api_version = api_version

        proxies = {
            proxy_protocol: f"{proxy_protocol}://{proxy_address}:{proxy_port}",
        }

        if proxy_address:
            if proxy_protocol in ["http", "https"]:
                self.session.proxies = proxies
            else:
                raise requests.exceptions.ProxyError(
                    "Check your proxy settings."
                )
        self.token = self.get_access_token()

    def get_access_token(self) -> str:
        """Obtain access token.

        :raises requests.exceptions.ConnectionError: API is Unavailable.
        :return: A token
        :rtype: str
        """
        url = urljoin(self.url, "vpx-api/v1/login")
        response = self.session.post(
            url,
            json={"email": self.email, "password": self.password},
        )
        if response.status_code != 200:
            notify(response.status_code, "Authentication problem.")
            raise requests.exceptions.ConnectionError("Could not authenticate")
        return response.json()["access_token"]

    def get_bronco_public_key(self):
        """Get server public key.

        :return: A string representation of a public key.
        :rtype: str
        """
        key = None
        try:
            key = self.session.get(
                urljoin(self.url, "vpx-api/v1/bronco-public-key"),
            ).json()["data"]["public_key"]
        except (requests.exceptions.ConnectionError, KeyError):
            LOG.warning("Unable to retrieve the Public key.")
        return key

    def decrypt_bronco_in_report(self, report, bronco_public_key):
        """Decrypt the content of a report using a private and public key.

        :param report: The encrypted message.
        :type report: object
        :param bronco_public_key: The public key
        :type bronco_public_key: str
        :raises KeyError: When Bronco Key is wrong.
        :return: A dictionary object representing the report.
        :rtype: dict
        """
        ciphertext = b64decode(report["bronco"])
        nonce = ciphertext[0:24]
        ciphertext = ciphertext[24:]
        try:
            unseal_box = nacl.public.Box(
                nacl.public.PrivateKey(b64decode(self.private_key)),
                nacl.public.PublicKey(b64decode(bronco_public_key)),
            )
            plaintext = unseal_box.decrypt(ciphertext, nonce)
        except Exception as e:
            notify(403, f"{e}. Verify your private key.")
            raise KeyError()
        report["bronco"] = json.loads(plaintext)
        return report

    def handle_reset_option(self, reset: str = "") -> Union[datetime, None]:
        """Reset number of days.

        :param reset: Number of days in the past to reset
        :type reset: int
        :return: A date in ISO8601
        :rtype: datetime
        """
        if reset is None:
            return None

        # First, try to load reset as an integer indicating the number of days
        # in the past to reset to
        try:
            reset = int(reset)
            return datetime.utcnow() - timedelta(days=reset)
        except ValueError:
            pass

        # Try to load reset as a ISO8601 datetime
        try:
            reset = dateutil.parser.isoparse(reset)
        except ValueError as e:
            LOG.warning(
                f"Did not recognize '{reset}' as ISO8601 datetime - {e}"
            )
            return None
        return reset

    def get_vuln(self, identifier: str) -> dict:
        """Get a Vulnerability by identifier or cve.

        ie:
        >>>  x.get_vuln('CVE-2020-9456')

        :param identifier: String representation of vulnerability id.
        :type identifier: str
        :return: Returns vulnerability
        :rtype: dict
        """
        if self.api_version == "v1":
            api_path = f"vpx-api/{self.api_version}/vuln/for/"
        else:
            api_path = f"vpx-api/{self.api_version}/vulnerabilities/"

        try:
            r = self.session.get(
                urljoin(
                    self.url,
                    f"{api_path}/{identifier}",
                )
            )
            return r.json()
        except (KeyError, requests.exceptions.ConnectionError):
            return notify(404, f"Vulnerability {identifier} not found.")

    def get_recent_vulns(
        self, reset: Union[str, int] = "", before: str = "", after: str = ""
    ) -> dict:
        """Get all vulnerabilities within 60 days of the user's stream marker;\
             limit of 500 vulnerabilities can be returned.

        :param reset: Reset the stream maker to a number of days in the
                past, defaults to 0
        :type reset: int, optional
        :return: Returns recent vulnerabilities.
        :rtype: dict
        """
        params = {}

        if self.api_version == "v1":
            api_path = f"vpx-api/{self.api_version}/vulns/recent"
        else:
            api_path = f"vpx-api/{self.api_version}/vulnerabilities"

        # Int or ISO datetime
        if reset != "":
            reset = self.handle_reset_option(reset)

        if self.api_version == "v2":
            params["since"] = reset
            if after != "":
                params["after"] = after
        else:
            params["reset"] = reset

        r = self.session.get(
            urljoin(self.url, f"{api_path}"),
            params=params,
        )

        if r.status_code != 200:
            return notify(
                r.status_code,
                "There was an error retrieving the recent vulnerability list.",
            )
        return r.json()

    def search(self, search_term: str) -> dict:
        """Search specific term

        :param search_term: Term to search for.
        :type search_term: str
        :return: Returns vulnerabilities containing search term
        :rtype: dict
        """
        api_path = "vpx-api/v2/vulnerabilities/search?query="

        try:
            response = self.session.get(
                urljoin(
                    self.url,
                    f"{api_path}{search_term}",
                ),
            )
            return response.json()
        except (KeyError, requests.exceptions.ConnectionError):
            return notify(
                404,
                f"Vulnerability containing the term {search_term} \
                     were not found.",
            )

    def get_recent_reports(
        self, reset: Union[int, datetime, None] = None
    ) -> dict:
        """Get recent reports.

        :param reset: A number of days in the past to reset, defaults to 0
        :type reset: int, datetime, optional
        :return: Recent reports.
        :rtype: dict
        """
        params = {}
        if reset:
            reset = self.handle_reset_option(reset)

        if reset:
            reset = reset.isoformat()
            params = {"reset": reset}
        r = self.session.get(
            urljoin(self.url, "vpx-api/v1/reports/recent"),
            params=params,
        )
        if r.status_code != 200:
            return notify(
                r.status_code,
                "Unable to retrieve the recent report list",
            )

        r = r.json()

        if self.private_key and r["ok"]:
            bronco_public_key = self.get_bronco_public_key()
            try:
                r["data"]["items"] = [
                    self.decrypt_bronco_in_report(report, bronco_public_key)
                    for report in r["data"]["items"]
                ]
            except KeyError:
                notify(421, "Unable to decrypt report")
            return r

        return r

    def get_report(self, identifier: str) -> dict:
        """Get a report by identifier .

        :param identifier: String representation of report id.
        :type identifier: str
        :return: Returns report
        :rtype: dict
        """
        r = self.session.get(
            urljoin(self.url, f"vpx-api/v1/report/{identifier}")
        )
        if r.status_code != 200:
            return notify(
                r.status_code,
                f"Couldn't find a report for {identifier}",
            )
        r = r.json()
        if self.private_key:
            bronco_public_key = self.get_bronco_public_key()
            self.decrypt_bronco_in_report(r["data"], bronco_public_key)
        return r

    def get_vulns_by_day(self) -> dict:
        """Get vulnerabilities by day .

        :return: Returns number of vulnerabilities by day.
        :rtype: dict
        """
        r = self.session.get(urljoin(self.url, "vpx-api/v1/aggr/vulns/by/day"))

        if r.status_code != 200:
            return notify(
                r.status_code,
                "Unable to retrieve vulnerabilities by day.",
            )
        return r.json()

    def generate_key_pair(self) -> tuple:
        """Generate a public key pair .

        :raises exceptions.InvalidStateError: Could not set the public key.
        :raises exceptions.InvalidStateError: Could not confirm the public key.
        :return: A key pair (sk, pk)
        :rtype: tuple
        """
        # Get the CSRF token from the session cookies

        csrf_token = [
            c.value
            for c in self.session.cookies
            if c.name == "csrf_access_token"
        ][0]

        # Generate a public/private key pair
        secret_key = nacl.public.PrivateKey.generate()
        public_key = secret_key.public_key
        # Propose the public key
        r = self.session.post(
            urljoin(self.url, "vpx-api/v1/pubkey"),
            headers={"X-CSRF-TOKEN": csrf_token},
            json={
                "key": public_key.encode(nacl.encoding.Base64Encoder).decode(
                    "utf-8"
                )
            },
        )

        if r.status_code != 200:
            raise exceptions.InvalidStateError(
                f"Couldn't set public key, status code {r.status_code}"
            )

        challenge = b64decode(r.json()["data"]["challenge"])

        # Send the challenge response
        unseal_box = nacl.public.SealedBox(secret_key)
        challenge_response = unseal_box.decrypt(challenge)
        r = self.session.post(
            urljoin(self.url, "vpx-api/v1/pubkey"),
            headers={"X-CSRF-TOKEN": csrf_token},
            json={
                "challenge_response": b64encode(challenge_response).decode(
                    "utf-8"
                )
            },
        )
        if r.status_code != 200:
            raise exceptions.InvalidStateError(
                f"Couldn't confirm public key, status code {r.status_code}"
            )

        return (
            public_key.encode(nacl.encoding.Base64Encoder).decode("utf-8"),
            secret_key.encode(nacl.encoding.Base64Encoder).decode("utf-8"),
        )
