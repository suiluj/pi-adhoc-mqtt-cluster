import fcntl, socket, struct

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

def get_mac_addr(ifname):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname[:15], 'utf-8')))
  return ''.join(['%02x:' % b for b in info[18:24]])[:-1]

# print (getHwAddr('eth0'))
# print (getHwAddr('wlan0'))
print (get_mac_addr('eth0'))
print (get_mac_addr('wlan0'))