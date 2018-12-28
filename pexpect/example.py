# coding: utf-8

import pexpect

target_host_list = [
]

def check_crontab(host):
    print('-----')
    print(host)
    print('-----')

    # EC2 login
    c = pexpect.spawn('ssh %s' % host)
    c.expect(r'\[.* ~\]\$ ')

    # check crontab
    c.sendline('sudo crontab -l')
    c.expect(r'\[.* ~\]\$ ')
    print(c.before.decode())

    # check process
    c.sendline('egrep "ruby" <<< "$(ps -ef)"')
    c.expect(r'\[.* ~\]\$ ')
    print(c.before.decode())

    # session close
    c.close()

def all_check_crontab(host_list):
    for host in host_list:
        check_crontab(host)

if __name__ == '__main__':
    all_check_crontab(target_host_list)
