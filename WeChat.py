#!/usr/bin/python
#-*- encoding: utf-8 -*-

''' Mengimport library untuk aplikasi '''
import socket														# Library untuk koneksi
from threading import Thread						# Library untuk multithreading
import os, platform, time, sys					# Library untuk tugas sistem operasi
import random														# Library untuk pemilihan acak
from datetime import datetime						# Library untuk waktu
import colorama													# Library untuk pewarna teks
from colorama import Fore, Back, Style	# Library untuk pewarna teks

''' Pewarnaan '''
warnaList = [
	[ # List Pertama Untuk Warna Foreground Text
		Fore.RED, Fore.LIGHTRED_EX,
		Fore.GREEN, Fore.LIGHTGREEN_EX,
		Fore.BLUE, Fore.LIGHTBLUE_EX,
		Fore.YELLOW, Fore.LIGHTYELLOW_EX,
		Fore.CYAN, Fore.LIGHTCYAN_EX,
		Fore.MAGENTA, Fore.LIGHTMAGENTA_EX,
		Fore.WHITE, Fore.LIGHTWHITE_EX
	], [ # List Kedua Untuk Warna Background Text
		Back.RED, Back.LIGHTRED_EX,
		Back.GREEN, Back.LIGHTGREEN_EX,
		Back.BLUE, Back.LIGHTBLUE_EX,
		Back.YELLOW, Back.LIGHTYELLOW_EX,
		Back.CYAN, Back.LIGHTCYAN_EX,
		Back.MAGENTA, Back.LIGHTMAGENTA_EX,
		Back.WHITE, Back.LIGHTWHITE_EX
	] # 0 = Foreground, 1 = Background
]
warnaStyle = [Style.DIM, Style.NORMAL, Style.BRIGHT]	# Style : Italic, Normal, Bold
warnaInit = colorama.init()														# Inisialisasi console untuk colorama
warnaReset = [Fore.RESET, Style.RESET_ALL]						# Me-reset pewarnaan

''' Banner aplikasi '''
teksBanner = f'''
  __      __         ___    _                _     
  \ \    / / ___    / __|  | |_     __ _    | |_   
   \ \/\/ / / -_)  | (__   | ' \   / _` |   |  _|  
    \_/\_/  \___|   \___|  |_||_|  \__,_|   _\__|
  _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
  "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
       <[ Created with {warnaList[0][0]}<3{warnaReset[0]} by Kelompok 1 OOP ]>
           <( Coded by Muhammad Rizky )>
                   (versi 1.0)
'''

''' Kelas Utilitas untuk fitur-fitur tambahan di dalam program
Contoh : pembersihan layar/console, menampilkan info hostname dan IP Address '''
class Utilitas:
	hostname = socket.gethostname()							# Mendapatkan info hostname komputer client
	ip_saya = socket.gethostbyname(hostname)		# Mendapatkan info IP Address client
	# Method untuk membersihkan layar/console
	def bersihkan_layar():
		if platform.system() == "Windows":
			os.system('cls')		# Jika platform sistem operasinya Windows
		else:
			os.system('clear')	# Jika platform sistem operasinya selain Windows
	# Method untuk menampilkan info hostname dan IP Address client
	def info_jaringan():
		print(f"\n[i] Hostname   : {Utilitas.hostname}")
		print(f"[i] IP Address : {Utilitas.ip_saya}\n")

''' Kelas Server untuk keperluan Server-Side '''
class Server():
	# Method untuk inisialisai saat instansi/objek dari kelas dibuat
	def __init__(self, IP, Port):
		self.daftarClient = set()						# Membuat set/himpunan untuk menampung client
		#self.koneksi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.koneksi = socket.socket()			# Inisialisasi socket untuk jaringan
		self.serverIP = IP									# Variabel serverIP
		self.serverPort = Port							#	Variabel serverPort
		print(f"[*] Mengatur IP server -> {self.serverIP}")
		print(f"[*] Mengatur Port server -> {self.serverPort}")
	# Method untuk mengaktifkan fungsi Server-Side
	def aktif(self):
		print(f"[+] Mengaktifkan server pada {self.serverIP}:{self.serverPort}")
		self.koneksi.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# Memastikan port dapat digunakan
		self.koneksi.bind((self.serverIP, self.serverPort))									# Membuka koneksi port pada server
		self.koneksi.listen(3)																							# Mendengarkan koneksi masuk
		print(f"[*] Menunggu koneksi dari client ...")
	# Method untuk menerima koneksi dari client
	def terima(self):
		return self.koneksi.accept()
	# Method untuk menunggu pesan dari client untuk di-broadcast
	def monitoring(self, koneksiClient, IPClient):
		# Looping untuk terus menunggu pesan
		while True:
			# Mencoba menangkap pesan dari client
			try:
				pesan_broadcast = koneksiClient.recv(1024).decode()
			# Jika terjadi error (Exception, ConnectionAbortedError, ConecctionResetError)
			except:
				print(f"[-] {IPClient} terputus dari server")
				self.daftarClient.remove(koneksiClient)						# Menghapus client dari himpunan client
			# Melakukan broadcast pesan kepada seluruh client
			for client in self.daftarClient:
				# Mencoba mengirim pesan kepada client
				try:
					client.send(pesan_broadcast.encode())
				# Jika gagal karena koneksi, skip tanpa pesan error
				except ConnectionResetError:
					pass
	# Method untuk menambahkan client ke set/himpunan client
	def tambahClient(self, koneksiClient, IPClient):
		self.daftarClient.add(koneksiClient)
		print(f"[+] {IPClient} terhubung dengan server")

''' Kelas untuk keperluan Client-Side '''	
class Client():
	# Method untuk inisialisai saat instansi/objek dari kelas dibuat
	def __init__(self, IP, Port):
		#self.koneksi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.koneksi = socket.socket()
		self.serverIP = IP
		self.serverPort = Port
		print(f"[*] Mengatur IP server -> {self.serverIP}")
		print(f"[*] Mengatur Port server -> {self.serverPort}")
	# Method untuk menghubungkan client dengan server
	def hubungkan(self):
		print(f"[*] Mencoba terhubung dengan server {self.serverIP}:{self.serverPort} ...")
		# Mencoba terhubung dengan server
		try:
			self.koneksi.connect((self.serverIP, self.serverPort))
			print("[+] Berhasil terhubung dengan server")
			self.statusKoneksi = "Berhasil"
		# Jika gagal terhubung dengan server
		except Exception:
			print("[-] Gagal terhubung dengan server")
			self.statusKoneksi = "Gagal"
	# Method untuk menunggu pesan broadcast dari server
	def monitoring(self):
		# Looping untuk terus menunggu pesan
		while True:
			# Mencoba menangkap pesan dari server
			try:
				pesan_masuk = self.koneksi.recv(1024).decode()
				print(pesan_masuk)
			# Jika gagal karena koneksi server terputus
			except ConnectionAbortedError:
				print("[!] Koneksi dengan server terputus!")
				exit()
	# Method untuk mengirim pesan kepada server
	def kirim(self, pesan):
		self.koneksi.send(pesan.encode())

''' Fungsi Server-Side '''
def ServerSide():
	koneksiServer = Server("0.0.0.0", 5522)		# Membuat instansi/objek
	koneksiServer.aktif()											# Mengaktifkan server
	# Menunggu koneksi dari client
	while True:
		try:
			koneksiClient, IPClient = koneksiServer.terima()
			koneksiServer.tambahClient(koneksiClient, IPClient)
			try:
				proses = Thread(target=koneksiServer.monitoring, args=(koneksiClient,IPClient,))
				proses.daemon = True
				proses.start()
			except Exception:
				print("[!] Error pada thread server")
				proses.stop()
		except KeyboardInterrupt:
			print("[!] Interupsi keyboard terdeteksi!")
			break
	# Memutuskan koneksi client
	print("[*] Memutuskan koneksi seluruh client ...")
	for client in koneksiServer.daftarClient:
		client.close()
	# Menonakifkan server
	print(f"[*] Menonaktifkan server pada {koneksiServer.serverIP}:{koneksiServer.serverPort}")
	koneksiServer.koneksi.close()
	exit()

''' Fungsi Client-Side '''
def ClientSide():
	# Meminta informasi terkait server
	tanyaIP = input("[>] IP Address Server : ")
	if tanyaIP == "":
		print("[!] Masukkan IP Address Server!\n")
		ClientSide()
	# Mencoba terhubung dengan server
	koneksiClient = Client(tanyaIP, 5522)
	koneksiClient.hubungkan()
	if koneksiClient.statusKoneksi == "Gagal":
		input(f"{warnaStyle[2]}[TEKAN ENTER ...]{warnaReset[1]}")
		WeChatApp()
	print()
	# Mengatur username chat (jika tidak diisi, diberi username random)
	usernameClient = input("[>] Username : ")
	try:
		if usernameClient == "":
			usernameClient = f"unknown{random.randint(1000,9999)}"
	except KeyboardInterrupt:
		exit()
	# Membersihkan layar dan tampilkan banner
	Utilitas.bersihkan_layar()
	print(teksBanner)
	# Pesan ketika login/logout
	warnaClient = warnaList[0][random.randint(1,11)]		# Memilih warna teks chat untuk client saat di room
	pesan_login = f"{warnaList[0][12]}// '{usernameClient}' bergabung ke dalam room! //{warnaReset[0]}"
	pesan_logout = f"{warnaList[0][12]}// '{usernameClient}' meninggalkan room ... //{warnaReset[0]}"
	koneksiClient.kirim(pesan_login)
	# Menunggu pesan broadcast dari server
	try:
		proses = Thread(target=koneksiClient.monitoring)		# Membuat multithreading untuk proses koneksi
		proses.daemon = True																# Berjalan di latar belakang
		proses.start()																			# Mulai menjalankan multithreading
	except Exception:
		print("[!] Error pada thread client")
		proses.stop()
	except ConnectionAbortedError:
		proses.stop()
		pass
	# Mengambil input untuk mengirim pesan ke server
	time.sleep(1)
	while True:
		try:
			pesan_ketik = input("\r")
			# Jika client mengetikkan <WeQuit> maka keluar dari room
			if pesan_ketik == "<WeQuit>":
				koneksiClient.kirim(pesan_logout)
				break
			# Jika client mengetikkan <WeInfo> maka menampilkan info_jaringan()
			elif pesan_ketik == "<WeInfo>":
				Utilitas.info_jaringan()
			timestamp = datetime.now().strftime("%H:%M:%S")			# Timestamp chat
			pesan_kirim = f"{warnaClient}[{timestamp}][{usernameClient}] > {pesan_ketik}{warnaReset[0]}"
			koneksiClient.kirim(pesan_kirim)										# Mengirim pesan kepada server
		except KeyboardInterrupt:
			koneksiClient.kirim(pesan_logout)
			break
	# Memutuskan koneksi
	time.sleep(1)
	print("\n[*] Memutuskan koneksi dari server ...")
	try:
		koneksiClient.koneksi.close()
	except ConnectionAbortedError:
		pass # Menyembunyikan pesan error
	exit()

# Fungsi utama aplikasi
def WeChatApp():
	Utilitas.bersihkan_layar()
	print(teksBanner)
	print("[#] PILIH MODE PENGGUNAAN [#]")
	print("\n(1) Server\n(2) Client\n")
	mode = input("[>] Pilihan : ")
	if mode == "1":
		Utilitas.bersihkan_layar()
		print(teksBanner)
		ServerSide()
	elif mode == "2":
		Utilitas.bersihkan_layar()
		print(teksBanner)
		ClientSide()
	else:
		print(f"[!] Error: Pilihan {mode} tidak tersedia\n")
		input(f"{warnaStyle[2]}[TEKAN ENTER ...]{warnaReset[1]}")
		WeChatApp()

# Menjalankan aplikasi
if __name__ == '__main__':
	WeChatApp()

''' Credit
ASCII Art Generator by PatorJK : https://patorjk.com/software/taag/
Coding Reference : thepythoncode.com
'''