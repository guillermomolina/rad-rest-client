# Solaris RAD REST Client

This repository has a python implementation for a client to the RAD REST API and a Command Line interface (CLI) to use it. With this API and CLI you can remotely query and manage a Solaris server remotely and securely with standard https protocol.

## Using the command line

### Previous steps

- Enable rad remote service

```
$ ssh solaris sudo svcadm enable rad:remote
```

Where "solaris" is the server name.

- Get certificate

```
$ scp solaris:/etc/certs/localhost/host-ca/hostca.crt /tmp/solaris.crt
```


### Connect to to a server

```
$ rad -H solaris login admin --ssl-cert-path=/tmp/solaris.crt 
Password: 
```

Where "solaris" is the server name and "admin" is the user name.


### Use comands

```
$ rad -H solaris zpool list
NAME       SIZE  ALLOCATED     FREE  CAPACITY  DEDUPRATIO  HEALTH  ALTROOT
rpool  31.75 GB   23.74 GB  8.01 GB   74.00 B  1.00x       ONLINE  -      
```

```
$ rad -H solaris zfs list
NAME                                   USED  AVAILABLE  REFERENCED  MOUNTPOINT                 
rpool                              23.74 GB    7.51 GB    73.50 KB  /rpool                     
rpool/ROOT                         17.19 GB    7.51 GB    31.00 KB  none                       
rpool/ROOT/11.4.17.3.0              3.41 MB    7.51 GB     3.26 GB  /                          
rpool/ROOT/11.4.17.3.0/var        194.50 KB    7.51 GB     1.37 GB  /var                       
rpool/ROOT/11.4.20.4.0            101.31 MB    7.51 GB     3.27 GB  /                          
rpool/ROOT/11.4.20.4.0/var        568.50 KB    7.51 GB     1.77 GB  /var                       
rpool/ROOT/11.4.28.82.3            17.09 GB    7.51 GB     4.62 GB  /                          
rpool/ROOT/11.4.28.82.3/var         6.81 GB    7.51 GB     3.13 GB  /var                       
rpool/VARSHARE                    285.38 MB    7.51 GB    14.91 MB  /var/share                 
rpool/VARSHARE/kvol                27.75 MB    7.51 GB    31.00 KB  /var/share/kvol            
rpool/VARSHARE/kvol/dump_summary    1.22 MB    7.51 GB     1.02 MB  None                       
rpool/VARSHARE/kvol/ereports       10.25 MB    7.51 GB    10.03 MB  None                       
rpool/VARSHARE/kvol/kernel_log     16.25 MB    7.51 GB    16.03 MB  None                       
rpool/VARSHARE/pkg                 37.35 MB    7.51 GB    32.00 KB  /var/share/pkg             
rpool/VARSHARE/pkg/repositories    37.32 MB    7.51 GB    37.32 MB  /var/share/pkg/repositories
rpool/VARSHARE/sstore               9.02 MB    7.51 GB     9.02 MB  /var/share/sstore/repo     
rpool/VARSHARE/tmp                196.32 MB    7.51 GB   196.32 MB  /var/tmp                   
rpool/VARSHARE/zones               36.00 KB    7.51 GB    36.00 KB  /system/zones              
rpool/dump                          1.00 GB    7.51 GB     1.00 GB  None                       
rpool/export                      794.50 KB    7.51 GB    32.00 KB  /export                    
rpool/export/home                 762.50 KB    7.51 GB    32.00 KB  /export/home               
rpool/export/home/admin           730.50 KB    7.51 GB   730.50 KB  /export/home/admin         
rpool/oci                          24.52 MB    7.51 GB    31.00 KB  /var/lib/oci/filesystems   
rpool/oci/9TA8KSELN0RYJ782         24.49 MB    7.51 GB    24.11 MB  none                       
rpool/repos                         1.16 GB    7.51 GB     1.16 GB  /repos                     
rpool/swap                          1.00 GB    7.51 GB     1.00 GB  None                       
rpool/zones                         3.07 GB    7.51 GB     3.07 GB  /zones                     
```

```
$ rad -H solaris zone list
ID  NAME      BRAND       STATE  
1   intranet  solaris-kz  running
5   pkg       solaris     running
16  ops       solaris-kz  running
4   test      solaris10   running
```

## [Solaris RAD REST info](https://github.com/oracle/oraclesolaris-contrib/blob/master/REST/README.md)
