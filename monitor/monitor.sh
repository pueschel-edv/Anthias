#!/bin/bash

# watch processor temp
temperature=$(vcgencmd measure_temp | awk -F"=" '{print $2}')
cpu_temp=$(echo $temperature | sed 's/[^0-9.]//g')

# watch cpu and memory's load 
cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
memory_usage=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')

# monitor disk space
disk_usage=$(df -h / | awk '/\//{print $5}')

# monitor network usage
network_connections=$(netstat -tuln | awk 'NR>2{print $6}' | sort | uniq -c | awk '{print $2":"$1}')

# get last login (useful to know who accessed your device)
last_logins=$(last -n 5)

# last system event
recent_events=$(journalctl --since "10 minutes ago" --no-pager -p err..emerg)

# Is security up to date ?
security_updates=$(apt list --upgradable 2>/dev/null | grep -i security)

# check internet connectivity

wget -q --spider http://google.com

if [ $? -eq 0 ]; then
  internet_status="connected"
else
  internet_status="not connected"
fi

# get network interfaces
network_interfaces=$(ip link show | awk '$0 !~ /lo|vir|^[^0-9]/ {print $2}')

# get LAN IP address
lan_ip=$(ip addr show | awk '$1 == "inet" {print $2}' | grep -v "127.0.0.1")

# get active Docker containers
active_containers=$(docker ps -q | xargs -n 1 docker inspect --format '{{.Name}}')


json_output='{
  "date": "'$(date +'%Y-%m-%d %H:%M:%S')'",
  "temperature": "'$cpu_temp'",
  "cpu_usage": "'$cpu_usage'",
  "memory_usage": "'$memory_usage'",
  "disk_usage": "'$disk_usage'",
  "network_connections": "'$network_connections'",
  "recent_events": "'$recent_events'",
  "last_logins": "'$last_logins'",
  "security_updates": "'$security_updates'",
  "internet_status": "'$internet_status'",
  "network_interfaces": "'$network_interfaces'",
  "lan_ip": "'$lan_ip'",
  "active_containers": "'$active_containers'"
}'

# save log to file
if [ -f /home/root/screenly/monitor/monitoring.json ]; then
  echo "," >> /home/root/screenly/monitor/monitoring.json
else
    echo "[" >> /home/root/screenly/monitor/monitoring.json
fi
echo $json_output >> /home/root/screenly/monitor/monitoring.json
