def device(request):
    '''from mobile browser or pc browser'''
    user_agent = request.META['HTTP_USER_AGENT'].lower()
    mobile_re = ['iphone','android','mobile']

    is_mobile = False
    for keyword in mobile_re:
        if user_agent.find(keyword) >= 0:
            is_mobile = True
            break

    if is_mobile:
        return {'device_type': 'mobile'}
    else:
        return {'device_type': 'pc'}
