okautoconf for Asterisk
=======================
What is it used for? It's used for calling emergency teams where you need to contact
everyone really quickly.

This package manages asterisk callout groups, basic flow:

 * User calls for example extension 2010
 * Asterisk calls all users defined by this extension
 * Asterisk joins all members into a conference

It also contains a CGI script to manage the extensions via web.


![okautoconf List](http://opinkerfi.github.com/okautoconf/okautoconf-list.png)

![okautoconf Edit](http://opinkerfi.github.com/okautoconf/okautoconf-edit.png)


Install
-------
These instructions are tested on Trixbox CE


Download
```
wget -O okautoconf-1.0.0.tar.gz https://github.com/opinkerfi/okautoconf/tarball/1.0.0
```

Create configuration dir, example
```
mkdir /etc/okautoconf
chown asterisk:asterisk /etc/okautoconf
```

Copy AGI script to the correct dir, example
```
install -m 755 agi-bin/okautoconf.pl /var/lib/asterisk/agi-bin/okautoconf.pl
```

Copy the CGI script to apache cgi-bin, example
```
install -m 755 cgi-bin/okautoconf.cgi /var/www/cgi-bin/okautoconf.cgi
```

Copy CSS for the CGI script to html directory
```
cp html/okautoconf.css /var/www/html/
```

Configure
---------
Include the okautoconf in a relevant place, for instance
/etc/asterisk/extensions_custom.conf under "from-internal-custom".

```
[from-internal-custom]
include => custom-okautoconf
```

Configure extensions that shall use okautoconf, example say 98XX are allocated
to okautoconf, also add the "custom-okautoconfmember" context

Take care that ${OUT_1} is your first configured trunk, you might want to use something different
```
[custom-okautoconf]
exten => _98XX,1,Answer
exten => _98XX,n,Wait(1)
exten => _98XX,n,AGI(okautoconf.pl,${EXTEN},${OUT_1})
exten => _98XX,n,Meetme(${CONFERENCEID},xqd)


[custom-okautoconfmember]
exten => s,1,Answer
exten => s,n,Wait(1)
exten => s,n,Meetme(${CONFERENCEID},xqd)
```

Now you should be ready to reload asterisk and go to 
http://yourasterisk/cgi-bin/okautoconf.cgi and configure your extensions.
