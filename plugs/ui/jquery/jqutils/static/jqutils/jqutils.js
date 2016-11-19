/***************************
QueryString
****************************/
(function($){
    QueryString = function(url){
        this.urlParams = {};
        this.load(url);
    }
    QueryString.prototype = {
        load: function(param){
            this.urlParams = {}
            var e,k,v,i,
                a = /\+/g,  // Regex for replacing addition symbol with a space
                r = /([^&=]+)=?([^&]*)/g,
                d = function (s) { return decodeURIComponent(s.replace(a, " ")); }
            if(!param){
                param = window.location.search;
            }
            if (param.charAt(0) == '?'){
                param = param.substring(1);
            }else{
                i = param.indexOf('?');
                if (i>-1){
                    param = param.substring(i+1);
                }
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

var show_simple_message = function(msg, target, options){
    $('.simple_message').remove();
    if (!msg) {
        return;
    }
    var setting = $.extend({trigger:'auto', delay:5000}, options||{});
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
    }else{
        m.find('.mg').addClass('rounded');
        $(t).html(m);
    }
    if(setting.trigger == 'auto'){
        setTimeout('show_simple_message("")', setting.delay);
    }
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
        opt = opt || {};
        t.find('input').poshytip('hide');
        if (r.success){
            if(r.message) show_message(r.message);
            if (opt.success){
                opt.success(r.data);
            }
        } else if (!r.success){
            if(r.message) show_message(r.message, 'error');
            var error = r.errors || r.data
            if(error){
                $.each(error, function(key, value){
                    var el = t.find('input[name='+key+'],select[name='+key+'],textarea[name='+key+']');
                    if (el.is(':hidden')){
                        el = el.parent();
                    }
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
}

var create_ajax_callback = function(target, options){
    return function(r){
        var opts = {
            field_prefix:'div_field_'
            , message_type:'bootstrap'
        };
        if (typeof options === 'function'){
            opts.success = options;
        }else{
            opts = $.extend(opts, options);
        }
        if (r.success){
            if(r.message) show_message(r.message);
            if (opts.success){
                opts.success(r.data);
            }
        } else if (!r.success){
            if(r.message) show_message(r.message, 'error');
            var error = r.errors || r.data
            if(opts.message_type == 'bootstrap'){
                $('div.control-group').removeClass('error').find('.help-block.error').remove();
                if(error){
                    $.each(error, function(key, value){
                        var f, t;
                        f = '#' + opts.field_prefix + key;
                        t = $(f).addClass('error');
                        t.find('.controls').append('<p class="help-block error">'+value+'</p>');
                    });
                }
            }else if(opts.message_type == 'tip'){
                var t = $(target);
                $('body').on('dialog2.beforeClose', t, function(e){
                    t.find('input, select, textarea').poshytip('hide');
                });
                t.find('input, select, textarea').poshytip('hide');
                if(error){
                    $.each(error, function(key, value){
                        var el = t.find('input[name='+key+'],select[name='+key+'],textarea[name='+key+']');
                        if (el.is(':hidden')){
                            el = el.parent();
                        }
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
    }
}

/*! http://mths.be/placeholder v2.0.6 by @mathias */
;(function(window, document, $) {

	var isInputSupported = 'placeholder' in document.createElement('input'),
	    isTextareaSupported = 'placeholder' in document.createElement('textarea'),
	    prototype = $.fn,
	    valHooks = $.valHooks,
	    hooks,
	    placeholder;

	if (isInputSupported && isTextareaSupported) {

		placeholder = prototype.placeholder = function() {
			return this;
		};

		placeholder.input = placeholder.textarea = true;

	} else {

		placeholder = prototype.placeholder = function() {
			var $this = this;
			$this
				.filter((isInputSupported ? 'textarea' : ':input') + '[placeholder]')
				.not('.placeholder')
				.bind({
					'focus.placeholder': clearPlaceholder,
					'blur.placeholder': setPlaceholder
				})
				.data('placeholder-enabled', true)
				.trigger('blur.placeholder');
			return $this;
		};

		placeholder.input = isInputSupported;
		placeholder.textarea = isTextareaSupported;

		hooks = {
			'get': function(element) {
				var $element = $(element);
				return $element.data('placeholder-enabled') && $element.hasClass('placeholder') ? '' : element.value;
			},
			'set': function(element, value) {
				var $element = $(element);
				if (!$element.data('placeholder-enabled')) {
					return element.value = value;
				}
				if (value == '') {
					element.value = value;
					// Issue #56: Setting the placeholder causes problems if the element continues to have focus.
					if (element != document.activeElement) {
						// We can’t use `triggerHandler` here because of dummy text/password inputs :(
						setPlaceholder.call(element);
					}
				} else if ($element.hasClass('placeholder')) {
					clearPlaceholder.call(element, true, value) || (element.value = value);
				} else {
					element.value = value;
				}
				// `set` can not return `undefined`; see http://jsapi.info/jquery/1.7.1/val#L2363
				return $element;
			}
		};

		isInputSupported || (valHooks.input = hooks);
		isTextareaSupported || (valHooks.textarea = hooks);

		$(function() {
			// Look for forms
			$(document).delegate('form', 'submit.placeholder', function() {
				// Clear the placeholder values so they don’t get submitted
				var $inputs = $('.placeholder', this).each(clearPlaceholder);
				setTimeout(function() {
					$inputs.each(setPlaceholder);
				}, 10);
			});
		});

		// Clear placeholder values upon page reload
		$(window).bind('beforeunload.placeholder', function() {
			$('.placeholder').each(function() {
				this.value = '';
			});
		});

	}

	function args(elem) {
		// Return an object of element attributes
		var newAttrs = {},
		    rinlinejQuery = /^jQuery\d+$/;
		$.each(elem.attributes, function(i, attr) {
			if (attr.specified && !rinlinejQuery.test(attr.name)) {
				newAttrs[attr.name] = attr.value;
			}
		});
		return newAttrs;
	}

	function clearPlaceholder(event, value) {
		var input = this,
		    $input = $(input),
		    hadFocus;
		if (input.value == $input.attr('placeholder') && $input.hasClass('placeholder')) {
			hadFocus = input == document.activeElement;
			if ($input.data('placeholder-password')) {
				$input = $input.hide().next().show().attr('id', $input.removeAttr('id').data('placeholder-id'));
				// If `clearPlaceholder` was called from `$.valHooks.input.set`
				if (event === true) {
					return $input[0].value = value;
				}
				$input.focus();
			} else {
				input.value = '';
				$input.removeClass('placeholder');
			}
			hadFocus && input.select();
		}
	}

	function setPlaceholder() {
		var $replacement,
		    input = this,
		    $input = $(input),
		    $origInput = $input,
		    id = this.id;
		if (input.value == '') {
			if (input.type == 'password') {
				if (!$input.data('placeholder-textinput')) {
					try {
						$replacement = $input.clone().attr({ 'type': 'text' });
					} catch(e) {
						$replacement = $('<input>').attr($.extend(args(this), { 'type': 'text' }));
					}
					$replacement
						.removeAttr('name')
						.data({
							'placeholder-password': true,
							'placeholder-id': id
						})
						.bind('focus.placeholder', clearPlaceholder);
					$input
						.data({
							'placeholder-textinput': $replacement,
							'placeholder-id': id
						})
						.before($replacement);
				}
				$input = $input.removeAttr('id').hide().prev().attr('id', id).show();
				// Note: `$input[0] != input` now!
			}
			$input.addClass('placeholder');
			$input[0].value = $input.attr('placeholder');
		} else {
			$input.removeClass('placeholder');
		}
	}

}(this, document, jQuery));

$(function(){
    $('input, textarea').placeholder();
});

$.fn.serializeObject = function() {
    var o = {};
//    var a = this.serializeArray();
    $(this).find('input[type="hidden"], input[type="text"], input[type="password"], input[type="checkbox"]:checked, input[type="radio"]:checked, select').each(function() {
        if ($(this).attr('type') == 'hidden') { //if checkbox is checked do not take the hidden field
            var $parent = $(this).parent();
            var $chb = $parent.find('input[type="checkbox"][name="' + this.name.replace(/\[/g, '\[').replace(/\]/g, '\]') + '"]');
            if ($chb != null) {
                if ($chb.prop('checked')) return;
            }
        }
        if (this.name === null || this.name === undefined || this.name === '') return;
        var elemValue = null;
        if ($(this).is('select')) elemValue = $(this).find('option:selected').val();
        else elemValue = this.value;
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(elemValue || '');
        } else {
            o[this.name] = elemValue || '';
        }
    });
    return o;
}

/* ajaxSetup */
$.ajaxSetup({cache:false, traditional:true});