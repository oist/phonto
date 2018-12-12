OntoSearcher = function(){
	//this.targetBase = "http://localhost:8000";
	this.targetBase = "http://phonto.unit.oist.jp";

	this.defaultdialog = false;
	this.defaultdialog_width = 500;
	this.defaultdialog_height = 300;
	this.defaultdialog_title = "Ontological Links";
};
OntoSearcher.prototype.error = function(response){};

/*
* args
*     words:[word,word]
*     usedefaultdialog:
*     defaultdialog_width
*     defaultdialog_height
*     defaultdialog_title
*     success: function
*     error: function
*
*/
OntoSearcher.prototype.exactSearch = function(args){
	if(!args){ return;}

	var data ;
	var me = this;
	if(args.usedefaultdialog){
		args.success = this._showdafaultdialog;
	}
	if(args.defaultdialog_width){
		this.defaultdialog_width = args.defaultdialog_width;
	}
	if(args.defaultdialog_height){
		this.defaultdialog_height = args.defaultdialog_height;
	}
	if(args.defaultdialog_width){
		this.defaultdialog_title = args.defaultdialog_title;
	}
	var wordstr = args.words.join("_,_");

	this._ajax({
		 "url" : this.targetBase + "/apps/searchdball/" + wordstr
		,params: data
		,"success":function(response , _self){
			if(args.success){
				args.success(response , _self);
			}
		}
		,"error":args.error
		,"_self":me
	});
};
/*
* args
*     dbname:
*     identifier:
*     usedefaultdialog:
*     usewrapper:
*     defaultdialog_width
*     defaultdialog_height
*     defaultdialog_title
*     success: function
*     error: function
*
*/
OntoSearcher.prototype.getNeighbors = function(args){
	if(!args){ return;}

	var data ;
	var me = this;
	if(args.usedefaultdialog){
		args.success = this._showdafaultdialog;
	}
	if(args.defaultdialog_width){
		this.defaultdialog_width = args.defaultdialog_width;
	}
	if(args.defaultdialog_height){
		this.defaultdialog_height = args.defaultdialog_height;
	}
	if(args.defaultdialog_width){
		this.defaultdialog_title = args.defaultdialog_title;
	}
	this.usewrapper = args.usewrapper;
	
	this._ajax({
		 "url" : this.targetBase + "/apps/searchneighbors/" + args.dbname +"/" + args.identifier
		,params: {}
		,"success":function(response , _self){
			if(args.success){
				args.success(response , _self);
			}
		}
		,"error":args.error
		,"_self":me
	});
};

OntoSearcher.prototype._ajax = function(args){
	var data = args.params;

	var xhreq = new XMLHttpRequest();
	xhreq.onreadystatechange = function()
	{
	    var READYSTATE_COMPLETED = 4;
	    var HTTP_STATUS_OK = 200;

	    if( this.readyState == READYSTATE_COMPLETED ){
		    if( this.status == HTTP_STATUS_OK ){
		    	var response;
		    	var skipjsonadjust;
		    	try {
			    	response = JSON.parse(this.responseText);
				} catch (e) {
					try{
						response = eval(this.responseText);
					} catch (ex) {
						skipjsonadjust = true;
						response = this.responseText;
					}
					
				}
		    	if(args.success){
		    		if(!skipjsonadjust){
		    			response = response.payload;
		    		}
		    		args.success(response , args._self);
		    	}
			}else{
		    	if(args.error){
		    		args.error(this.responseText ,args._self);
		    	}
				
		    }
		}
	}

	var type = args.type || 'GET';
	xhreq.open( type, args.url ,true);

	if(type == 'POST'){
		xhreq.setRequestHeader( 'Content-Type', 'application/x-www-form-urlencoded' );
	}
	xhreq.send( this._encodeHTMLForm( data ) );
};
OntoSearcher.prototype._encodeHTMLForm = function( data ){
	var params = [];

	for( var name in data ){
		var value = data[ name ];
		var param = encodeURIComponent( name ) + '=' + encodeURIComponent( value );

		params.push( param );
	}

	return params.join( '&' ).replace( /%20/g, '+' );
};
OntoSearcher.prototype._showdafaultdialog = function(response , _self){
	var newDiv = document.getElementById("ontosearcher_defaultdiv");
	var datatcontent =  document.getElementById("ontosearcher_defaultdiv_content");
	var basehtml = "";
	basehtml += "<div id='ontosearcher_defaultdiv_headerparent' class='headerparent'><div class='header'>";
	basehtml += _self.defaultdialog_title ;
	basehtml += "</div><div id='ontosearcher_defaultdiv_closebtn' class='closebtn'>x</div><div style='clear:both'></div></div>";
	basehtml += "<div id='ontosearcher_defaultdiv_content' class='content'>";
	basehtml += "</div>";

	if(datatcontent){
		datatcontent.innerHTML = "";
	}else{
		if(newDiv){
			newDiv.innerHTML = basehtml;
		}else{
			newDiv = document.createElement("div");
			newDiv.innerHTML = basehtml;
			newDiv.id = "ontosearcher_defaultdiv";
			newDiv.classList.add("ontosearcher_defaultdiv");
		}
		document.body.appendChild(newDiv);
		newDiv.style.position = "absolute";
		newDiv.style.width = _self.defaultdialog_width + "px";
		newDiv.style.height = _self.defaultdialog_height + "px";
		
	}
	newDiv.style.display = "none";
	datatcontent =  document.getElementById("ontosearcher_defaultdiv_content");//refetch
	datatcontent.style.backgroundColor = "white";
	
	var frag = document.createDocumentFragment();
	if(!response || !response.hits){return;}

	var isodd = false;
	for( var dbname in response.hits ){
		var rowsInDb = response.hits[dbname];
		if(!rowsInDb){continue;}

		var dataUl = document.createElement("ul");
		dataUl.innerHTML = "<span class='dbname'>" + dbname + "</span>";
		frag.appendChild(dataUl);
		for( var key in rowsInDb ){
			var row = rowsInDb[key];
			if(!row){continue;}
			isodd = !isodd;
			var datali = document.createElement("li");
			datali.classList.add(isodd ? "odd":"even");
			var titlestr= row.keywords ? row.keywords.join(",") : "";

			var targurl;
			if(this.usewrapper){
				targurl = _self.targetBase + "/wrapper/" + dbname +"/" + row.id;
			}else{
				targurl = row.url;
			}
//			var linkstr = "<a href='" + targurl + "' target='_blank' title='" + titlestr + "'>" + row.name + "</a>";
			var linkstr = "<a class='ontosearcher linka' onclick='_OntoSearcher_onAclick(\"" + targurl + "\");' target='_blank' title='" + titlestr + "'>" + row.name + "</a>";
			datali.innerHTML = linkstr;

			dataUl.appendChild(datali);
		}
	}
	datatcontent.appendChild(frag);
	var closelink =  document.createElement("a")
	closelink.innerHTML = "close";
	closelink.classList.add("closelink");
	closelink.id = "ontosearcher_defaultdiv_closelink";
	datatcontent.appendChild(closelink);

	newDiv.style.display = "block";
	var me=this;
//	setTimeout(function(){
		var newDiv = document.getElementById("ontosearcher_defaultdiv");
		var windowWidth = (document.documentElement.clientWidth||window.innerWidth||0);
		var windowHeight = (document.documentElement.clientHeight||window.innerHeight||0);
		
		newDiv.style.top = ((windowHeight - newDiv.offsetHeight) / 2) + "px";
		newDiv.style.left = ((windowWidth - newDiv.offsetWidth) / 2) + "px";

		var headDiv = document.getElementById("ontosearcher_defaultdiv_headerparent");
		headDiv.onmousedown = function(evt){
			me.flag = true;
			evt = (evt) || window.event;
			me.clickOffsetTop = evt.clientY - newDiv.offsetTop;
			me.clickOffsetLeft = evt.clientX - newDiv.offsetLeft;
			if(!document.all){
				window.getSelection().removeAllRanges();
			}
		}
		document.onmouseup = function(){
			me.flag = false;
		}
		document.onmousemove = function(evt){
			evt = (evt) || window.event;
			if(me.flag){
				newDiv.style.top = evt.clientY - me.clickOffsetTop + 'px';
				newDiv.style.left = evt.clientX - me.clickOffsetLeft + 'px';
			}
		}
		var closebtn =  document.getElementById("ontosearcher_defaultdiv_closebtn");
		closebtn.onclick = function(){newDiv.style.display = "none";me.flag = false;};
		var closelink =  document.getElementById("ontosearcher_defaultdiv_closelink");
		closelink.onclick = function(){newDiv.style.display = "none";me.flag = false;};
		
		var datatcontent =  document.getElementById("ontosearcher_defaultdiv_content");
		var constyle = datatcontent.currentStyle || document.defaultView.getComputedStyle(datatcontent, '');
		var dialogstyle = newDiv.currentStyle || document.defaultView.getComputedStyle(newDiv, '');
		var divpad = dialogstyle.paddingTop || dialogstyle.padding;
		var conpad = constyle.paddingTop || constyle.padding;
		var _pxNum = function(sizeStr){
			if(sizeStr){
				var ret = sizeStr.toLowerCase();
				if(ret.indexOf("px", ret.length - 2) !== -1 ){
					ret = ret.substr(0 , ret.length - 2 );
					return ret * 1;
				}else{
					return 0;
				}
			}else{
				return 0;
			}
		};
		var pad = _pxNum(divpad) + _pxNum(conpad);
		datatcontent.style.height = (newDiv.clientHeight - headDiv.offsetHeight - pad * 2 ) + "px";
//	},10);
};
OntoSearcher.prototype._closedialog = function(){
	var newDiv = document.getElementById("ontosearcher_defaultdiv");
	newDiv.style.display = "none";
	return false;
};
_OntoSearcher_onAclick = function(url){
	window.open(url ,"_blank",'top=50,left=50,width=1000,height=700,scrollbars=1,location=0,menubar=0,toolbar=0,status=1,directories=0,resizable=1');
};

