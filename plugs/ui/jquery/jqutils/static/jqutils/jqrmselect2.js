(function( $ ) {
    $.widget( "ui.remote_multiple_select2", {
        _create: function() {
            var self = this,
                select = this.element.hide();
            self.select = select;
            //add buttons to select control
            var display = this.display = $('<div class="rmselect-widget2"><div class="rmselect-tool"></div><div class="rmselect-body"></div></div>')
            display.insertAfter(select);
            var remove_all = this.remove_all = $(template('<input type="button" class="remove_all" value="${remove_all_txt}"></input>', this.options));
            var input = self.rselect = $('<input type="text" name="username"></input>');
            self.input = input;
            $('.rmselect-tool', display).append('<span>'+this.options.label+'</span>').append(input).append(remove_all);
            
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
            
            var body = this.container = $('.rmselect-body', display);
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
            
            var url;
            if (!this.options.url){
                url = select.attr('url');
            }else{
                url = this.options.url;
            }
            
            function fetch_data( request, response ) {
                $.ajax({
                    url: url,
                    dataType: "json",
                    data: {
                        term: request.term
                    },
                    success: function( data ) {
                        if (data.length == 0){
                            self.element.val('');
                            self.input.val('');
                            response([]);
                        }
                        else{
                            d = $.map(data, function(x){
                                if ($.type(x) == 'array')
                                    return {'id':x[0], 'title':x[1]};
                                else
                                    return x;
                            });
                            response(d);
                        }
                    }
                });
            }
            
            input.autocomplete({
                delay: 5,
                minLength: self.options.minLength,
                source: fetch_data,
                select: function( event, ui ) {
                    self.add_item(ui.item.id, ui.item.title);
                    input.val('');
                    if (self.options.onSelect){
                        self.options.onSelect.call(self);
                    }
                    return false;
                }
            });
            input.data( "autocomplete" )._renderItem = function( container, item ) {
                return $( "<li></li>" )
                    .data( "item.autocomplete", item )
                    .append( "<a>" + item.title + "</a>")
                    .appendTo( container );
            };
            
        },
        clear:function(){
            this.select.empty();
            this.container.empty();
        },
        add_item: function(v, txt){
            var se = this.select.get(0);
            var flag = false;
            if (v){
                for(var i=0; i<se.options.length; i++){
                    if (se.options[i].value == v){
                        if (!se.options[i].selected){
                            se.options[i].selected = true;
                        }
                        flag = true;
                        break;
                    }
                }
                if (!flag){
                    se.options.add(new Option(txt, v));
                    se.options[se.options.length-1].selected=true;
                    this._add_item(v, txt);
                }
            }
        },
        
        _add_item : function(value, text){
            var self = this;
            var item = $(template('<li rel="${value}"><span class="rm-text">${text}</span><span class="rm-blank">&times;</span></li>', {'value':value, 'text':text}));
            this.container.append(item);
            item.find('.rm-blank').click(function(){
                item.remove();
                var se = self.element.get(0);
                for(var i=0; i<se.options.length; i++){
                    if(se.options[i].value == value){
                        se.remove(i);
                    }
                }
            });

        }
,
        
        _remove_item: function(value){
            $('li[rel='+value+']', this.container).remove();
        },
        
        options : {
            'remove_all_txt':'Remove All',
            'width':null,
            'height':200,
            'label':'Search User:',
            minLength: 2
        },
        destroy: function() {
            this.display.remove();
            this.input.remove();
            this.element.show();
            $.Widget.prototype.destroy.call( this );
        }
    });
})( jQuery );
            
