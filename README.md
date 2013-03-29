Backup Tool - DOPS Recipe
=========================

Tested on:

- Fedora Linux: 18
- *please contribute to other OS*

Description
-----------

This is a daemon that sleeps and wakes up regurlarly and checks if backups need
to run. In which case, it will go through all backup sources and execute them.

The recipe set up the daemon.

DOPS Configuration
------------------

- `DOPS_MYCONF/mail`: mail address of the administrator
- `DOPS_MYCONF/mount`: mount command for the remote filesystem
- `DOPS_MYCONF/mountpoint`: mountpoint
- `DOPS_MYCONF/umount`: umount command

Portability
-----------

Must be ported to OS not using systemd.

Backup Tool - Daemon
====================

System Configuration
--------------------

*not yet documented*

