def call(app, var, env):
    a = []
    a.append('facebox/facebox.css')
    a.append('facebox/facebox.js')
    a.append('''<![if lt IE 9]>
<style type="text/css">
#facebox_overlay {
  left: expression( ( ( ignoreMe2 = document.documentElement.scrollLeft ? document.documentElement.scrollLeft : document.body.scrollLeft ) ) + 'px' );
  top: expression( ( ( ignoreMe = document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop ) ) + 'px' );
}
</style>
<![endif]>''')

    return {'toplinks':a}
