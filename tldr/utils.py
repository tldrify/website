import re, chardet

RE_BASE_HREF = re.compile('<base[^>]*href=[^>]*>', re.I)
RE_HEAD_START = re.compile('(<head(?:\s+[^>]*)?>)', re.I)
RE_HEAD_END = re.compile('(</head\s*>)', re.I)
RE_BODY_END = re.compile('(.*)(</body\s*>)', re.I | re.S)
RE_HTML_END = re.compile('(.*)(</html\s*>)', re.I | re.S)
RE_CHARSET = re.compile('<meta.*charset=["\']?([\w\-]+)["\']?', re.I)
RE_REDIRECT1 = re.compile('(\.location(?:\.href)?)\s*=')
RE_REDIRECT2 = re.compile('(\.location\.(?:replace|assign))\(')


def decode_response(response):
    detect = False
    meta_encoding = None
    try:
        html = response.content.decode(response.encoding)
        encoding = response.encoding
        meta_encoding = detect_charset(html)
        # Check that encoding specified in HTML matches the detected one:
        if meta_encoding and encoding != meta_encoding:
            detect = True
    except:
        detect = True

    if detect:
        response.encoding = None
        html = response.text
        encoding = response.apparent_encoding

    return (html, encoding, meta_encoding)


def detect_charset(html):
    m = RE_CHARSET.search(html)
    return m.group(1) if m else None


def fix_base_url(html, base_url):
    if not RE_BASE_HREF.match(html):
        html = RE_HEAD_START.sub('\\1\n<base href="%s" />' % base_url, html, 1)
    return html


def disable_redirects(html):
    html = RE_REDIRECT1.sub('\\1!=', html)
    html = RE_REDIRECT2.sub('\\1!=(', html)
    return html


def inject_scripts(html, citation):
    html = disable_redirects(html)
    head_start_inject = '''
\\1
<script type="text/javascript">
(function(open){
 XMLHttpRequest.prototype.open = function(method,url,async,user,pass){
  var a = document.createElement('a'); a.href = url;
  if(a.href.indexOf('/tldrify.com/')!==-1||a.href.indexOf('http')!==0){
   open.call(this,method,url,async,user,pass);
  }else if(a.href.length>0){
   open.call(this,method,'//tldrify.com/ajaxproxy?url='+encodeURIComponent(a.href),async,user,pass);
  }
 };
})(XMLHttpRequest.prototype.open);
</script>
'''
    html = RE_HEAD_START.sub(head_start_inject, html, 1)

    head_end_inject = '''
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
\\1
'''
    html = RE_HEAD_END.sub(head_end_inject, html, 1)

    body_inject = '''
\\1
<script src="//tldrify.com/static/js/ajaxslt.min.js?v20140205-1504" type="text/javascript"></script>
<script src="//cdn.jsdelivr.net/g/rangy@1.2.3(rangy-core.js),jquery@2.1.4(jquery.min.js)" type="text/javascript"></script>
<script src="//tldrify.com/static/js/tldr.min.js?v20150427-1637" type="text/javascript"></script>
<script type="text/javascript">
(function($){
 var retries = 15;
 function restore() { TLDR.restore('%s', window.location.protocol + '//tldrify.com/%s', %d, %s, false, retries==1); }
 $(window).load(restore);
 function checkpost() {
  if ($("span[class*=tldr-span]").length == 0 && retries-- > 0) {
   restore();
   setTimeout(checkpost, 1000);
  }
 }
 setTimeout(checkpost, 1000);
})($TLDR);
</script>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-23508932-7', 'auto');
  ga('send', 'pageview');
</script>
\\2
	''' % (citation.url, citation.short_id(), citation.id,
        citation.data.replace('\\n', '\\\\n'))

    l = len(html)
    html = RE_BODY_END.sub(body_inject, html, 1)
    if l == len(html):
        html = RE_HTML_END.sub(body_inject, html, 1)

    return html
