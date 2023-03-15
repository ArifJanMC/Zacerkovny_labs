import socket

def get_packet_count():
    while True:
        packet_count = input("Enter the number of packets to capture: ")
        try:
            return int(packet_count)
        except ValueError:
            print("Invalid input. Please enter an integer.")

def create_socket():
    return socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))

def capture_packets(sock, num_packets):
    return [sock.recv(65535) for _ in range(num_packets)]

def process_packets(packets):
    for packet in packets:
        if packet[12:14] == b'\x08\x00' and packet[33] != 255:
            source_ip = '.'.join(map(str, packet[26:30]))
            dest_ip = '.'.join(map(str, packet[30:34]))
            ip_header_length = (packet[14] & 15) * 4
            ip_protocol = packet[23]

            if ip_protocol == 6:
                protocol_str = "tcp"
            elif ip_protocol == 17:
                protocol_str = "udp"
            else:
                protocol_str = str(ip_protocol)

            print(f"IPv4 packet; src IP:{source_ip}, dst IP:{dest_ip}, IP header length:{ip_header_length}, content type:{protocol_str}")

            if ip_protocol == 6:
                source_port = int.from_bytes(packet[34:36], 'big')
                dest_port = int.from_bytes(packet[36:38], 'big')
                print(f"TCP segment; src port:{source_port}, dst port:{dest_port}")

        eth_payload = packet[14:]
        dest_mac = ':'.join([f'{b:02x}' for b in eth_payload[:6]])
        source_mac = ':'.join([f'{b:02x}' for b in eth_payload[6:12]])
        print(f"Ethernet frame; src MAC:{source_mac}, dst MAC:{dest_mac}")

def main():
    packet_count = get_packet_count()
    sock = create_socket()
    packets = capture_packets(sock, packet_count)
    sock.close()
    process_packets(packets)

if __name__ == '__main__':
    main()
