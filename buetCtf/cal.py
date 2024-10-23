# a = SSH + HTTP + UPS
# b = RDP - SLP
# c = (Telnet + FTP) * SMTP
# d = STUN * Echo

# flag = c(b -a) + d
SSH = 22
HTTP = 80
UPS = 401
RDP = 3389
SLP = 427
Telnet = 23
FTP = 21
SMTP = 465  # 3535, 587, 465 , 25
STUN = 3478
Echo = 7


a= (SSH + HTTP + UPS)
b = RDP - SLP
c = (Telnet + FTP) * SMTP
d = STUN * Echo


flag =  c * (b - a) + d
print(flag)
# //2729246