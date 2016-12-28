get_ipv4addrs() {
  /sbin/ifconfig -a                                 |
  grep inet[^6]                                     |
  sed 's/.*inet[^6][^0-9]*\([0-9.]*\)[^0-9]*.*/\1/' |
  grep -v '^127\.'                                  |
  head -n 1
}
#echo $(get_ipv4addrs)
node ~/c9sdk/server.js --listen $(get_ipv4addrs) --port 20003 -a dev:scorer4sdk!
