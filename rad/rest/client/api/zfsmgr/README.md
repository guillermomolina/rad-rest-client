# ZFS Properties

```
$ zfs help -l properties
PROPERTY                            EDIT  INHERIT  VALUES
aclinherit                           YES      YES  discard | noallow | restricted | passthrough | passthrough-x | passthrough-mode-preserve
aclmode                              YES      YES  discard | mask | passthrough
atime                                YES      YES  on | off
available                             NO       NO  <size>
canmount                             YES       NO  on | off | noauto
casesensitivity                       NO      YES  sensitive | insensitive | mixed
checksum                             YES      YES  on | off | fletcher2 | fletcher4 | sha256
compression                          YES      YES  on | off | lzjb | gzip | gzip-[1-9] | zle | lz4
compressratio                         NO       NO  <1.00x or higher if compressed>
copies                               YES      YES  1 | 2 | 3
creation                              NO       NO  <date>
dedup                                YES      YES  on | off | verify | sha256[,verify]
defaultgroupquota                    YES       NO  <size> | none
defaultreadlimit                     YES      YES  <bytes/sec> | none
defaultuserquota                     YES       NO  <size> | none
defaultwritelimit                    YES      YES  <bytes/sec> | none
defer_destroy                         NO       NO  yes | no
devices                              YES      YES  on | off
effectivereadlimit                    NO       NO  <bytes/sec>
effectivewritelimit                   NO       NO  <bytes/sec>
encryption                            NO      YES  on | off | aes-128-ccm | aes-192-ccm | aes-256-ccm | aes-128-gcm | aes-192-gcm | aes-256-gcm
exec                                 YES      YES  on | off
keychangedate                         NO       NO  <date>
keysource                            YES      YES  raw | hex | passphrase,prompt | file://<path> | pkcs11: | https://<path>
keystatus                             NO       NO  undefined | unavailable | available
logbias                              YES      YES  latency | throughput
mlslabel                             YES       NO  <sensitivity label>
mounted                               NO       NO  yes | no
mountpoint                           YES      YES  <path> | legacy | none
multilevel                           YES      YES  on | off
nbmand                               YES      YES  on | off
normalization                         NO      YES  none | formC | formD | formKC | formKD
origin                                NO       NO  <snapshot>
primarycache                         YES      YES  all | none | metadata
quota                                YES       NO  <size> | none
readlimit                            YES       NO  <bytes/sec> | default | none
readonly                             YES      YES  on | off
recordsize                           YES      YES  512 to 1MB, power of 2
referenced                            NO       NO  <size>
refquota                             YES       NO  <size> | none
refreservation                       YES       NO  <size> | none | auto
rekeydate                             NO       NO  <date>
reservation                          YES       NO  <size> | none
rstchown                             YES      YES  on | off
secondarycache                       YES      YES  all | none | metadata
setuid                               YES      YES  on | off
shadow                               YES       NO  <uri> | none
share.auto                           YES       NO  on | off
share.autoname                       YES      YES  <string>
share.desc                           YES      YES  <string>
share.name                            NO       NO  <share name>
share.nfs                            YES      YES  on | off
share.nfs.aclok                      YES      YES  on | off
share.nfs.anon                       YES      YES  <uid>
share.nfs.charset.cp932              YES      YES  <access list>
share.nfs.charset.euc-cn             YES      YES  <access list>
share.nfs.charset.euc-jp             YES      YES  <access list>
share.nfs.charset.euc-jpms           YES      YES  <access list>
share.nfs.charset.euc-kr             YES      YES  <access list>
share.nfs.charset.euc-tw             YES      YES  <access list>
share.nfs.charset.iso8859-1          YES      YES  <access list>
share.nfs.charset.iso8859-13         YES      YES  <access list>
share.nfs.charset.iso8859-15         YES      YES  <access list>
share.nfs.charset.iso8859-2          YES      YES  <access list>
share.nfs.charset.iso8859-5          YES      YES  <access list>
share.nfs.charset.iso8859-6          YES      YES  <access list>
share.nfs.charset.iso8859-7          YES      YES  <access list>
share.nfs.charset.iso8859-8          YES      YES  <access list>
share.nfs.charset.iso8859-9          YES      YES  <access list>
share.nfs.charset.koi8-r             YES      YES  <access list>
share.nfs.charset.shift_jis          YES      YES  <access list>
share.nfs.cksum                      YES      YES  <stringset>
share.nfs.index                      YES      YES  <file>
share.nfs.labeled                    YES      YES  on | off
share.nfs.log                        YES      YES  <tag>
share.nfs.noaclfab                   YES      YES  on | off
share.nfs.nosub                      YES      YES  on | off
share.nfs.nosuid                     YES      YES  on | off
share.nfs.public                     YES       NO  on | off
share.nfs.sec                        YES      YES  <security mode list>
share.nfs.sec.default.none           YES      YES  <access list>
share.nfs.sec.default.ro             YES      YES  <access list>
share.nfs.sec.default.root           YES      YES  <access list>
share.nfs.sec.default.root_mapping   YES      YES  <uid>
share.nfs.sec.default.rw             YES      YES  <access list>
share.nfs.sec.dh.none                YES      YES  <access list>
share.nfs.sec.dh.ro                  YES      YES  <access list>
share.nfs.sec.dh.root                YES      YES  <access list>
share.nfs.sec.dh.root_mapping        YES      YES  <uid>
share.nfs.sec.dh.rw                  YES      YES  <access list>
share.nfs.sec.dh.window              YES      YES  <number>
share.nfs.sec.krb5.none              YES      YES  <access list>
share.nfs.sec.krb5.ro                YES      YES  <access list>
share.nfs.sec.krb5.root              YES      YES  <access list>
share.nfs.sec.krb5.root_mapping      YES      YES  <uid>
share.nfs.sec.krb5.rw                YES      YES  <access list>
share.nfs.sec.krb5i.none             YES      YES  <access list>
share.nfs.sec.krb5i.ro               YES      YES  <access list>
share.nfs.sec.krb5i.root             YES      YES  <access list>
share.nfs.sec.krb5i.root_mapping     YES      YES  <uid>
share.nfs.sec.krb5i.rw               YES      YES  <access list>
share.nfs.sec.krb5p.none             YES      YES  <access list>
share.nfs.sec.krb5p.ro               YES      YES  <access list>
share.nfs.sec.krb5p.root             YES      YES  <access list>
share.nfs.sec.krb5p.root_mapping     YES      YES  <uid>
share.nfs.sec.krb5p.rw               YES      YES  <access list>
share.nfs.sec.none.none              YES      YES  <access list>
share.nfs.sec.none.ro                YES      YES  <access list>
share.nfs.sec.none.root_mapping      YES      YES  <uid>
share.nfs.sec.none.rw                YES      YES  <access list>
share.nfs.sec.sys.none               YES      YES  <access list>
share.nfs.sec.sys.resvport           YES      YES  on | off
share.nfs.sec.sys.ro                 YES      YES  <access list>
share.nfs.sec.sys.root               YES      YES  <access list>
share.nfs.sec.sys.root_mapping       YES      YES  <uid>
share.nfs.sec.sys.rw                 YES      YES  <access list>
share.path                           YES       NO  <mountpoint-relative path>
share.point                           NO       NO  <path>
share.protocols                       NO       NO  <protocol list>
share.smb                            YES      YES  on | off
share.smb.abe                        YES      YES  on | off
share.smb.ad-container               YES      YES  <string>
share.smb.bypasstraverse             YES      YES  on | off
share.smb.catia                      YES      YES  on | off
share.smb.cont_avail                 YES      YES  on | off
share.smb.csc                        YES      YES  <empty> | disabled | manual | auto | vdo
share.smb.dfsroot                    YES       NO  on | off
share.smb.encrypt                    YES      YES  on | off
share.smb.guestok                    YES      YES  on | off
share.smb.none                       YES      YES  <access list>
share.smb.oplocks                    YES      YES  <empty> | disabled | enabled
share.smb.ro                         YES      YES  <access list>
share.smb.rw                         YES      YES  <access list>
share.state                           NO       NO  unshared | shared | invalid | unvalidated
sharenfs                             YES      YES  on | off
sharesmb                             YES      YES  on | off
snapdir                              YES      YES  hidden | visible
sync                                 YES      YES  standard | always | disabled
type                                  NO       NO  filesystem | volume | snapshot
used                                  NO       NO  <size>
usedbychildren                        NO       NO  <size>
usedbydataset                         NO       NO  <size>
usedbyrefreservation                  NO       NO  <size>
usedbysnapshots                       NO       NO  <size>
userrefs                              NO       NO  <count>
utf8only                              NO      YES  on | off
version                              YES       NO  <version> | current
volblocksize                          NO      YES  512 to 1MB, power of 2
volsize                              YES       NO  <size>
vscan                                YES      YES  on | off
writelimit                           YES       NO  <bytes/sec> | default | none
xattr                                YES      YES  on | off
zoned                                YES      YES  on | off
```

# ZFS pool propertyes

```
$ zpool help -l properties
PROPERTY       EDIT  VALUES
allocated        NO  <size>
altroot         YES  <path>
autoexpand      YES  on | off
autoreplace     YES  on | off
bootfs          YES  <filesystem>
cachefile       YES  <file> | none
capacity         NO  <size>
clustered       YES  on | off
dedupditto      YES  <threshold (min 100)>
dedupratio       NO  <1.00x or higher if deduped>
delegation      YES  on | off
failmode        YES  wait | continue | panic
free             NO  <size>
guid            YES  <guid>
health           NO  <state>
lastscrub        NO  <last scrub time>
listshares      YES  on | off
listsnapshots   YES  on | off
readonly        YES  on | off
scrubinterval   YES  manual | <count> <h | d | w | m | y>
size             NO  <size>
version         YES  <version>
```
