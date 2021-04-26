# HAProxy 2.3.10 for CentOS 7

This repository contains necessary build files of HAProxy 2.3.10 with no support and no expectation of stability. The recommended way of using the repository is to build and test your own packages.

This repository fills my needs. I am not expecting to handle all CentOS environments.

## Prerequisites

From a CentOS 7 server with EPEL repositories installed, you have to install some packages:

```bash
yum install -y epel-rpm-macros gcc git openssl-devel pcre2-devel rpm-build spectool systemd-devel zlib-devel
```

Then you have to build LUA but not by following the official way (As it is explained on the official website: http://www.lua.org/download.html)

NOTE: To build HAProxy 2.3.10, you will need LUA >= 5.3. On the officials CentOS 7 repositories, the latest version is 5.1.4. It why we need to do this:

NOTE2: It is very important to build LUA on /opt/lua-5.4.3 as this folder is hardcoded in the SPEC file. If you want to specify another folder, you have to fix haprvoxy.spec to modify these values: `LUA_INC=/opt/lua-5.4.3/src LUA_LIB=/opt/lua-5.4.3/src`

```
cd /opt/
curl -R -O http://www.lua.org/ftp/lua-5.4.3.tar.gz
tar zxf lua-5.4.3.tar.gz
cd /opt/lua-5.4.3/src
sed -i '/^CFLAGS/ s/$/ -fPIC/' Makefile
make
```

## HAProxy Build

Now your environment is ready, let's build HAProxy:

```
cd ~
git clone https://github.com/locobastos/haproxy
rpmdev-setuptree
spectool -g ~/haproxy/SPEC/haproxy.spec -C ~/rpmbuild/SOURCES/
cp ~/haproxy/SOURCES/ha* ~/rpmbuild/SOURCES/
rpmbuild -ba ~/haproxy/SPEC/haproxy.spec
cp ~/rpmbuild/RPMS/x86_64/haproxy-2.3.10-1.el7.x86_64.rpm ~/
cp ~/rpmbuild/SRPMS/haproxy-2.3.10-1.el7.src.rpm ~/
```

