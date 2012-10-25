/* =========================================================
 * jquery.scrollpagination.js v1.0
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


!function( $ ){

  "use strict"

  /* MODAL CLASS DEFINITION
   * ====================== */

  var ScrollPagination = function ( content, options ) {
    var that = this;
    this.options = options;
    this.element = $(content);
    var target = this.options.target;
    this.currentPage = this.options.start;
    
    $(target).scroll(function(e){
        var load = $(target).scrollTop()+that.options.offset >= $(document).height() - $(target).height();
        if(load && (that.currentPage*that.options.pageRows) < that.options.total){
            that.load(that.currentPage+1);
        }  
    });   
    
    //Load init page if initLoad is true
    if (this.options.initLoad){
        this.load(this.currentPage);
    }

  }

  ScrollPagination.prototype = {
  
      constructor: ScrollPagination
    , load: function (page){
        this.currentPage = page
        if (this.options.onChange) {
            this.options.onChange.call(this, page);
        }
    }
  }

 /* MODAL PLUGIN DEFINITION
  * ======================= */

  $.fn.scrollpagination = function (option) {
    var args = Array.prototype.slice.call(arguments);
    args.shift();
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('scrollpagination')
        , options = $.extend({}, $.fn.scrollpagination.defaults, typeof option == 'object' && option);
      if (!data) $this.data('scrollpagination', (data = new ScrollPagination(this, options)));
      if (typeof option == 'string') data[option].apply(data, args);
    })
  }

  $.fn.scrollpagination.defaults = {
      total: 0,
      pageRows: 0,
      start: 1,
      initLoad: false,
      target: window,
      offset: 20,
      onChange: null
  }

  $.fn.scrollpagination.Constructor = ScrollPagination;

}( window.jQuery );

