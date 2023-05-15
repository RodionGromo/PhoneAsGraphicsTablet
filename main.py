import socket, struct, win32api, win32con, pyautogui, time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("ip","port"))
server_socket.listen()
print("Waiting for user!")
width, height = pyautogui.size()
isLow = False

def udpServer():
	global isLow
	userSock, addr = server_socket.accept()
	print(f"User connected! IP: {addr}")
	while True:
		try:
			data = userSock.recv(11)
		except ConnectionResetError:
			print("User disconnected!")
			break
		if not data:
			break
		try:
			decoded = struct.unpack("<bbIIc",data)
		except Exception as e:
			print(f"wrong data: {data}")
			print(e)
		else:
			x = decoded[3] / 10 ** decoded[0]
			y = 1 - (decoded[2] / 10 ** decoded[0])
			press = bool(decoded[1])
			#print(f"New data: resolution: {decoded[0]}, x: {x}, y: {y}, press: {press}")
			win32api.SetCursorPos((int(x * width), int(y * height)))
			if(press and not isLow):
				isLow = True
				win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
			elif(not press and isLow):
				isLow = False
				win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

while True:
	udpServer()
	time.sleep(1)
