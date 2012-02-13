(function( $ ) {
    $.widget( "ui.paginator", {
        _create: function() {
            var self = this;
            var s = self.options;
            if (s.start == 0) s.start = 1;
            self.currentPage = s.start - 1;
            var totalpages = self.totalpages = parseInt(s.total / s.page_rows);
            if (s.total % s.page_rows > 0) totalpages++;
            var container = $(self.element).addClass('pagination').empty();
            var list = self.list = $('<ul/>').appendTo(container);
            
            //bind events
            container.delegate('li.prev a', 'click', function(e) { 
                e.preventDefault();
                if ($(this).parent().hasClass('disabled')) return;
                self.currentPage = parseInt(list.find('li.active a').text()) - 1; 
                self.navigate(--self.currentPage); 
                self.load(self.currentPage);
                });
            container.delegate('li.next a', 'click', function(e) { 
                e.preventDefault();
                if ($(this).parent().hasClass('disabled')) return;
                self.currentPage = parseInt(list.find('li.active a').text()); 
                self.navigate(self.currentPage); 
                self.load(self.currentPage);
                });
            
            var btnPrev = self.btnPrev = $('<li class="prev"><a href="#">' + s.prev + '</a></li>');
            var btnNext = self.btnNext = $('<li class="next"><a href="#">'+s.next+'</a></li>');
            list.append(btnPrev).append(btnNext);
            self.navigate(self.currentPage);
            if (s.init_load){
                this.load(this.currentPage);
            }
        },
        options : {
            total: 0,
            page_rows: 0,
            length: 10,
            next: 'Next',
            prev: 'Prev',
            first: 'First',
            last: 'Last',
            start: 1,
            init_load: false,
            onchange: null
        },
        _buildNavigation: function(startPage) {
            var s = this.options;
            var self = this;
            if (s.total <= s.page_rows) return;
            var target = this.list.find('li:last');
            for (var i = startPage; i < startPage + s.length; i++) {
                if (i == this.totalpages) break;
                var li = $('<li/>')
                    .insertBefore(target)
                    .append($('<a>').attr('rel', (i + 1))
                    .attr('href', '#')
                    .text(i + 1))
                li.delegate('a', 'click', function(e) {
                    e.preventDefault()
                    self.currentPage = startPage + $(this).parent().closest('li').prevAll().length - 1;
                    self.navigate(self.currentPage);
                    self.load(self.currentPage);
                });
            }
        },
        navigate: function(topage) {
            var s = this.options;
            for(var i=this.list.find('li').size()-2; i>0; i--){
                this.list.find('li:eq('+i+')').remove();
            }
            var index = topage;
            var mid = s.length / 2;
            if (s.length % 2 > 0) mid = (s.length + 1) / 2;
            var startIndex = 0;
            if (topage >= 0 && topage < this.totalpages) {
                if (topage >= mid) {
                    if (this.totalpages - topage > mid)
                        startIndex = topage - (mid - 1);
                    else if (this.totalpages > s.length)
                        startIndex = this.totalpages - s.length;
                }
                this._buildNavigation(startIndex); 
                this.list.find('li').removeClass('active');
                this.list.find('li a[rel='+(index+1)+']').parent().addClass('active');
            }
            this._showRequiredButtons();
        },
        _showRequiredButtons: function() {
            var s = this.options;
            if (this.totalpages > 1) {
                if (this.currentPage > 0) 
                    this.btnPrev.removeClass('disabled'); 
                else 
                    this.btnPrev.addClass('disabled'); 
        
                if (this.currentPage == this.totalpages - 1)
                    this.btnNext.addClass('disabled'); 
                else 
                    this.btnNext.removeClass('disabled');
            }
            else {
                this.btnPrev.addClass('disabled');
                this.btnNext.addClass('disabled');
            }
        },
        load: function(page){
            if (this.options.onchange != null) {
                this.options.onchange((this.currentPage + 1));
            }
            
        },
        destroy: function() {
            this.element.empty();
            $.Widget.prototype.destroy.call( this );
        }
    });
})( jQuery );
