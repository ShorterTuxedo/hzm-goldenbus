import string

def set_list(l, i, v):
      try:
          l[i] = v
      except IndexError:
          for _ in range(i-len(l)+1):
              l.append(None)
          l[i] = v

def int2base(x, base):
    digs = string.digits + string.ascii_letters
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

def getAcwScV2(arg1):
    _0x5e8b26 = '3000176000856006061501533003690027800375'
    def hexXor(string, _0x4e08d8):
        _0x5a5d3b = '';
        _0xe89588 = 0x0
        # _0xe89588 < len(string) && _0xe89588 < _0x4e08d8['length']
        while (_0xe89588 < len(string) and _0xe89588 < len(_0x4e08d8)):
            _0x401af1 = int(string[_0xe89588: _0xe89588 + 0x2], 0x10)
            _0x105f59 = int(_0x4e08d8[_0xe89588: _0xe89588 + 0x2], 0x10)
            _0x189e2c = int2base((_0x401af1 ^ _0x105f59), 0x10)
            if (len(_0x189e2c) == 0x1):
                _0x189e2c = '0' + _0x189e2c
            
            _0x5a5d3b += _0x189e2c
            _0xe89588 += 0x2
        
        return _0x5a5d3b
    
    def unsbox(string):
        _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24]
        _0x4da0dc = []
        _0x12605e = ''
        _0x20a7bf = 0x0
        while (_0x20a7bf < len(string)):
            _0x385ee3 = string[_0x20a7bf]
            # print(_0x385ee3)
            _0x217721 = 0x0
            while (_0x217721 < len(_0x4b082b)):
                if (_0x4b082b[_0x217721] == _0x20a7bf + 0x1):
                    # print(_0x385ee3)
                    set_list(_0x4da0dc, _0x217721, _0x385ee3)
                _0x217721 += 1
            _0x20a7bf += 1
                
            
        # print(_0x4da0dc)
        _0x12605e = ''.join(_0x4da0dc)
        # print(_0x12605e)
        return _0x12605e
    
    _0x23a392 = unsbox(arg1)
    # print(_0x23a392)
    arg2 = hexXor(_0x23a392, _0x5e8b26)
    # print(arg2)
    return arg2

def getArg1FromHTML(html):
    return html.split("arg1='")[1].split("'")[0]