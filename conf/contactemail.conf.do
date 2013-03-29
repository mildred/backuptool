#!.../dopsh
# kate: hl sh;

do-conf - c=mail v="$(whoami)@$(hostname -f)" >$3
