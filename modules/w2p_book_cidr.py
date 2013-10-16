#!/usr/bin/env python
# coding: utf8

##adapted from https://github.com/bsterne/bsterne-tools/blob/master/cidr/cidr.py

class CIDRConv(object):
    def __init__(self, cidrs=[]):
        self.cidrs = cidrs

    def ip2bin(self, ip):
        """
        convert an IP address from its dotted-quad format to its
        32 binary digit representation
        """
        b = ""
        inQuads = ip.split(".")
        outQuads = 4
        for q in inQuads:
            if q != "":
                b += self.dec2bin(int(q),8)
                outQuads -= 1
        while outQuads > 0:
            b += "00000000"
            outQuads -= 1
        return b

    @staticmethod
    def dec2bin(n,d=None):
        """
        convert a decimal number to binary representation
        if d is specified, left-pad the binary number with 0s to that length
        """
        s = ""
        while n>0:
            if n&1:
                s = "1"+s
            else:
                s = "0"+s
            n >>= 1
        if d is not None:
            while len(s)<d:
                s = "0"+s
        if s == "": s = "0"
        return s

    @staticmethod
    def bin2ip(b):
        """
        convert a binary string into an IP address
        """
        ip = ""
        for i in range(0,len(b),8):
            ip += str(int(b[i:i+8],2))+"."
        return ip[:-1]

    def CIDR_range(self, c):
        parts = c.split("/")
        baseIP = self.ip2bin(parts[0])
        subnet = int(parts[1])
        if subnet == 32:
            return [self.bin2ip(baseIP)]
        else:
            ipPrefix = baseIP[:-(32-subnet)]
            return (self.bin2ip(ipPrefix+self.dec2bin(i, (32-subnet))) for i in xrange(2**(32-subnet)))

    def valid_ip(self, ip):
        """
        is the ip included in the cidrs ?
        """
        for cidr in self.cidrs:
            if ip in self.CIDR_range(cidr):
                return True
        return False

if __name__ == "__main__":
    ip = '192.30.252.50'
    a = CIDRConv(['204.232.175.64/27', '192.30.252.0/22'])
    print a.valid_ip(ip)
