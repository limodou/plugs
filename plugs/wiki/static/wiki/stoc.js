(function($){
 $.fn.stoc = function(options) {
	//Our default options
	var defaults = {
		search: "body", //where we will search for titles
		depth: 6, //how many hN should we search
		start: 1, //which hN will be the first (and after it we go just deeper)
		stocTitle: "<h2>Topic of Content</h2>", //what to display before our box
		listType: "ul", //could be ul or ol
		smoothScroll: 1,
        tocnumber: false
	};

	//let's extend our plugin with default or user options when defined
	var options = $.extend(defaults, options);

    return this.each(function() {
		//"cache" our target and search objects
		var obj = $(this); //target
		var src = $(options.search); //search
		//let's declare some variables. We need this var declaration to create them as local variables (not global)
		var appHTML = "", tagNumber = 0, txt = "", id = "", before = "", 
            after = "", previous = options.start, start = options.start, 
            depth = options.depth, i = 0, srcTags = "h" + options.start, 
            cacheHN = "", j, s;
        var find = false;
        var tocnumber;
        var cur_number = {};

		//which tags we will search
		while ( depth > 1) {
			start++; //we will just get our start level and numbers higher than it
			srcTags = srcTags + ", h" + start;
			depth--; //since went one level up, our depth will go one level down
		}
		src.find(srcTags).each(function() {
            find = true;
            
			//we will cache our current H element
			cacheHN = $(this);
			//if we are on h1, 2, 3...
			tagNumber = ( cacheHN.get(0).tagName ).substr(1);
            
            for (j=parseInt(tagNumber)+1; j<=parseInt(previous); j++){
                cur_number[j.toString()] = 0;
            }
            
            //calculate tocnumber
            if (!cur_number[tagNumber]){
                cur_number[tagNumber] = 1;
            }else{
                cur_number[tagNumber] += 1;
            }
            s = [];
            j = options.start;
            while (j<=parseInt(tagNumber)){
                if (cur_number[j])
                    s.push(cur_number[j]); 
                j++;
            }
            tocnumber = s.join('.');
			//sets the needed id to the element
			id = cacheHN.attr('id');
			if (id == "") { //if it doesn't have only, of course
				id = "h" + tagNumber + "_" + i;
				cacheHN.attr('id', id);
			}
			//our current text
			txt = cacheHN[0].firstChild.textContent;
            
            if (options.tocnumber){
                txt = '<span class="tocnumber">'+tocnumber+'</span> ' + txt;
            }

			switch(true) { //with switch(true) we can do comparisons in each case
				case (tagNumber > previous) : //it means that we went down one level (e.g. from h2 to h3)
						appHTML = appHTML + "<" + options.listType +"><li>"+ before +"<a href=\"#"+ id + "\">" + txt + "</a>";
						previous = tagNumber;
					break;
				case (tagNumber == previous) : //it means that stay on the same level (e.g. h3 and stay on it)
						appHTML = appHTML + "</li><li>"+ before +"<a href=\"#"+ id + "\" class='toclink'>" + txt +  "</a>";
					break;
				case (tagNumber < previous) : //it means that we went up but we don't know how much levels  (e.g. from h3 to h2)
						while(tagNumber != previous) {
							appHTML = appHTML + "</" + options.listType +"></li>";
							previous--;
						}
						appHTML = appHTML + "<li>"+ before +"<a href=\"#"+ id + "\">" + txt + "</a></li>";
					break;
			}
			i++;
		});

		//corrects our last item, because it may have some opened ul's
		while(find && (tagNumber != options.start)) {
			appHTML = appHTML + "</" + options.listType +">";
			tagNumber--;
		}
		//append our html to our object
		appHTML = '<table><tbody><tr><td>' + 
            options.stocTitle + "<"+ options.listType + " class='tocitems'>" + 
            appHTML + 
            "</" + options.listType + ">" +
            '</td></tr></tbody></table>';
		obj.append(appHTML);

		//our pretty smooth scrolling here
		// acctually I've just compressed the code so you guys will think that I'm the man . Source: http://css-tricks.com/snippets/jquery/smooth-scrolling/
		if (options.smoothScroll == 1) {
        
            $("#toc a.toclink").click(function() {  
                $("html, body").animate({  
                    scrollTop: $($(this).attr("href")).offset().top + "px"  
                }, {  
                    duration: 500,  
                    easing: "swing"  
                });  
                return false;  
            });  
        
		}
    });
 };
})(jQuery);
