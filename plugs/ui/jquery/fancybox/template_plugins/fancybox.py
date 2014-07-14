def call():
    a = []
    a.append('fancybox/jquery.fancybox.css')
    a.append('fancybox/jquery.fancybox.min.js')
    return {'toplinks':a, 'depends':['jquery']}
