# coding = utf8
import traceback
import logging


def send_error_msg(msg=''):
    logging.info(msg)
    traceback.print_exc()


def is_ip_valid(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        try:
            if not 0 <= int(item) <= 255:
                return False
        except:
            return False
    return True




if __name__ == '__main__':
    proxy = 'http://171.39.40.3:8450'
    ip = proxy.replace('http://', '').split(':')[0]
    print ip
    print is_ip_valid(ip)
