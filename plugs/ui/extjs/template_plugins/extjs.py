def call(app, var, env, adapter=None, all=False, debug=False, lang=None):
    a = []
    a.append('extjs/resources/css/ext-all.css')
    if not adapter:
        a.append('extjs/adapter/ext/ext-base.js')
        
    elif adapter == 'prototype':
#        a.append('extjs/adapter/prototype/prototype.js')
#        a.append('extjs/adapter/prototype/scriptaculous.js?load=effects.js')
        a.append('extjs/adapter/prototype/ext-prototype-adapter.js')
        
    elif adapter == 'jquery':
#        a.append('extjs/adapter/jquery/jquery.js')
        a.append('extjs/adapter/jquery/ext-jquery-adapter.js')
        
    elif adapter == 'yui':
#        a.append('extjs/adapter/yui/yui-utilities.js')
        a.append('extjs/adapter/yui/ext-yui-adapter.js')
        
    if all:
        a.append('extjs/ext-all.js')

    if debug:
        a.append('extjs/ext-all-debug.js')
        
    if lang:
        a.append('extjs/src/locale/ext-lang-%s.js' % lang)
        
    a.append('extjs/ext-init.js')
    return {'toplinks':a}
