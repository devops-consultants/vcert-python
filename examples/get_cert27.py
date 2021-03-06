#!/usr/bin/env python2
#
# Copyright 2019 Venafi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from vcert import CertificateRequest, Connection, CloudConnection, FakeConnection, TPPConnection, RevocationRequest
import string
import random
import logging
import time
from os import environ

logging.basicConfig(level=logging.INFO)
logging.getLogger("urllib3").setLevel(logging.ERROR)


def main():
    # Get credentials from environment variables
    token = environ.get('TOKEN')
    user = environ.get('TPPUSER')
    password = environ.get('TPPPASSWORD')
    url = environ.get('TPPURL')
    zone = environ.get("ZONE")
    # connection will be chosen automatically based on what arguments are passed,
    # If token is passed Venafi Cloud connection will be used. if user, password, and URL Venafi Platform (TPP) will
    # be used. If none, test connection will be used.
    conn = Connection(url=url, token=token, user=user, password=password)
    # If your TPP server certificate signed with your own CA or available only via proxy you can specify requests vars
    # conn = Connection(url=url, token=token, user=user, password=password,
    #                   http_request_kwargs={"verify": "/path/to/trust/bundle.pem"})

    print("Trying to ping url %s" % conn._base_url)
    status = conn.ping()
    print("Server online: %s" % status)
    if not status:
        print('Server offline - exit')
        exit(1)

    request = CertificateRequest(common_name=randomword(10) + u".venafi.example.com")
    request.san_dns = [u"www.client.venafi.example.com", u"ww1.client.venafi.example.com"]
    if not isinstance(conn, CloudConnection):
        # Venafi Cloud doesn't support email or IP SANs in CSR
        request.email_addresses = [u"e1@venafi.example.com", u"e2@venafi.example.com"]
        request.ip_addresses = [u"127.0.0.1", u"192.168.1.1"]
        # Specify ordering certificates in chain. Root can be "first" or "last". By default it last. You also can
        # specify "ignore" to ignore chain (supported only for Platform).

    # make certificate request
    conn.request_cert(request, zone)

    # and wait for signing
    while True:
        cert = conn.retrieve_cert(request)
        if cert:
            break
        else:
            time.sleep(5)

    # after that print cert and key
    print("\n".join([cert.full_chain, request.private_key_pem]))
    # and save into file
    f = open("/tmp/cert.pem", "w")
    f.write(cert.full_chain)
    f = open("/tmp/cert.key", "w")
    f.write(request.private_key_pem)
    f.close()

    if not isinstance(conn, FakeConnection):
        # fake connection doesn`t support certificate renewing
        print("Trying to renew certificate")
        new_request = CertificateRequest(
            id=request.id,
        )
        conn.renew_cert(new_request)
        while True:
            new_cert = conn.retrieve_cert(new_request)
            if new_cert:
                break
            else:
                time.sleep(5)
        print(new_cert.cert)
        fn = open("/tmp/new_cert.pem", "w")
        fn.write(new_cert.cert)
    if isinstance(conn, TPPConnection):
        revocation_req = RevocationRequest(id=request.id,
                                           comments="Just for test")
        print("Revoke", conn.revoke_cert(revocation_req))


def randomword(length):
    letters = string.ascii_lowercase
    return u''.join(random.choice(letters) for i in range(length))


if __name__ == '__main__':
    main()
