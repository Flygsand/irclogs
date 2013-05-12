import errno

def error_to_status(e):

    status = None

    if isinstance(e, IOError):
        if e.errno == errno.EACCES:
            return '403 Access Denied'
        elif e.errno == errno.ENOENT or \
              e.errno == errno.EISDIR or \
              e.errno == errno.ENOTDIR:
            return '404 Not Found'
    
    if not status:
        status = '500 Internal Server Error'

    return status