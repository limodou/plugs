/*
 * author: Lin Wei
 * tel: 13691031092
 * email: wataru19831111@hotmail.com
 * Date: 2013-02-28
 * version 0.1 (single select only)
 * depend on jQuery,Bootstrap,select2 & zTree
 */


SingleDropDownTree2=function(setting){
	this.config=setting;
};
SingleDropDownTree2.prototype=$.extend(new Select2["class"].single(), {
		createContainer: function () {
            var container = $("<div></div>", {
                "class": "select2-container"
            }).html([
                "<a href='#' onclick='return false;' class='select2-choice'>",
                "   <span></span>" ,
                "	<abbr class='select2-search-choice-close' style='display:none;'></abbr>",
                "   <div><b></b></div>" ,
                "</a>",
                "<div class='select2-drop select2-offscreen'>" ,
                "   <div class='select2-search'>" ,
                "       <input type='text' autocomplete='off' class='select2-input'/>" ,
                "   </div>" ,
                "   <ul class='select2-results'>" ,
                "   </ul>" ,
                "	<ul class='ztree' style='width:auto;height:auto;max-height:400px;border:0;overflow-y:auto;margin-top:0'></ul>" ,
                "</div>"].join(""));
            return container;
        },
        // single
        initContainer: function () {
        	var self=this;
        	Select2["class"].single.prototype.initContainer.call(this);
        	this.treeContainer=self.results.next();
        	/*this.treeBtn=this.container.find("b");
        	this.treeBtn.on("click",function(event){
        		self.showTree(self)
        	});*/
        	this.selection.bind("focus",function(){
        		//self.treeContainer.hide();
        		self.search.parent().show();
        		//self.showTree(self)
        		//self.results.show();
        	});
        },
        updateSelection:function(data){
        	//console.log(data)
        	var container=this.selection.find("span"), formatted;
            this.selection.data("select2-data", data);
            container.empty();
            formatted=this.opts.formatSelection(data, container);
            if (formatted !== undefined) {
                container.append(this.opts.escapeMarkup(formatted));
            }
            this.selection.removeClass("select2-default");
            if (this.opts.allowClear && data.id) {
                this.selection.find("abbr").show();
            }
        },
        clear: function() {
            var v = this.opts.element.val();
            var se = this.opts.element[0];
            for(var i=0; i<se.options.length; i++){
                if(se.options[i].value == v){
                    se.remove(i);
                }
            }
            
//            this.opts.element.val("");
            this.triggerChange({ removed: {id:this.opts.element.val()} });
            //console.log("clear",this.opts.element.val());
            this.selection.find("span").empty();
            this.selection.removeData("select2-data");
            this.setPlaceholder();
        },
        setPlaceholder: function () {
            var placeholder = this.getPlaceholder();

            if (!this.opts.element.val()) {
                if (placeholder === undefined) placeholder = '';

                // check for a first blank option if attached to a select
                if (this.select && this.select.find("option:first").text() !== "") return;

                this.selection.find("span").html(this.opts.escapeMarkup(placeholder));

                this.selection.addClass("select2-default");

                this.selection.find("abbr").hide();
            }
        },
        updateResults:function(){
        	Select2["class"].single.prototype.updateResults.call(this);
        	this.treeContainer.hide();
        },
        opening: function () {
        	//console.log("opening");
        	if(this.config.search){
	            Select2["class"].single.prototype.opening.call(this);
        	}
        	else{
        		Select2["class"].single.prototype.opening.call(this);
        		//console.log(this.search)
        		this.search.parent().hide();
        		this.results.hide();
        	}
            this.showTree();
        },
        showTree:function(){
        	var self=this;
        	//self.search.parent().hide();
        	//self.results.hide();
        	//Select2["class"].single.prototype.parent.opening.call(self);
        	
        	this.treeContainer.show();
        	
        	var filter=function (treeId, parentNode, childNodes) {
				if (!childNodes) return null;
				for (var i=0, l=childNodes.length; i<l; i++) {
					childNodes[i].name = childNodes[i].name.replace(/\.n/g, '.');
				}
				return childNodes;
			};
			
			var beforeAsync=function(treeId,treeNode){
				if(treeNode && !treeNode.id){
					treeNode.id=treeNode.name;
				}
			};
			
			var beforeClick=function(treeId, treeNode) {
				//var check = (treeNode && !treeNode.isParent);
				var check = (treeNode && !treeNode.disSelected)||(treeNode && treeNode.node_type!=2);
				if(self.config.selectCheckField && !treeNode[self.config.selectCheckField])
                    check = false;
//                if (!check) alert("Can not select this node...");
				return check;
			};
			
			var onClick=function(e, treeId, treeNode) {
				if(self.config.tree.userOnly){
					if(treeNode.node_type==2){
						treeId=treeNode.id.split(",")[0];
						self.data({id:treeId, text:treeNode.name});
						self.onSelect({id:treeId, text:treeNode.name});
						self.treeContainer.hide();
						self.close();
						self.focus();
					}
				}
				else{
					self.data({id:treeNode.id, text:treeNode.name});
					self.onSelect({id:treeNode.id, text:treeNode.name});
					self.treeContainer.hide();
					self.close();
					self.focus();
				}
			};
			
			var onAsyncSuccess=function(event,treeId,treeNode,msg){
			};
			
			var onNodeCreated=function(event, treeId, treeNode){
				if(treeNode.hidden){
					$("#"+treeNode.tId).css({display:"none"});
				}
			};
			
        	var setting={
				selectCheckField:null,
                view: {
					dblClickExpand: false
				},
				async: {
					enable: !!this.config.tree.url,
					url:this.config.tree.url,
					//autoParam:["id", "name=n", "level=lv"],
					autoParam:["id"],
					//otherParam:{"otherParam":"zTreeAsyncTest"},
					dataFilter: filter
				},
				data: {
					keep:{
						leaf:true,
						parent:true	
					},
					simpleData: {
						enable: true
					}
				},
				callback: {
					beforeAsync:beforeAsync,
					beforeClick: beforeClick,
					onClick: onClick,
					onAsyncSuccess:onAsyncSuccess,
					onNodeCreated:onNodeCreated
				}
			};
        	
			setting=$.extend(true, setting,this.config.tree);
        	$.fn.zTree.init(this.treeContainer,setting);
        }
});

jQuery.fn.dropDownTree2=function(){
        var args = Array.prototype.slice.call(arguments, 0),
            opts,
            select2,
            value, multiple, allowedMethods = ["val", "destroy", "opened", "open", "close", "focus", "isFocused", "container", "onSortStart", "onSortEnd", "enable", "disable", "positionDropdown", "data"];

        this.each(function () {
            if (args.length === 0 || typeof(args[0]) === "object") {
            	var defaults={
            		formatNoMatches:function(){/*console.log(this);*/return "没找到对应值"},
            		formatInputTooShort:function(input, min){return "还需要输入"+(min-input.length)+"个字符"},
            		formatSelectionTooBig:function(limit){return "只能选择"+limit+"条数据"},
            		formatSearching:function(){return "正在搜索，请稍候..."},
            		minimumInputLength:2,
					allowClear:true,
					placeholder:args[0].search?"输入文字进行搜索":"",
					ajax: {
						url: "",
						dataType: 'json',
						data: function (term, page) {
							return {
								term: term, 
								page_limit: 10
							};
						},
						results: function (data, page) {
							return {results: data};
						}
					}
            	};
            	if(args[0].search){
	            	defaults.ajax.url=args[0].search.url;
	            	args[0].search=args[0].width?$.extend(defaults,args[0].search,{width:args[0].width}):"";
	                opts = args.length === 0 ? {} : $.extend({width:"200px"}, args[0].search);
            	}
            	else{
            		opts = args.length === 0 ? {} : $.extend({allowClear:true}, args[0]);
            	}
            	
                opts.element = $(this);

                if (opts.element.get(0).tagName.toLowerCase() === "select") {
                    multiple = opts.element.attr("multiple");
                } else {
                    multiple = opts.multiple || false;
                    if ("tags" in opts) {opts.multiple = multiple = true;}
                }

                select2 = multiple ? new Select2["class"].multi() : new SingleDropDownTree2(args[0]);
                select2.init(opts);
            } else if (typeof(args[0]) === "string") {

                if (indexOf(args[0], allowedMethods) < 0) {
                    throw "Unknown method: " + args[0];
                }

                value = undefined;
                select2 = $(this).data("select2");
                if (select2 === undefined) return;
                if (args[0] === "container") {
                    value=select2.container;
                } else {
                    value = select2[args[0]].apply(select2, args.slice(1));
                }
                if (value !== undefined) {return false;}
            } else {
                throw "Invalid arguments to select2 plugin: " + args;
            }
        });
        return (value === undefined) ? this : value;
    
};
