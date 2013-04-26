import errno

def error_to_status(err):

    try:
        raise err
    except IOError, e:

        if e.errno == errno.EACCES:
            return '403 Access Denied'
        elif e.errno == errno.ENOENT or \
              e.errno == errno.EISDIR or \
              e.errno == errno.ENOTDIR:
            return '404 Not Found'
        else:
            return '500 Internal Server Error'

    except:

        return '500 Internal Server Error'