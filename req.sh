while :
do
	exec 3<>/dev/tcp/$1/$2
	echo -e "GET / HTTP/1.0\r\n\r\n" >&3
done
