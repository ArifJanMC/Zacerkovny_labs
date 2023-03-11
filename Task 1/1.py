import socket

# Prompt user to enter number of packets to capture
while True:
    amount_of_packets = input("How many packets would you like to capture?\n")
    try:
        amount_of_packets = int(amount_of_packets)
        break
    except ValueError:
        # Display error message if user input is not an integer
        print("Error: please enter an integer.")

# Create a raw socket with AF_PACKET address family, SOCK_RAW type, and htons(3) protocol
sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))

# Capture the specified number of packets and store them in a list named capt
capt = [sock.recv(65535) for p in range(amount_of_packets)]

# Close the socket
sock.close()

# Loop through each packet in the list capt
for p in capt:
    # Check if the packet is an IPv4 packet based on the value of bytes 13 and 14
    if p[12:14] == b'\x08\x00' and p[33] != 255:
        # Extract the source and destination IP addresses, length of IP header, and transport layer protocol type
        src_ip = '.'.join([str(b) for b in p[26:30]])
        dst_ip = '.'.join([str(b) for b in p[30:34]])
        ip_header_len = (p[14] & 15) * 4  # length is in 4-byte words
        ip_content_type = p[23]  # protocol number

        # Determine the transport layer protocol type based on the protocol number
        if ip_content_type == 6:
            content_type_str = "tcp"
        elif ip_content_type == 17:
            content_type_str = "udp"
        else:
            content_type_str = str(ip_content_type)

        # Print the IP information, including source and destination IP addresses, length of IP header, and transport layer protocol type
        print("IPv4 packet; src IP:{}, dst IP:{}, IP header length:{}, content type:{}".format(src_ip, dst_ip,
                                                                                               ip_header_len,
                                                                                               content_type_str))

        # If the protocol is TCP, extract the source and destination port numbers and print them
        if p[23] == 6:
            src_port = int.from_bytes(p[34:36], byteorder='big')
            dst_port = int.from_bytes(p[36:38], byteorder='big')
            print("TCP segment; src port:{}, dst port:{}".format(src_port, dst_port))

    # Extract the source and destination MAC addresses from the Ethernet header and print them along with the IP information
    body = p[14:]
    dst_eth = ':'.join(['{:02x}'.format(b) for b in body[:6]])
    src_eth = ':'.join(['{:02x}'.format(b) for b in body[6:12]])
    print("Ethernet frame; src MAC:{}, dst MAC:{}".format(src_eth, dst_eth))
