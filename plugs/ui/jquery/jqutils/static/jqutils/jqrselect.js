/*
 * Author: limodou@gmail.com
 * This jquery plugin will be used as select replacement, and it'll just like 
 * autocomplete wigets and search some result from the server according the enterned text,
 * and the server will return all matched records, and the plugin will
 * display them.
 * old input <input value='1' alt='display' url='urlpath'></input>
 * server response will be [{'id':xxx, 'title':yyy}]
 */
(function( $ ) {
    $.widget( "ui.rselect", {
        _create: function() {
            var self = this,
                select = this.element.hide(),
                display = select.attr('alt') || '',
                title = select.attr('title') || 'Search Result',
                url = '';
                this.value = {'element':select.val(), 'input':display};
                
            
            if (!this.options.url){
                url = select.attr('url');
            }else{
                url = this.options.url;
            }
            
            var refresh_delicon = this.refresh_delicon = function(){
                var len = self.input.val().length;
                if(len>0) {
                    $(self.input).next("a").show();
                } else {
                    $(self.input).next("a").hide();
                }
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
                            refresh_delicon();
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
            
            var input = this.input = $( "<input>" )
                .insertAfter( select )
                .val( display )
                .css('display', 'inline')
                .css('paddingRight', '25px')
                .autocomplete({
                    delay: 200,
                    minLength: 2,
                    source: fetch_data,
                    select: function( event, ui ) {
                        self.element.val(ui.item.id);
                        input.val(ui.item.title);
                        if (self.options.onSelect){
                            self.options.onSelect.call(self);
                        }
                        
                        self.value['element'] = self.element.val();
                        self.value['input'] = self.input.val();
                        
                        return false;
                    }
                })
                .keydown(function(event){
                    var keycode = (event.keyCode ? event.keyCode : event.which);
                    if(keycode == 13){
                        event.preventDefault();
                    }
                })
                .keyup(refresh_delicon)
                .blur(function(){
                    if (self.input.val().length <= 0){
                        self.value['element'] = ''
                        self.value['input'] = ''
                    }
                    
                    self.element.val(self.value['element']);
                    self.input.val(self.value['input']);
                    
                    self.refresh_delicon();
                });

            input.data( "autocomplete" )._renderItem = function( ul, item ) {
                return $( "<li></li>" )
                    .data( "item.autocomplete", item )
                    .append( "<a>" + item.title + "</a>")
                    .appendTo( ul );
            };

//            this.button = $( "<a href='#' class='jqrselect-button' title='click to search'>&nbsp;&nbsp;&nbsp;&nbsp;</a>" )
//                .attr( "tabIndex", -1 )
//                .attr( "title", title )
//                .insertAfter( input )
//                .click(function(e) {
//                    e.preventDefault();
//                    // close if already visible
//                    if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
//                        input.autocomplete( "close" );
//                        return;
//                    }
//
//                    // work around a bug (likely same cause as #5265)
//                    $( this ).blur();
//
//                    // pass empty string as value to search for, displaying all results
//                    var old_minLength = input.autocomplete('option', 'minLength');
//                    input.autocomplete('option', 'minLength', 0);
//                    input.autocomplete( "search", input.val() );
//                    input.autocomplete('option', 'minLength', old_minLength);
//                    input.focus();
//                });
            this.clearBtn = $("<a href='#' class='jqrselect-clearButton' title='click to clear' style='display:none'>&times;</a>" )
                .attr( "tabIndex", -1 )
                .insertAfter( this.input )
//                .insertAfter( this.button )
                .click(function(e) {
                    e.preventDefault();
                    if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
                        input.autocomplete( "close" );
                        return;
                    }
                    
                    // work around a bug (likely same cause as #5265)
                    $( this ).blur();
                    input.val('');
                    self.element.val('');
                    refresh_delicon();
                });
            
            refresh_delicon();
            
            if(!self.options.showRemoveable){
            	this.clearBtn.css("display", "none");
            }
        },
        
        getValue: function(){
            return this.element.val();
        },
        
        getText: function(){
            return this.input.val();
        },

        clear: function(){
            this.input.val('');
            this.element.val('');
            this.value = {'element':'', 'input':''};
            this.refresh_delicon();
        },
        options:{
        	showRemoveable:true,
            url:null
        },
        destroy: function() {
            this.input.remove();
//            this.button.remove();
            this.clearBtn.remove();
            this.element.show();
            $.Widget.prototype.destroy.call( this );
        }
    });
})( jQuery );
