"""
Author: snoopbanana
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my own simple program to recreate three-way handshakes of TCP.
"""

"""
You should have Wireshark to see threeway-handshakes process.
"""

# Import scapy as a main core for threeway handshakes 
from scapy.all import IP, TCP, UDP, sr1, send, DNS, DNSQR, ICMP
import random


"""Extract IP from domain by sending packet to server and expect extracting IP address from server's response"""
def extract_ip_from_domain() -> str:
    domain = input("Type your target domain: ")

    # Use Google DNS query (OK with most public IP)
    # Encapsulate the packet
    packet = (
        IP(dst="192.168.1.1")/ # Replace your own DNS address
        UDP(dport=53)/
        DNS(rd=1, qd=DNSQR(qname=domain))
    )


    # sr1 sends packet, waits and catch the first packet from server
    # verbose=0 means you do not want any log sent off from server
    response = sr1(packet, timeout=3, verbose=0)

    if response and response.haslayer(DNS):
        for i in range(response[DNS].ancount):
            answer = response[DNS].an[i]
            if answer.type == 1: # A record (IPv4)
                return answer.rdata

"""
Simulate how threeway handshakes works
SYN | ACK = IP header + TCP trailer
Client-side: send SYN -> receive SYN-ACK -> send ACK

sr1 = send SYN + receive SYN-ACK
"""
def threeway_handshakes(target_ip) -> None:
    # Generate an ephemeral source port (from 49152 to 65535)
    sport = random.randint(49152, 65535)
    # Generate random sequence number
    seq = random.randint(0, 2 ** 32 - 1)
    
    print(f'Your source port is {sport}. Paste "tcp.port=={sport}" in Wireshark display filtere')
    input("Press Enter to continue: ")

    syn = IP(dst=target_ip)/TCP(
        sport=sport,
        dport=80,
        flags="S",
        seq=seq
    )

    # Send SYN and catch SYN-ACK while listening
    synack=sr1(syn)


    ack = IP(dst=target_ip)/TCP(
        sport=sport,
        dport=80,
        flags="A",
        seq=seq + 1,
        ack=synack.seq + 1
    )

    send(ack)

def main():
    target_ip = extract_ip_from_domain()
    threeway_handshakes(target_ip)

if __name__ == "__main__":
    main()




