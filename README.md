# HAProxy 2.3.10 for CentOS 7

This repository contains necessary build files of HAProxy 2.3.10 with no support and no expectation of stability. The recommended way of using the repository is to build and test your own packages.

This repository fills my needs. I am not expecting to handle all CentOS environments.

## Prerequisites

From a CentOS 7 server with EPEL repositories installed, you have to install some packages:

```bash
yum install -y epel-release git rpm-build rpmdevtools
```

## HAProxy Build

Now your environment is ready, let's build HAProxy:

```
cd ~
git clone https://github.com/locobastos/haproxy
mkdir -p ~/rpmbuild/SOURCES/
spectool --get-files ~/haproxy/SPEC/haproxy.spec --directory ~/rpmbuild/SOURCES/
cp ~/haproxy/SOURCES/ha* ~/rpmbuild/SOURCES/
yum install -y $(rpmspec --parse ~/haproxy/SPEC/haproxy.spec | grep BuildRequires | sed 's/\\ *//g' | cut -d':' -f2)
rpmbuild -ba ~/haproxy/SPEC/haproxy.spec
cp ~/rpmbuild/RPMS/x86_64/haproxy-2.3.10-1.el7.x86_64.rpm ~/
cp ~/rpmbuild/SRPMS/haproxy-2.3.10-1.el7.src.rpm ~/
```
