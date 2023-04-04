import socket

dhcp_msg_type = {
1:'DHCPDISCOVER',
2:'DHCPOFFER',
3:'DHCPREQUEST',
4:'DHCPDECLINE',
5:'DHCPACK',
6:'DHCPNAK',
7:'DHCPRELEASE'
}

def IPv4_str(fourbytes):
    return '.'.join([ str(b) for b in fourbytes ])

def Eth_str(sixbytes):
    return ':'.join([ '{:02x}'.format(b) for b in sixbytes])

def parse_dhcp_msg(messg):
    op,htype,hlen,hops = message[:4]
    xid = message[4:8]
    seconds = message[8:10]
    flags=message[10:12]
    ciaddr=message[12:16]
    yiaddr=message[16:20]
    siaddr=message[20:24]
    giaddr=message[24:28]
    chaddr=message[28:44]
    sname=message[44:108]
    file=message[108:236]
    options=message[236:]
    return op,htype,hlen,hops,xid,seconds,flags,ciaddr,yiaddr,siaddr,giaddr,chaddr,sname,file,options

def parse_dhcp_options(opts):
    if len(opts)>0 and (opts[0]!=0xff):
        opt_type = opts[0]
        opt_length = opts[1]
        dhcp_msg[opt_type]=opts[2:2+opt_length]
        parse_dhcp_options(opts[2+opt_length:])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
server_socket.bind(('', 67))

while True:
    dhcp_msg = {}
    message, address = server_socket.recvfrom(1024)
    op,htype,hlen,hops,xid,seconds,flags,ciaddr,yiaddr,siaddr,giaddr,chaddr,sname,file,options = parse_dhcp_msg(message)
    xid_int = int.from_bytes(xid,'big')
    secs_int = int.from_bytes(seconds,'big',signed=True)
    ciaddr_str=IPv4_str(ciaddr)
    yiaddr_str=IPv4_str(yiaddr)
    siaddr_str=IPv4_str(siaddr)
    giaddr_str=IPv4_str(giaddr)
    chaddr_eth=Eth_str(chaddr[:hlen])
    if options[:4]==b'\x63\x82\x53\x63':
        parse_dhcp_options(options[4:])
    else:
        print("Invalid magic cookie in the message options beginning:",options[:4])

    print('Start--------------------------------------------------')
    print(f"srcIP: {address}, msgLen: {len(message)}, oper: {op}, htype: {htype}, h1en: {hlen}, hops: {hops}, msgID: {xid_int}, seconds: {secs_int}, bootp_flags: {flags}")
    print(f"clientIP: {ciaddr_str}, yourIP: {yiaddr_str}, client_hwAddr: {chaddr_eth}")
    print('Msg type:', dhcp_msg_type[(dhcp_msg[53])[0]])

    if 61 in dhcp_msg:
        client_id = Eth_str(dhcp_msg[61])
        print(f"Client ID: {client_id}")
    if 60 in dhcp_msg:
        client_type = dhcp_msg[60].decode("utf-8")
        print(f"Client type: {client_type}")
    if 57 in dhcp_msg:
        max_msg_size = int.from_bytes(dhcp_msg[57], 'big')
        print(f"Max. msg. size: {max_msg_size}")
    if 12 in dhcp_msg:
        host_name = dhcp_msg[12].decode("utf-8")
        print(f"Host name: {host_name}")
    if 55 in dhcp_msg:
        param_req_list = [b for b in dhcp_msg[55]]
        print(f"Parameter Request List: {param_req_list}")

    print('unparsed dhcp_msg:', dhcp_msg)
    print('End---------------------------------------------------')
    server_socket.sendto(message, address)

