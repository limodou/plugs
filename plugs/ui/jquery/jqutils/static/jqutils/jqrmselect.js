(function( $ ) {
    $.widget( "ui.remote_multiple_select", {
        _create: function() {
            var self = this,
                select = this.element.hide();
            //add buttons to select control
            var display = this.display = $('<div class="rmselect-widget"><div class="rmselect-tool"></div><div class="rmselect-body"></div></div>')
            display.insertAfter(select);
            var remove_all = this.remove_all = $(template('<input type="button" class="remove_all" value="${remove_all_txt}"></input>', this.options));
            var add = this.remove = $(template('<input type="button" class="add" value="${add_txt}"></input>', this.options));
            var rselect = self.rselect = $(template('<input type="text" name="username" class="rselect" url="${0}"></input>', [$(select).attr('url')]));
            $('.rmselect-tool', display).append(remove_all).append(add).append(rselect);
            rselect.rselect();
            
            if (this.options.width){
                display.width(this.options.width);
            }
            
            var h;
            if (this.options.height){
                h = this.options.height;
                display.height(h);
            }else
                h = display.height();
                
            display.find('.rmselect-tool').height(30);
            display.find('.rmselect-body').height(h-30).css({overflow:'auto'});
            
            var body = $('.rmselect-body', display);
            var ul = this.ul = $('<ul></ul>');
            body.append(ul);
            //process select options
            var se = select.get(0);
            for (var i=0; i<se.options.length; i++){
                var o = se.options[i];
                if (o.selected){
                    self._add_item(o.value, o.text);
                }
            }
            
            //binding events
            remove_all.click(function(){
                for(var i = se.options.length-1; i >= 0; i--){
                    self._remove_item(se.options[i].value);
                    se.remove(i);
                }
            });
            
            add.click(function(){
                var v = rselect.rselect('getValue');
                var txt = rselect.rselect('getText');
                var flag = false;
                if (v){
                    for(var i=0; i<se.options.length; i++){
                        if (se.options[i].value == v){
                            flag = true;
                            break;
                        }
                    }
                    if (!flag){
                        se.options.add(new Option(txt, v));
                        se.options[se.options.length-1].selected=true;
                        self._add_item(v, txt);
                    }
                    rselect.rselect('clear');
                }
            });
            
        },
        _add_item : function(value, text){
            var self = this;
            var item = $(template('<li rel="${value}"><span class="rm-blank"><img class="rm-delete" src="/static/images/cross_grey_small.png" /></span><span class="rm-text">${text}</span></li>', {'value':value, 'text':text}));
            this.ul.append(item);
            var img = $('img.rm-delete', item).hide();
            item.hover(
                function(e){
                    img.slideDown();
                },
                function(e){
                    img.slideUp();
                }
            ).click(function(){
                item.remove();
                var se = self.element.get(0);
                for(var i=0; i<se.options.length; i++){
                    if(se.options[i].value == value){
                        se.remove(i);
                    }
                }
            });
        },
        
        _remove_item: function(value){
            $('li[rel='+value+']', this.ul).remove();
        },
        
        options : {
            'remove_all_txt':'Remove All',
            'remove_txt':'Remove',
            'add_txt':'Add',
            'width':null,
            'height':200
        },
        destroy: function() {
            this.display.remove();
            this.element.show();
            $.Widget.prototype.destroy.call( this );
        }
    });
})( jQuery );
            
