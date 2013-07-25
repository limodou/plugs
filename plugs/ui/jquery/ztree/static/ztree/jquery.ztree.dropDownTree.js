/*
 * author: Lin Wei
 * tel: 13691031092
 * email: wataru19831111@hotmail.com
 * Date: 2012-02-24
 */
jQuery.fn.zTree.dropDownTree=function(config){
	return new function(){
		var self=this;
		var beforeClick=function(treeId, treeNode) {
			//var check = (treeNode && !treeNode.isParent);
			var check = (treeNode && !treeNode.disSelected);
            if(self.setting.selectCheckField && !treeNode[self.setting.selectCheckField])
                check = false;
			if (!check) alert("Can not select this node...");
			return check;
		};
		
		var onClick=function(e, treeId, treeNode) {
			var zTree = $.fn.zTree.getZTreeObj(self.setting.dom.menuTree.id),
			nodes = zTree.getSelectedNodes(),
			v = "",id="";
			nodes.sort(function compare(a,b){return a.id-b.id;});
			for (var i=0, l=nodes.length; i<l; i++) {
				v += nodes[i].name + ",";
				id +=nodes[i].id + ",";
			}
			if (v.length > 0 ) v = v.substring(0, v.length-1);
			if (id.length > 0 ) id = id.substring(0, id.length-1);
			var valueBox = $(self.setting.dom.valueBox);
			/*var count=v.split(",");
			if(count>0){
				v=cityObj.attr("value")+","+v;
			}
			if(count>2){
				cityObj.attr("value", count+"个人被选中");		
			}
			else{
				cityObj.attr("value", v);
			}*/
			valueBox.attr("value", id);
			$(self.setting.dom.textBox).attr("value", v);
            if(config.changeEvent) {
                config.changeEvent.call(valueBox, id);
            }
			hideMenu();
		};
		
		var onAsyncSuccess=function(){
			//alert($(self.setting.dom.menuTree).outerHeight()+"px")
			//self.setting.dom.menuDiv.style.height=$(self.setting.dom.menuTree).outerHeight()+"px";
		};
		
		self.setting={
            selectCheckField:null,
			dom:{},
			view: {
				dblClickExpand: false
			},
			dom:{
			},
			async: {
				enable: !!config.url,
				url:config.url,
				autoParam:["id"],
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
				beforeClick: beforeClick,
				onClick: onClick,
				onAsyncSuccess:onAsyncSuccess
			}
		};
		
		
		var filter=function (treeId, parentNode, childNodes) {
			if (!childNodes) return null;
			for (var i=0, l=childNodes.length; i<l; i++) {
				childNodes[i].name = childNodes[i].name.replace(/\.n/g, '.');
			}
			return childNodes;
		};
	
		
	
		var showMenu=function () {
			var textBox=$(self.setting.dom.textBox);
			var textBoxOffset = textBox.offset();
			$(self.setting.dom.menuDiv).css({left:textBoxOffset.left + "px", top:textBoxOffset.top + textBox.outerHeight()+ "px"}).slideDown("fast");
			$("body").bind("mousedown", onBodyDown);
		};
		
		var delSelected=function (){
			var valueBox = $(self.setting.dom.valueBox);
			valueBox.attr("value","");
			var textBox = $(self.setting.dom.textBox);
			textBox.attr("value","");
		};
		
		var hideMenu=function () {
			$(self.setting.dom.menuDiv).fadeOut("fast");
			$("body").unbind("mousedown", onBodyDown);
		};
		
		var onBodyDown=function (event) {
			if (!(event.target.className == "ztree" || $(event.target).parents(".menuContent").length>0)) {
				hideMenu();
			}
		};
		
		var createDom=function(config){
			var valueBox=document.getElementById(config.renderTo);
			valueBox.style.display="none";
			var parentContainer=valueBox.parentNode;
			var textBox=document.createElement("input");
			textBox.type="text";
			textBox.className="x-form-text";
			textBox.readOnly=true;
			var alt=valueBox.getAttribute("alt");
			if(alt && alt.length>0){
				textBox.value=alt;
			}
			$(textBox).keydown(function(e){
				e.preventDefault();
				if(e.keyCode==8||e.keyCode==46){//backspace or delete
					delSelected();
				}
			});
			self.setting.dom.textBox=textBox;
			self.setting.dom.valueBox=valueBox;
			var renderBox=document.createElement("div");
			$(renderBox).css({display:"inline",padding:"2 10"});
			var selBtn=document.createElement("a");
			selBtn.className="selBtn";
			$(selBtn).bind('click',null,showMenu);
			
			renderBox.appendChild(valueBox);
			renderBox.appendChild(textBox);
			renderBox.appendChild(selBtn);
			parentContainer.appendChild(renderBox);
			
			var menuDiv=document.createElement("div");
			menuDiv.className="menuContent";//标识类型接口
			$(menuDiv).css({display:"none",position:"absolute"});
			self.setting.dom.menuDiv=menuDiv;
			var menuTree=document.createElement("ul");
			menuTree.id=config.renderTo+"_treeRoot";
			menuTree.className="ztree";
			menuTree.style.marginTop="0px";
			menuTree.style.width=config.width?config.width+"px":valueBox.style.width;
			menuTree.style.height=config.height?config.height+"px":"";
			if(!config.width && /msie/.test(navigator.userAgent.toLowerCase())){
				menuTree.style.width=$(textBox).outerWidth()+"px";
			}
			menuDiv.appendChild(menuTree);
			document.body.appendChild(menuDiv);
			self.setting.dom.menuTree=menuTree;
		}(config);
		
		var opts = $.extend(true, self.setting, config)
		return $.fn.zTree.init($(self.setting.dom.menuTree),opts);
	}
};
