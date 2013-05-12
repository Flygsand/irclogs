from irclogs.utils import platform

def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):

    if isinstance(s, platform.text_type):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, platform.string_types):
            if hasattr(s, '__unicode__'):
                s = s.__unicode__()
            else:
                if platform.PY3:
                    if isinstance(s, bytes):
                        s = platform.text_type(s, encoding, errors)
                    else:
                        s = platform.text_type(s)
                else:
                    s = platform.text_type(bytes(s), encoding, errors)
        else:
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise UnicodeDecodeError(s, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join([force_text(arg, encoding, strings_only,
                    errors) for arg in s])
    return s

def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):

    if isinstance(s, platform.memoryview):
        s = bytes(s)
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and (s is None or isinstance(s, int)):
        return s
    if not isinstance(s, platform.string_types):
        try:
            if platform.PY3:
                return six.text_type(s).encode(encoding)
            else:
                return bytes(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return b' '.join([force_bytes(arg, encoding, strings_only,
                        errors) for arg in s])
            return platform.text_type(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)