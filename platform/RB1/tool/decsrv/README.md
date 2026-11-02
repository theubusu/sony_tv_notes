# decsrv
decsrv is a remote service running on the TV, that will nicely decrypt the contents of a FRA file for you.

It consits of:
- `decmod.c`, kernel module that calls directly into `decrypt_data` of sonyrd, and provides an interface to it on `/dev/sonydec`
- `decsrv.c`, socket server that exposes the interface to the network 
- `decsrv.py` - python client for decsrv, used in `fra.py`