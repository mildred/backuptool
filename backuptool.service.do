cat >$3 <<EOF
[Unit]
Description=Make sure backups are ran regularly

[Service]
ExecStart=$BINDIR/backuptool
Nice=10
Restart=always
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
EOF
