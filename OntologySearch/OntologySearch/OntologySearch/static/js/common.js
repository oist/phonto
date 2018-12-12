
function ctrlEnterKey(e){
	var event = e || window.event;
	if (!event) {return null;}

	var ret = (event.ctrlKey && (13 == getKeyCode(event)|| 10 == getKeyCode(event)));
	return ret;
}

function isEnterKey(e){
	var event = e || window.event;
	if (!event) {return null;}

	var ret = (13 == getKeyCode(event)|| 10 == getKeyCode(event));
	return ret;
}

function getKeyCode(e){
	if(document.all)
		return  e.keyCode;
	else if(document.getElementById)
		return (e.keyCode)? e.keyCode: e.charCode;
	else if(document.layers)
		return  e.which;
	else
		return null;
};

/*
 * ajax request
 * URLorArg: (required)
 *           urlString or
 *          {
 *            "url":url                   (required)
 *           ,"pars":request parameter    (optional)
 *                  {
 *                  }
 *           ,"type": POST/GET/....       (optional)
 *           ,"dataType":"text"/...       (optional)
 *           ,"success":success function  (optional)
 *           ,"error":error function      (optional)
 *           ,"complete":complete function(optional)
 *          }
 *
 * follw 2 are ommited if URLorArg is {...} (optional)
 * pars: 
 * completeFnc: complete function (same as URLorArg.complete)
 */
function request(URLorArg , pars , completeFnc){

	/* modify argument */
	var ajaxType = "POST";
	var ajaxDataType = "text";
	var arg;
	var argtype = typeof URLorArg;
	if(argtype == "string"){
		arg = {};
		arg.url = URLorArg;
		arg.pars = pars;
		arg.complete = completeFnc;
	}else{
		arg = URLorArg;
		if(URLorArg.type){
			ajaxType = URLorArg.type;
		}
		if(URLorArg.dataType){
			ajaxDataType = URLorArg.dataType;
		}
	}

	if(!arg.pars){
		arg.pars = {};
	}
	arg.pars.date = (new Date()).getTime() + "_" + getRandom(1000);
	/* request */
	var me = this;
	$.ajax({
		"type": ajaxType,
		"url":  arg.url,
		"data": arg.pars,
		"dataType" :ajaxDataType,
		"success": function(responseText){
			if(arg.success){
				arg.success(responseText);
			}
		},
		"complete" : function(XMLHttpRequest, textStatus){
			if(arg.complete){
				arg.complete( XMLHttpRequest, textStatus );
			}
		},
		"error": function(XMLHttpRequest, textStatus, errorThrown){
			if(arg.error){
				arg.error(XMLHttpRequest, textStatus, errorThrown);
			}
		}
	});
}

/*
 * generate random value
 */
function getRandom(maxint){
	if(maxint){
		return Math.floor( Math.random() * maxint);
	}else{
		return Math.random();
	}

};

/*_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
 * JsonData -> String(json-translatable)
 *_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/*/
function toJSONString(data){
  if (data === undefined) return;
  if (data === null) return "null";
  var type = typeof data;
  if (type == 'number' || type == 'boolean') {
    return data.toString();
  } else if (type == 'function' || type == 'unknown') {
    return;
  } else if (type == 'string' || data.constructor == String) {
    return '"' + data.replace(/\"|\n|\\/g, function(c){ return c == "\n" ? "\\n" : '\\' + c ;}) + '"';
  } else if (data.constructor == Date) {
    return 'new Date("' + data.toString() + '")';
  } else if (data.constructor == Array) {
    var items = [];
    for (var i = 0,dlen = data.length; i < dlen; i++) {
      var val = toJSONString(data[i]);
      if (val != undefined)
          items.push(val);
    }
    return "[" + items.join(",") + "]";
  } else if (data.constructor == Object) {
    var props = [];
    for (var k in data) {
      var val = toJSONString(data[k]);
      if (val != undefined)
          props.push(toJSONString(k) + ":" + val);
    }
    return "{" + props.join(",") + "}";
  }
};

/* _/_/_/  replace  _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/ */
function replaceAll(str, target ,dest){
	var retStr = "";
	if(str){
		retStr = str.split(target).join(dest);
	}

	return retStr;

};

function escapeHTML(html) {
	return $('<div>').text(html).html();
}
function escapeHTML_sq(html) {
	var ret = $('<div>').text(html).html();
	ret = replaceAll(ret , "'","\'");
	return ret;
}

function toCenter(id){
	var w = $("#" + id).width();
	var h = $("#" + id).height();

	var ww = window.innerWidth;
	var wh = window.innerHeight;

	var top  = ww/2 - w/2;
	var left = wh/2 - h/2;
	
	$("#" + id).css("top",top +"px");
	$("#" + id).css("left",left +"px");
}

/*
* alert Dialog
* args:{
*        "msg":message
*       ,"okFunction":after function
*      }
* needs "#alertdialog" , "#alertmsg" @html
*/
function alertDialog(args){
	$("#alertdialog").dialog( "close" )
	                 .dialog("destroy");
	$("#alertmsg").html(args.msg);

	$("#alertdialog")
	.dialog({
		 modal: true
		,buttons: [
			{
				text: "OK",
				click: function() {
					if(args && args.okFunction){
						args.okFunction(this);
					}
					$( this ).dialog( "close" );
				}
			}
		 ]
	});
//	$( "#alertdialog" ).dialog( "open" );
}
/*
* confirm Dialog
* args:{
*        "msg":message
*       ,"okFunction":after [OK] function
*       ,"cancelFunction":after [Cancel] function
*      }
* needs "#alertdialog" , "#alertmsg" @html
*/
function confirmDialog(args){
	$("#alertdialog").dialog( "close" )
	                 .dialog("destroy");
	$("#alertmsg").html(args.msg);

	$("#alertdialog")
	.dialog({
		 modal: true
		,buttons: [
			{
				text: "OK",
				click: function() {
					if(args && args.okFunction){
						args.okFunction(this);
					}
					$( this ).dialog( "close" );
				}
			},
			{
				text: "Cancel",
				click: function() {
					if(args && args.cancelFunction){
						args.cancelFunction(this);
					}
					$( this ).dialog( "close" );
				}
			}
		 ]
	});
}


/*
* selector: selector of target
* args: {
*          "header": class of header
*        , "closer": class of closebtn
*       }
*/
function titleDraggable(selector , args){
	var me = this;
	$(selector).each(function(i) {
		var target = this;
		var data = {};

		$(target).disableSelection();
		$("input" , target)
//		.bind('mousedown.ui-disableSelection selectstart.ui-disableSelection', function(e) {
		.bind('mousedown selectstart', function(e) {
			  e.stopImmediatePropagation();
		});

		var myargs;
		if(!args){
			myargs = {};
		}else{
			myargs = args;
		}

		// header
		var selHeader = "titledraggableheader";
		if(myargs && myargs.header){
			selHeader = myargs.header;
		}
		myargs.selHeader = selHeader;

		var selCloser = "titledraggablecloser";
		if(myargs && myargs.closer){
			selCloser = args.selCloser;
		}
		myargs.selCloser = selCloser;
		me.args = myargs;

		// header
		$("." + selHeader , this ).each(function(j){
			var header = this;
			$(header).css("cursor","default");
			if(header){
				header.onmousedown = function(event){
					if($(event.target).hasClass(me.args.selCloser)){
					}else{
						event.preventDefault();
						event.stopPropagation();
						data.onDrag = true;
						data.startMX = event.pageX || event.clientX;
						data.startMY = event.pageY || event.clientY;
						var dlgoffset = $(target).offset();
						data.startX = dlgoffset.left;
						data.startY = dlgoffset.top;
						var mask = new titleDraggable_mask(target, data);
					}
				};
			}
		});

		// closer
		var closer = $("." + selCloser , this );
		if(closer){
			closer
				.unbind()
				.click(function(){
					$(target).hide();
				 })
		}
		
	});
}
/*
*   target : 
*   data   : {
*                     "startX":
*                    ,"startY":
*                    ,"startMX":
*                    ,"startMY":
*                    ,"onDrag":
*            }
*/
var titleDraggable_mask = function(target, data){
	this.target = target;
	this.data = data;
	this.mask;
	var maskobj = document.getElementById("titleDraggableMask");
	if(!maskobj){
		$(target).after("<div id='titleDraggableMask'></div>");
	}else{
		$(maskobj).show();
	}
	maskobj = $("#titleDraggableMask");
	this.mask = maskobj;
	var me = this;
	maskobj.css({
			 "position":"absolute"
			,"zIndex":1000
			,"top":"0px"
			,"left":"0px"
			,"width":"100%"
			,"height":"100%"
			,"background":"rgba(255,255,255,0.01)"
			,"cursor":"default"
		 })
		.unbind('mouseup')
		.unbind('mouseleave')
		.unbind('mousemove')
		.mouseup(function(event){
			maskobj.hide();
		 })
		.mouseleave(function(event){
			maskobj.hide();
		 })
		.mousemove(function(event){
			if(data.onDrag){
				var curX = event.pageX || event.clientX;
				var curY = event.pageY || event.clientY;
				var setLeft = data.startX + (curX - data.startMX);
				var setTop  = data.startY + (curY - data.startMY);

				$(target).css("left", setLeft);
				$(target).css("top", setTop);
			}
		 })
		;
};
var tdmproto = titleDraggable_mask.prototype;

/* should be in ready */
function pretendButtons(){
	$(".pretend_btn")
		.unbind("mousedown")
		.unbind("mouseup")
		.unbind("mouseout")
		.mousedown(function(event){
			event.preventDefault();
			event.stopPropagation();
			$(this).addClass("mdown");
		})
		.mouseup(function(event){
			$(this).removeClass("mdown");
		})
		.mouseout(function(event){
			$(this).removeClass("mdown");
		})
}
