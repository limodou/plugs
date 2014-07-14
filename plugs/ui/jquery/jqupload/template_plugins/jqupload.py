def call():
    a = []
    a.append('jqupload/jquery.iframe-transport.js')
    a.append('jqupload/jquery.fileupload.js')
    return {'toplinks':a, 'depends':[('jquery', {'ui':True})]}
