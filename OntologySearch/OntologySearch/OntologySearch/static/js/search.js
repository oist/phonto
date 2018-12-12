searchingobj = {
	success:function(response , obj){
//		$("body,body *").css("cursor" , bkcursor);
		$("body,body *").css("cursor" , "default");

		var ele = document.getElementById("smalldata1");
		if(response.hits){
//			ele.appendChild(this.eachContent(response.hits ,true));			
			var cont = this.eachContent(response.hits ,true );
			if(cont){
				ele.appendChild(cont);							
			}
		}
		var ele = document.getElementById("smalldataParents");
		if(response.parents){
//			ele.appendChild(this.eachContent(response.parents ));			
			var cont = this.eachContent(response.parents ,true);
			if(cont){
				ele.appendChild(cont);							
			}
		}
		var ele = document.getElementById("smalldata2");
		if(response.siblings){
//			ele.appendChild(this.eachContent(response.siblings ));			
			var cont = this.eachContent(response.siblings ,true);
			if(cont){
				ele.appendChild(cont);							
			}
		}
		var ele = document.getElementById("smalldataChildren");
		if(response.children){
//			ele.appendChild(this.eachContent(response.children ));			
			var cont = this.eachContent(response.children ,true);
			if(cont){
				ele.appendChild(cont);							
			}
		}
		var ele = document.getElementById("smalldataOther");
		if(response.rels){
//			ele.appendChild(this.eachContent(response.rels ));			
			var cont = this.eachContent(response.rels ,true);
			if(cont){
				ele.appendChild(cont);							
			}
		}

//		$("#smallqlist").show();
//		$( "#smalltabs" ).tabs();	
//		this.centeringContents("smallqlist");

	}
	,eachContent(data , skipanotation ){
		var isodd = false;
		var frag = document.createDocumentFragment();
		for( var dbname in data ){
			var rowsInDb = data[dbname];
			if(!rowsInDb){continue;}
			var chkindex = gchkindexes[dbname];
			var chk = $("[id=dbchk_" + chkindex + "]:checked").val();
			if(!chk){continue;}

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
//				var linkstr = "<a href='" + row.url + "' target='_blank' title='" + titlestr + "'>" + row.name + "</a>";
//				var linkstr = "<a href='#'>" + row.name + "</a>";
				var linkstr ='<a style="cursor:pointer;" ';
				linkstr +='onclick="openDstDialog(&quot;' + row.identifier + '&quot;,&quot;' + row.name + '&quot;,&quot;' + row.url + '&quot;);return false;">';
				linkstr += row.name ;
				linkstr +="</a>";
				if(!skipanotation){
					linkstr +="<br>(" + keyword2csv(row.keyword) + ")";					
				}

				datali.innerHTML = linkstr;

				dataUl.appendChild(datali);
/*
				datali.onclick=function(){
					alert(row.url);
				};
//*/
			}
		}
		return frag;
	}
	,close:function(ID){
		if(ID){
			$("#"+ID).hide();
		}else{
			$("#smallqlist").hide();			
		}
	}
	,centeringContents : function (ID){
		var ww = $(window).width();
		var wh = $(window).height();
		var w = ww * 0.9;
//		$("#"+ ID).width(w);
		var w = $("#" + ID).width();
		var h = $("#" + ID).height();
		if(h > wh){
			h = wh - 10;
		}
		var sl = $(window).scrollLeft();
		var st = $(window).scrollTop();

		var ctop = (wh - h)/2 + st;
		var cleft = (ww - w)/2 + sl;
		$("#" + ID).offset({"left":cleft , "top":ctop});
	}
};
