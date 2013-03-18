cat >$3 <<"EOF"
xargs -d "\n" bup save -n $BACKUP_NAME
EOF
