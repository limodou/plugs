/***************************
QueryString
****************************/
(function($){
    QueryString = function(options){
        this.urlParams = {};
        this.load();
    }
    QueryString.prototype = {
        load: function(param){
            this.urlParams = {}
            var e,k,v,
                a = /\+/g,  // Regex for replacing addition symbol with a space
                r = /([^&=]+)=?([^&]*)/g,
                d = function (s) { return decodeURIComponent(s.replace(a, " ")); }
            if(!param){
                param = window.location.search;
            }
            if (param.charAt(0) == '?'){
                param = param.substring(1);
            }
            while (e = r.exec(param)){
                k = d(e[1]);
                v = d(e[2]);
                this.set(k, v, false);
            }
            return this;
        },
        toString:function(options){
            var settings = {
                'hash' : false,
                'traditional' : true
            };
            if ( options ) { 
              $.extend( settings, options );
            }
            var old = jQuery.ajaxSettings.traditional;
            jQuery.ajaxSettings.traditional = settings.traditional;
            var result = '?' + $.param(this.urlParams);
            jQuery.ajaxSettings.traditional = old;
            if (settings.hash)
                result = result + window.location.hash;
            return result;
        },
        set:function(k, v, replace){
            replace = replace || false;
            if (replace)
                this.urlParams[k] = v;
            else{
                if (k in this.urlParams){
                    if ($.type(this.urlParams[k]) === 'array'){
                        this.urlParams[k].push(v);
                    }
                    else{
                        if (this.urlParams[k] == '')
                            this.urlParams[k] = v;
                        else
                            this.urlParams[k] = [this.urlParams[k], v];
                    }
                }
                else
                    this.urlParams[k] = v;
            }
            return this;
        },
        get:function(k){
            return this.urlParams[k];
        },
        remove:function(k){
            if (k in this.urlParams){
                delete this.urlParams[k];
            }
            return this;
        }
    }
    $.query_string = new QueryString();
})(jQuery);

(function($){
    $(function(){
        jQuery('<iframe src="" style="display:none" id="ajaxiframedownload"></iframe>')
        .appendTo('body');
    });
    $.download = function(url){
    	//url and data options required
    	if(url){ 
    		//send request
            var el = $('#ajaxiframedownload');
            el.attr('src', url);
    	};
    };
})(jQuery);

$(function(){
    $('div.box-panel').each(function(){
        var el = $(this);
        var e = $('<span class="ui-icon ui-icon-triangle-1-s left" style="margin:8px 2px 0 2px;"></span>');
        var h2 = el.children('h2');
        h2.css('cursor', 'pointer');
        h2.attr('title', 'Click here to show/hide content')
        h2.click(function(){
            var body = el.children('div.box-body');
            body.slideToggle('normal', function(){
                if ($(this).is(':visible')){
                    e.removeClass('ui-icon-triangle-1-e')
                    .addClass('ui-icon-triangle-1-s');
                }else{
                    e.removeClass('ui-icon-triangle-1-s')
                    .addClass('ui-icon-triangle-1-e');
                }
            });
        });
        e.prependTo(el);
    });
});

/* datepicker process */
$(function() {
    $('input.field_date').datepicker({ dateFormat: 'yy-mm-dd' });
});

/* fix table process */
$(function() {
    $('table.fix-table').each(function(){
        var w = $(this).parent('div').width();
        $(this).width(w).css({'table-layout':'fixed', 'word-wrap':'break-all'});
    });
});

var template = function(tmp_string, hash_or_array){
    function _replace(m, word){
        var r;
        if (Boolean(word.match(/^[0-9]+$/)) && hash_or_array.constructor == Array)
            r = hash_or_array[parseInt(word)];
        else
            r = hash_or_array[word];
        if(r == undefined)  return '';
        else return r;
    }
    return $(tmp_string.replace(/\$\{?([A-Za-z_0-9]+)\}?/g, _replace));
};

/* process rselect input */
$(function() {
    $('input.rselect').each(function(){
        $(this).rselect();
    });
});

/* mytabs */
(function( $ ) {
    $.widget( "ui.mytabs", {
        _id : 1,
        options: {'container':'', 'current':0, 'ajax':true},
        _create: function() {
            var self = this, element = this.element;
            $(element).find('a.tabitem').each(function(){
                $($(this).attr('rel')).hide();
            });
            $(element).find('a.tabitem').click(function(e){
                if (!self.options.ajax && !$(this).attr('rel')) 
                    return true;
                e.preventDefault();
                self.show(this);
            });
            self.show(self.options.current);
        },
        show: function(index){
            var el;
            if (typeof index == 'number') el = $(this.element).find('a.tabitem:eq('+index+')');
            else if (typeof index == 'string') el = $(this.element).find('#'+index);
            else el = $(index);
            //if current item has class="current" then do nothing
            if (el.hasClass('current')) return;
            this._load(el);
            var cur = $(this.element).find('a.current');
            cur.removeClass('current');
            $(cur.attr('rel')).hide();
            el.addClass('current');
            $(el.attr('rel')).show();
        },
        _load: function(a){
            var self=this;
            //if it has rel attribute, then it means the content is loaded
            if(a.attr('rel')) return;
            var target = $(self.options.container);
            if(a.hasClass('iframe')){
                var id = '_mytabs_'+self._id;
                self._id ++;
                var div = $('<div id="'+id+'"></div>').appendTo(target);
                var w = a.attr('fw') || target.width();
                var h = a.attr('fh') || target.height();
                div.html('<iframe src="'+a.attr('href')+'" width="'+w+'" height="'+h+'"></iframe>');
                a.attr('rel', '#'+id);
            }else{
//            target.spin();
            //then it means that the content should be loaded by ajax
                $.ajax({
                    type: "POST",
                    url: a.attr('href'),
                    success: function(data){
                        var id = '_mytabs_'+self._id;
                        self._id ++;
                        var div = $('<div id="'+id+'"></div>').appendTo(target);
                        div.html(data);
                        a.attr('rel', '#'+id);
    //                    target.spin(false);
                    }
                });
            }
        },
        destroy: function() {
            $(self).find('a.tabitem').show();
            $.Widget.prototype.destroy.call( this );
        }
    });
})( jQuery );

/* spin plugin */
$.fn.spin = function(opts) {
  this.each(function() {
    var $this = $(this),
        data = $this.data();

    if (data.spinner) {
      data.spinner.stop();
      delete data.spinner;
    }
    if (opts !== false) {
      data.spinner = new Spinner(opts).spin(this);
    }
  });
  return this;
};

$.fn.hover_menu = function(){
    $(this).find('.items').hide();
    $(this).each(function(){
        $(this).hoverIntent({
            sensitivity: 1, // number = sensitivity threshold (must be 1 or higher)
            interval: 50,   // number = milliseconds for onMouseOver polling interval
            over: function(){
                var menu = $(this);
                var t = menu.find('cite');
                var offset = t.offset();
                menu.find(".items").css({top:offset.top+t.outerHeight(), left:offset.left, margin:0}).slideDown();
                t.addClass('hover');
            },     // function = onMouseOver callback (required)
            timeout: 300,   // number = milliseconds delay before onMouseOut
            out: function(){ 
                var menu = $(this);
                menu.find(".items").slideUp();
                menu.find("cite").removeClass('hover');
            } // function = onMouseOut callback (required)
         });
    });
};

var show_simple_message = function(msg, target){
    if (!msg) {
        $('.simple_message').remove();
        return;
    }
    var t = target || '.message-conainter';
    var m = $('<div class="simple_message"><div class="mg">' + msg + '</div></div>');
    if ($(t).size()==0){
        m.css({
            position:'fixed',
            top:0, 
            left:$(window).width() / 2 - (m.outerWidth() / 2),
            zIndex: 21000
        });
        m.find('.mg').addClass('rounded_bottom');
        $('body').append(m);
    }else
        m.find('.mg').addClass('rounded');
        $(t).html(m);
};

/*
  get select options from url
  server shoud return data just like this:

    [[value1, text1], [value2, text2], ...]
    
  or 

    [{value:'value1', text:'text1'}, {value:'value2', text:'text2'}...]
*/
function get_select(target, url, data){
    $.ajax({
        type: 'POST',
        url: url,
        data: data || {},
        dataType: 'json',
        success: function(data){
            var html = "<option value=''></option>";
            var v,k,t;
            $.each(data, function(j, value){
                if($.type(value) == 'array'){
                    v = value[0];
                    k = value[1];
                }else{
                    v = value.value;
                    k = value.text;
                }
                html = html + '<option value=' + v + '>' + k + '</option>'
            });
            if (typeof target == 'string') t = $('select[name='+target+']');
            else t = $(target);
            t.html(html);
        }
    });
};
/*
    bind change event to an element, and when the element value is changed
    then automatically fetch data from remote, and change the target select 
    element
*/
$.fn.bind_select_remote = function(target, url){
    return $(this).each(function(){
        $(this).change(function(){
            get_select(target, url, {value:t.val()});
        });
    });
};

/*
    ajax Form callback process
    for example:
    
    var result_process = create_result_process('form.yform', 
        {success:success});
    
    var options = { 
        success: result_process,  // post-submit callback 
        dataType: 'json'
    }; 
    // bind form using 'ajaxForm' 
    $('form.yform').ajaxForm(options); 
    
    response json data should be:
    
    {'success':true or false, 'message': 'xxx', 'data': {}}
    if success if false, then data should be {'field_name':'error_msg'}
    
*/
var create_result_process = function(target, opt){
    return function(r){
        var t = $(target);
        t.find('input').poshytip('hide');
        show_simple_message(r.message);
        if (r.success){
            opt.success(r.data);
        } else if (!r.success){
            $.each(r.data, function(key, value){
                var el = t.find('input[name='+key+'],select[name='+key+'],textarea[name='+key+']');
                $(el).poshytip({
                    className: 'tip-yellowsimple',
                    content: value,
                    showOn: 'none',
                    alignTo: 'target',
                    alignX: 'inner-left',
                    offsetX: 0,
                    offsetY: 5,
                    closeButton: true
                });
                $(el).poshytip('show');
                $(el).focus(function(){
                    $(this).poshytip('hide');
                });
            });
        }
    }
}

/* ajaxSetup */
$.ajaxSetup({cache:false});