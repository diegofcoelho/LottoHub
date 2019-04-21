import hashlib
import time


def create_hash():
    ticket_hash = hashlib.sha1()
    ticket_hash.update(str(time.time()).encode('utf-8'))
    # return ticket_hash.hexdigest()[:-10]
    return ticket_hash.hexdigest()[:10]


def create_tickets():
    return 0

