function model(options){
    /*options = {'header':'Test', 'message':'Hello', 
        'btnClass':'success',
        'footer':''}
    */
    $('.model').remove();
    var settings = $.extend({'btnClass':'success'}, options);
    var txt = ['<div class="modal hide fade">'];
    if (settings.header){
        txt.push('<div class="modal-header">'
            + '<a class="close" data-dismiss="modal">×</a>'
            + '<h3>' + settings.header + '</h3>'
            + '</div>');
    }
    txt.push('<div class="modal-body">'
        + settings.message 
        + '</div>');
    if (settings.footer){
        txt.push(settings.footer);
    }else{
        txt.push('<div class="modal-footer">'
            + '<a href="#" class="btn btn-warning" data-dismiss="modal">关闭</a>'
            + '</div>');
    }
    var el = $(txt.join(''));
    $('body').append(el);
    el.modal('show');
}
