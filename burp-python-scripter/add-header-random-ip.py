def generate_random_ip():
    import random
    n1 = str(random.randint(0,256))
    n2 = str(random.randint(0,256))
    n3 = str(random.randint(0,256))
    n4 = str(random.randint(0,256))
    random_ip = "%s.%s.%s.%s" % (n1,n2,n3,n4)
    #print random_ip
    return random_ip

if messageIsRequest:
    #if toolFlag in (callbacks.TOOL_PROXY,):
    if toolFlag not in (callbacks.TOOL_EXTENDER,):
        #if callbacks.isInScope(messageInfo.getUrl()):
        requestInfo = helpers.analyzeRequest(messageInfo.getRequest())
        headers = requestInfo.getHeaders()
        requestBody = messageInfo.getRequest()[requestInfo.getBodyOffset():]
        headers.add('X-Forwarded-For: %s' % generate_random_ip())
        headers.add('X-Originating-IP: %s' % generate_random_ip())
        headers.add('X-Remote-IP: %s' % generate_random_ip())
        headers.add('X-Remote-Addr: %s' % generate_random_ip())
        headers.add('X-Client-IP: %s' % generate_random_ip())
        request = helpers.buildHttpMessage(headers, requestBody)
        messageInfo.setRequest(request)
