from uliweb.utils.sorteddict import SortedDict
from copy import deepcopy

__menus__ = SortedDict()

def load_menu(menus):
    """
    Load menu definitions
    """
    global __menus__

    __menus__.clear()
    _m = []
    
    def _iter_menus(m, parent=''):
        """
        make menu tree to plat list
        """
        for i in m:
            _p = i.get('parent') or parent
            _m.append((_p, i.get('order', 900), i))
            name = i['name']
            subs = i.get('subs', [])
            _iter_menus(subs, name)
            i['subs'] = []
    
    def _f(menus):
        for name, item in menus:
            x = deepcopy(item)
            x['name'] = name
            yield x
    
    _iter_menus(_f(menus))
    
    _m.sort()
    
    #rebuild menu tree
    stack = [('', None)]
    while len(stack) > 0:
        parent, pitem = stack.pop(0)
        i = 0
        find = False
        while i<len(_m):
            _p, _, mitem = _m[i]
            is_path = '/' in _p
            if _p == parent or (is_path and pitem and pitem.get('id')==_p):
                name = mitem['name']
                if not parent:
                    __menus__[name] = mitem
                    _id = name
                else:
                    pitem['subs'].append(mitem)
                    _id = _p + '/' + name
                mitem['id'] = _id
                stack.append((name, mitem))
                find = True
                _m.pop(i)
            else:
                if find:
                    break
                i += 1
    return __menus__

def get_menu(name):
    global __menus__

    assert name
    
    path = name.split('/')
    items = __menus__[path[0]]
    if len(path) > 1:
        _items = items
        find = False
        for p in path[1:]:
            for x in _items.get('subs', []):
                if p == x.get('name'):
                    _items = x
                    find = True
                    break
        if find:
            items = _items
        else:
            raise KeyError("Can't find menu item %s" % name)
        
    return items
    
def print_menu(root=None, title=False):
    global __menus__
    
    items = __menus__
    if root:
        items = get_menu(root)
    
    def p(menus, tab=0):
        print ' '*tab + menus['name'],
        if title:
            print '[' + menus.get('title', menus['name']) + ']'
        else:
            print
        for x in menus.get('subs', []):
            p(x, tab+4)
       
    if not root:
        for x in items.values():
            p(x)
    else:
        p(items)
            
def after_init_apps(sender):
    from uliweb import settings
    
    load_menu(settings.MENUS.items())
    
def default_validators(item, context):
    """
    Check role and permission
    role and permission check result will be cached in context dict
    """
    from uliweb import functions, request
    
    roles = item.get('roles', [])
    perms = item.get('permissions', [])
    if roles or perms:
        if roles:
            con_roles = context.setdefault('roles', {})
            for x in roles:
                if x in con_roles:
                    flag = con_roles[x]
                else:
                    flag = functions.has_role(request.user, x)
                    con_roles[x] = flag
                if flag:
                    return flag
            
        if perms:
            con_perms = context.setdefault('permissions', {})
            for x in perms:
                if x in con_perms:
                    flag = con_perms[x]
                else:
                    flag = functions.has_permission(request.user, x)
                    con_perms[x] = flag
            if flag:
                return flag
    else:
        return True
    
def _validate(menu, context, validators=None):
    from uliweb.utils.common import import_attr
    
    #validate permission
    validators = validators or []
    
    check = menu.get('check')
    if check and not isinstance(check, (list, tuple)):
        check = [check]
    else:
        check = []
    
    validators = validators + check
    
    if validators:
        flag = False
        for v in validators:
            if not v: continue
            if isinstance(v, (str, unicode)):
                func = import_attr(v)
            else:
                func = v
            flag = func(menu, context)
            if flag:
                flag = True
                break
    else:
        flag = True
        
    return flag
    
def navigation(name, active='', check=None, id=None, _class=None):
    from uliweb import settings
    
    if check and not isinstance(check, (list, tuple)):
        check = [check]
    else:
        check = []
    validators = (settings.MENUS_CONFIG.validators or []) + list(check)
    
    return _navigation(name=name, active=active, validators=validators, id=id, _class=_class)
    
def _navigation(name, active='', validators=None, id=None, _class=None):
    s = []
    items = get_menu(name)
    context = {}
    
    _id = (' id="%s"' % id) if id else ''
    _cls = (' %s' % _class) if _class else ''
    s.append('<ul class="nav%s"%s>\n' % (_cls, _id))
    for j in items.get('subs', []):
        flag = _validate(j, context, validators)
        if not flag:
            continue
        
        href = j.get('link', '#')
        title = j.get('title', j['name'])
        if j['name'] == active:
            s.append('<li class="active"><a href="%s"><span>%s</span></a></li>\n' % (href, title))
        else:
            s.append('<li><a href="%s"><span>%s</span></a></li>\n' % (href, title))
    s.append('</ul>\n')
    
    return ''.join(s)
    
def menu(name, active='', check=None, id=None, _class=None):
    from uliweb import settings

    if check and not isinstance(check, (list, tuple)):
        check = [check]
    else:
        check = []
    validators = (settings.MENUS_CONFIG.validators or []) + list(check)
    
    return _menu(name=name, active=active, validators=validators, id=id, _class=_class)

def _menu(name, active='', validators=None, id=None, _class=None):
    """
    :param menu: menu item name
    :param active: something like "x/y/z"
    :param check: validate callback, basic validate is defined in settings
    """
    validators = validators or []

    x = active.split('/')
    items = get_menu(name)
    s = []
    context = {}
    
    def p(menus, index=0, tab=2):
        flag = _validate(menus, context, validators)
            
        if not flag:
            return ''
            
        if index < len(x):
            _name = x[index]
        else:
            _name = ''
        c = ' class="active"' if _name and _name==menus['name'] and index==len(x)-1 else ''
        href = menus.get('link', '#')
        title = menus.get('title', menus['name'])
        s.append('%s<li%s><a href="%s">%s</a>' % (' '*tab, c, href, title))
        
        #process sub menus
        subs = menus.get('subs', [])
        if subs:
            s.append('\n')
            s.append('%s<ul>\n' % (' '*tab))
            for i in subs:
                p(i, index+1, tab+2)
            s.append('%s</ul>\n' % (' '*tab))
            s.append('%s</li>\n' % (' '*tab))
        else:
            s.append('</li>\n')
    
    _id = (' id="%s"' % id) if id else ''
    _cls = (' %s' % _class) if _class else ''
    s.append('<ul class="menu%s"%s>\n' % (_cls, _id))
    for j in items.get('subs', []):
        p(j, tab=2)
    s.append('</ul>\n')
    
    return ''.join(s)