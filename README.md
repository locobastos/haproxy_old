# HAProxy 2.4.9 for CentOS 7

This repository contains necessary build files of HAProxy 2.4.9 with no support and no expectation of stability. The recommended way of using the repository is to build and test your own packages.

This repository fills my needs. I am not expecting to handle all CentOS environments.

## Prerequisites

From a clean and minimal CentOS 7 server, you have to install some packages:

```bash
yum install -y epel-release && yum update -y
yum install -y gcc git rpm-build rpmdevtools
```

Then, you have to build LUA but not by following the official way (As it is explained on the official website: http://www.lua.org/download.html)

NOTE: To build HAProxy 2.4.8, you will need LUA >= 5.3. On the official CentOS 7 repositories, the latest version is 5.1.4. It is why we need to do this:

```bash
cd /opt/
curl -R -O http://www.lua.org/ftp/lua-5.4.3.tar.gz
tar zxf lua-5.4.3.tar.gz
cd lua-5.4.3/src
sed -i '/^CFLAGS/ s/$/ -fPIC/' Makefile
make
```

## Build HAProxy

Now your environment is ready, let's build HAProxy:

```bash
cd ~
git clone https://github.com/locobastos/haproxy
mkdir -p ~/rpmbuild/SOURCES/
spectool --get-files ~/haproxy/SPEC/haproxy.spec --directory ~/rpmbuild/SOURCES/
cp ~/haproxy/SOURCES/ha* ~/rpmbuild/SOURCES/
yum install -y $(rpmspec --parse ~/haproxy/SPEC/haproxy.spec | grep BuildRequires | sed 's/\\ *//g' | cut -d':' -f2)
rpmbuild --define "_lua_bin /opt/lua-5.4.3/src" -ba ~/haproxy/SPEC/haproxy.spec
cp ~/rpmbuild/RPMS/x86_64/haproxy-*.rpm ~/
cp ~/rpmbuild/SRPMS/haproxy-*.rpm ~/
```
