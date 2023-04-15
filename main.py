import socket, struct, win32api, win32con, pyautogui

addr = ["ip","port"]
server = socket.create_server(tuple(addr))

server.listen()
print("Server is up and running!")
width, height = pyautogui.size()
lastPacket = time.time()
def doStuff():
	global lastPacket
	clientSock, addr = server.accept()

	while not clientSock._closed:
		data = clientSock.recv(10)
		if(data == b""):
			print("Disconnected, waiting for new client...")
			break
		try:
			decoded = struct.unpack("<bbII",data)
		except Exception:
			print("wrong data")
		else:
			x = decoded[3] / 10 ** decoded[0]
			y = 1 - (decoded[2] / 10 ** decoded[0])
			press = bool(decoded[1])
			#print(f"New data: resolution: {decoded[0]}, x: {x}, y: {y}, press: {press}")
			win32api.SetCursorPos((int(x * width), int(y * height)))
			if(press):
				win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
			else:
				win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

while True:
	doStuff()