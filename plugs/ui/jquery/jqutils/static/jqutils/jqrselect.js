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
                value = select.val(),
                display = select.attr('alt'),
                title = select.attr('title') || 'Search Result',
                url = '';
            if (!this.options.url){
                url = select.attr('url');
            }else{
                url = this.options.url;
            }
            var input = this.input = $( "<input>" )
                .insertAfter( select )
                .val( display )
                .autocomplete({
                    delay: 0,
                    minLength: 999,
                    source: url,
                    select: function( event, ui ) {
                        self.element.val(ui.item.id);
                        input.val(ui.item.title);
                        return false;
                    }
                }).keypress(function(event){
                    var keycode = (event.keyCode ? event.keyCode : event.which);
                    if(keycode == '13'){
                        var old_minLength = input.autocomplete('option', 'minLength');
                        input.autocomplete('option', 'minLength', 0);
                        input.autocomplete( "search", input.val() );
                        input.autocomplete('option', 'minLength', old_minLength);
                        input.focus();
                    }
                });

            input.data( "autocomplete" )._renderItem = function( ul, item ) {
                return $( "<li></li>" )
                    .data( "item.autocomplete", item )
                    .append( "<a>" + item.title + "</a>")
                    .appendTo( ul );
            };

            this.button = $( "<a href='#' class='jqrselect-button' title='click to search'>&nbsp;&nbsp;&nbsp;&nbsp;</a>" )
                .attr( "tabIndex", -1 )
                .attr( "title", title )
                .insertAfter( input )
                .click(function(e) {
                    e.preventDefault();
                    // close if already visible
                    if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
                        input.autocomplete( "close" );
                        return;
                    }

                    // work around a bug (likely same cause as #5265)
                    $( this ).blur();

                    // pass empty string as value to search for, displaying all results
                    var old_minLength = input.autocomplete('option', 'minLength');
                    input.autocomplete('option', 'minLength', 0);
                    input.autocomplete( "search", input.val() );
                    input.autocomplete('option', 'minLength', old_minLength);
                    input.focus();
                });
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
        },
        
        destroy: function() {
            this.input.remove();
            this.button.remove();
            this.element.show();
            $.Widget.prototype.destroy.call( this );
        }
    });
})( jQuery );
