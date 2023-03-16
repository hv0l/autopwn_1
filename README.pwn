the challenge machine has a vulnerable web server on port 80, after some fuzzing we find an id_rsa. Once cracked with ssh2john we see that the password of id_rsa is "goodcat9".
Unfortunately the ssh service runs on a non-standard port which changes every 60 seconds.
However, the port always seems to be between 31000-31200
Once logged into the machine we see that sudo -l allows us to issue the command:
sudo nmap
sudo nmap --interactive
nmap> !sh
But the connection lasts very little and we get kicked out, we want to create a persistence by automating
