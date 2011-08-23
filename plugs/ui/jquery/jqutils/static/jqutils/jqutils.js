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
                this.set(k, v);
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
}

/* process rselect input */
$(function() {
    $('input.rselect').each(function(){
        $(this).rselect();
    });
});
