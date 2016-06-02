
def get_principals(userid, request):
    if userid == 'admin':
        return ['group:admin']
    return []
