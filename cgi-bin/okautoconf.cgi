#!/usr/bin/python

import cgitb
import cgi
import os, pwd
import sys

extension_dir ="/etc/okautoconf"

cgitb.enable()
dbh = None

output_buffer = ''

def main():
    form = cgi.FieldStorage()

    check_setup()

    if form.has_key('add'):
        html_header('add')

        if form.has_key('number'):
            ext_add(form['number'].value, form['name'].value)
            html_ext_edit(form['number'].value)
        else:
            html_ext_add()

        html_footer()
    elif form.has_key('edit'):
        if form.has_key('eadd'):
            ext_add(form['edit'].value, member=form['eadd'].value)
        elif form.has_key('edel'):
            ext_del(form['edit'].value, form['edel'].value)
        html_header('edit')
        html_ext_edit(form['edit'].value)
        html_footer()
    else:
        html_header('list')
        extensions = ext_get()
        html_ext_list(extensions)
        html_footer()
    html_send()

def html_send():
    global output_buffer

    print output_buffer

def check_setup():
    if os.path.exists('/etc/okautoconf') is False:
        mylogin = pwd.getpwuid(os.getuid())[0]
        html_error("""
/etc/okautoconf directory does not exist, please create it and make writable for %s<br/><br/>
Example:<br/>
<pre>
mkdir /etc/okautoconf
chown %s /etc/okautoconf
</pre>
""" % (mylogin, mylogin))

def ext_add(number, name=None, member=None):
    global extension_dir

    fh = open("%s/%s" % (extension_dir, number), 'a')

    if name is not None:
        fh.write("%s\n" % (name))
    if member is not None:
        fh.write("%s\n" % (member))

    return True


def html_ext_edit(number, header=0):
    global output_buffer
    e = ext_get(number)
    
    output_buffer += """
<div class="extension_edit">
<h4>Edit Extension %s - %s</h4>
""" % (number, e['name'])
    if len(e['numbers']):
        output_buffer += """
  <table>
    <tr>
      <th>Number</th>
      <th></th>
    </tr>
"""
        for n in sorted(e['numbers']):
            output_buffer += """
    <tr>
      <td>%s</td>
      <td><a href="?edit=%s&edel=%s">Del</a></td>
    </tr>
""" % (n, number, n)
        output_buffer += """
  </table>"""

    else:
        output_buffer += "No numbers, add one<br/>"
    output_buffer += """
<br/>
<form method=POST>
<input type="hidden" name="edit" value="%s" />
Number <input type="text" name="eadd" />
<input type="submit" value="Add" />
</form>
</div>
""" % (number)

def ext_del(number, delete):
    global extension_dir
    edir = open("%s/%s" % (extension_dir, number), 'r')

    fcontents = edir.readlines()

    edir.close()

    edir = open("%s/%s" % (extension_dir, number), 'w')
    for l in fcontents:
        if l.strip() != delete:
            edir.write(l)
    return True
    

    
def ext_get(number=None):
    """Lists if number is None"""
    global extension_dir

    extensions = []
    if number is None:
        for f in os.listdir(extension_dir):
            if f.isdigit() is True:
                extensions.append(ext_get(f))
        return extensions
        
    try:
        edir = open("%s/%s" % (extension_dir, number), 'r')
    except Exception, e:
        html_error('Unable to open %s/%s: %s' % (extension_dir, number, e))

    name = edir.readline()
    numbers = [x.replace("\n", "") for x in edir.readlines()]

    return { 'number': number, 'name': name, 'numbers': numbers }

def html_ext_add():
    global output_buffer
    output_buffer += """
<div class="extension_add">
<h4>Add Extension</h4>
<form method=POST>
<input type="hidden" name="add" value="1" />
<span class="formtitle">Number</span> <input type="text" name="number" /><br/>
<span class="formtitle">Name</span> <input type="text" name="name" /><br/>
<input type="submit" value="Save" />
</form>
</div>
"""

def html_ext_list(exts):
    global output_buffer
    output_buffer += """
    <span class="button greenbg"><a href="?add=1">Add Extension</a></span>
<div class="extension_list">
<h4>Extension List</h4>
"""
    if len(exts):
        output_buffer += """
<table>
  <tr>
    <th>Number</th>
    <th>Name</th>
    <th></th>
  </tr>
"""
        for e in exts:
            output_buffer += """
  <tr>
    <td><a href="?edit=%s">%s</a></td>
    <td><a href="?edit=%s">%s</a></td>
    <td><a href="?edit=%s">Edit</a></td>
  </tr>
""" % (e['number'], e['number'], e['number'], e['name'], e['number'])

        output_buffer += """
</table>
"""
    else:
        output_buffer += "No extensions configured"

    output_buffer += "</div>"

def html_header(title):
    global output_buffer
    output_buffer += """Content-Type: text/html

<html>
  <head>
    <title>OK Auto-Conference - %s</title>
    <link rel="stylesheet" type="text/css" href="/okautoconf.css" />

  </head>
  <body>
    <div class="content">
    <div class="header">
        <h2><a href="?1">OK Auto-Conference</a></h2>
    </div>
    
""" % (title)


def html_footer():
    global output_buffer
    output_buffer += """
    </div>
  </body>
</html>
"""

def html_error(err):
    global output_buffer
    output_buffer = ''
    html_header('Error')
    output_buffer += """<span class="error">%s</span>""" % (err)
    html_footer()
    html_send()
    sys.exit(0)

if __name__ == "__main__":
    main()


# vim: ts=4 sts=4 expandtab
