#!.../dopsh
# kate: hl sh;

do-getconf mail "$(whoami)@$(hostname -f)"
echo "$mail" >$3
