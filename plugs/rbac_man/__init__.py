def test_ip(ip=None, iptables=None):
    from uliweb import request, settings
    
    ip = ip or request.remote_addr
    iptables = iptables or settings.PARA.CAN_READ_FILES_IPS
    return ip_can_visit(ip, iptables)
    
def ip_can_visit(ip, ips):
    t = [int(x) for x in ip.split('.')]
    #tables = []
    for x in ips:
        #d = []
        flag = True
        for j, y in enumerate(x.split('.')):
            if '-' in y:
                b, e = [int(i) for i in y.split('-')]
                if not (b <= t[j] <= e):
                    flag = False
                    break
                #d.append(b)
            elif y == '*':
                #d.append(y)
                continue
            else:
                #d.append(int(y))
                if t[j] != int(y):
                    flag = False
                    break
        if flag:
            return True
        #tables.append(d)
    return False

if __name__ == '__main__':
    iptables = ['128.192.200-203.*', '128.192.215-217.*']
    print ip_can_visit('127.0.0.1', iptables)
    print ip_can_visit('128.192.200.1', iptables)
    print ip_can_visit('128.192.204.1', iptables)