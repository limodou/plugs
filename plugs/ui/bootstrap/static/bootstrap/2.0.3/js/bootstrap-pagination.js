/* =========================================================
 * bootstrap-pagination.js v1.0
 * =========================================================
 * Copyright limodou.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================= */


!
function($) {

  "use strict"

  /* MODAL CLASS DEFINITION
   * ====================== */

  var Pagination = function(content, options) {

      var that = this;
      this.options = options;

      this.$element = $(content).addClass('pagination').empty();
      var list = $('<ul/>').appendTo(this.$element);

      var btnFirst = this.btnFirst = $('<li class="first"><a href="#">' + this.options.first + '</a></li>');
      var btnPrev = this.btnPrev = $('<li class="prev"><a href="#">' + this.options.prev + '</a></li>');
      var btnNext = this.btnNext = $('<li class="next"><a href="#">' + this.options.next + '</a></li>');
      var btnLast = this.btnLast = $('<li class="last"><a href="#">' + this.options.last + '</a></li>');

      list.append(btnPrev).append(btnNext);
      list.append(this.btnLast);
      list.prepend(this.btnFirst);

      this.$element.delegate('li:enabled, li', 'click.pagination', function(e) {
      
        e.preventDefault();
      
        var $this = $(this);
        var list = that.$element.find('ul');
      
        if ($this.hasClass('prev')) {
          that.currentPage = parseInt(list.find('li.active a').text()) - 1;
        } else if ($this.hasClass('next')) {
          that.currentPage = parseInt(list.find('li.active a').text()) + 1;
        } else if ($this.hasClass('first')) {
          that.currentPage = 1;
        } else if ($this.hasClass('last')) {
          that.currentPage = (that.options.total);
        } else {
          that.currentPage = parseInt($this.text());
        }
      
        if (!$this.hasClass('disabled')) {
          that.load(--that.currentPage);
        }
      
      });

    }

  Pagination.prototype = {

    constructor: Pagination,
    show: function(total, start) {
      this.options.start = start || this.options.start;
      this.options.total = total || this.options.total;
      this.currentPage = this.options.start - 1;
      this.totalPages = parseInt(this.options.total / this.options.pageRows);
      if (this.options.total % this.options.pageRows > 0) this.totalPages++;
      navigate.call(this, this.currentPage);
      if (this.options.initLoad) {
        this.load(this.currentPage);
      }
    },
    load: function(page) {
      navigate.call(this, page);
      if (this.options.onChange) {
        this.options.onChange((this.currentPage + 1));
      }
    }
  }

  /* MODAL PRIVATE METHODS
   * ===================== */

  function _buildNavigation(startPage) {

    var s = this.options;
    var self = this;
    var list = this.$element.find('ul');

    if (s.total <= s.pageRows) return;

    var target = list.find('li:last').prev();

    for (var i = startPage; i < startPage + s.length; i++) {
      if (i == this.totalPages) break;
      var li = $('<li/>').insertBefore(target).append($('<a>').attr('rel', (i + 1)).attr('href', '#').text(i + 1));
    }

    this.$element.find('ul').append(this.btnLast);
    this.$element.find('ul').prepend(this.btnFirst);

  }

  function navigate(topage) {

    var s = this.options;
    var list = this.$element.find('ul');
    for (var i = list.find('li').size() - 4; i > 0; i--) {
      list.find('li').eq(i+1).remove();
    }
    var index = topage;
    var mid = s.length / 2;
    if (s.length % 2 > 0) mid = (s.length + 1) / 2;
    var startIndex = 0;
    if (topage >= 0 && topage < this.totalPages) {
      if (topage >= mid) {
        if (this.totalPages - topage > mid) startIndex = topage - (mid - 1);
        else if (this.totalPages > s.length) startIndex = this.totalPages - s.length;
      }
      _buildNavigation.call(this, startIndex);
      list.find('li').removeClass('active');
      list.find('li a[rel=' + (index + 1) + ']').parent().addClass('active');
    }
    
    _showRequiredButtons.call(this);

  }

  function _showRequiredButtons() {
    var s = this.options;
    if (this.totalPages > 1) {
      if (this.currentPage > 0) {
        this.btnPrev.removeClass('disabled');
        this.btnFirst.removeClass('disabled');
      } else {
        this.btnPrev.addClass('disabled');
        this.btnFirst.addClass('disabled');
      }

      if (this.currentPage == this.totalPages - 1) {
        this.btnNext.addClass('disabled');
        this.btnLast.addClass('disabled');
      } else {
        this.btnNext.removeClass('disabled');
        this.btnLast.removeClass('disabled');
      }
    } else {
      this.btnPrev.addClass('disabled');
      this.btnNext.addClass('disabled');
      this.btnFirst.addClass('disabled');
      this.btnLast.addClass('disabled');
    }
  }


  /* MODAL PLUGIN DEFINITION
   * ======================= */

  $.fn.pagination = function(option) {
    var args = Array.prototype.slice.call(arguments);
    args.shift();
    return this.each(function() {
      var $this = $(this),
        data = $this.data('pagination'),
        options = $.extend({}, $.fn.pagination.defaults, typeof option == 'object' && option);
      if (!data) $this.data('pagination', (data = new Pagination(this, options)));
      if (typeof option == 'string') data[option].apply(data, args);
    })
  }

  $.fn.pagination.defaults = {
    total: 0,
    pageRows: 0,
    length: 10,
    next: 'Next',
    prev: 'Prev',
    first: 'First',
    last: 'Last',
    start: 1,
    initLoad: false,
    onChange: null
  }

  $.fn.pagination.Constructor = Pagination;

}(window.jQuery);