sampleadmin = {
	table : null ,
	keywordtable : null ,
	targetModel:null,
	targetModelKeywords:null,//map
	articlefile:null,
	datatableinitparam:{
		 "scrollY": "400px"
		,"scrollCollapse": true
		,"paging": false
		,"dom": '<"toolbar">frtip'
		,"destroy": true
		,"deferRender": true
		,"columnDefs": [
			 { "width": "20%", "targets": 0 }
			,{ "width": "20px", "targets": 3 }
		 ]
	},
	modelscrolling : false,
	creatingmodel : false,
//// initialize functions //////////////////////////////////////////////////////
	initTable : function (newInnerBody){
		//datatable
		if($.fn.dataTable.isDataTable("#pooledmodeltable" ) ){
			var bkstr = $("#pooledmodeltbody").html();
			this.table.off("click")
			.off("mouseenter")
			.off("mouseleave")
			.destroy();

			if(newInnerBody){
				$("#pooledmodeltbody").html(newInnerBody);
			}else{
				$("#pooledmodeltbody").html(bkstr);
			}
		}

		/* dataTable initialize */
		this.setDatatables();
		var me = this;
		setTimeout(function(){me.setDatatables();},10);
		
	},
	setDatatables:function(){
		var me = this;
		this.table = $("#pooledmodeltable").DataTable(me.datatableinitparam)
		.on("click", "td", function () {
			if($(this).hasClass("delmodelbtn")){
				//delete keyword
				me.deletemodel( this.parentNode);
			}else{
				me.openModelDlg(this.parentNode);
			}
		})
		//adjust Z-index
		var tblZ = $(this.table).zIndex();
		$(".draggableframe").zIndex(tblZ + 1 );
		
		$(".colmodelid").width($("#headmodelid").width());
		$(".colmodelname").width($("#headmodelname").width());
		$("#whole .dataTables_scrollBody").height("400px");

	},
	//get dblist
	setdblist : function (msg){
		var res={};
		eval("res=" + msg.responseText);

		if(!res || !res.payload || !res.payload.dblist){return;}

		$("#targetdb").html("");
		var optstr = "";

		var dbs = res.payload.dblist;
		for(var i=0,len = dbs.length;i<len;i++){
			var row = dbs[i];
			optstr +="<option value='" + row +"'>" + row + "</option>";
		}
		$("#targetdb").html(optstr);
		$("#targetdb").val("testdb");

	},
	reset : function(){
		location.reload();
	},
//// initialize functions end //////////////////////////////////////////////////

//// auth //////////////////////////////////////////////////////////////////////
	//get token
	gettoken : function (){
		$("#testres").html("");

		var uname = $("#username").val();
		var pwd = MD5_hexhash($("#userpass").val())
		var targ = $("#targetdb").val();
		$("#usernameview").text(uname);
		$("#targetdbview").text(targ);

		var param = {
				  "username": uname
				 ,"password": pwd
				 ,"dbname": targ
		};
		authval = param;
		var me = this;
		request({
			 "url"     :"apps/gettoken"
			,"pars"    :param
			,"type"    :"POST"
			,"complete":function(msg){
				me.aftertoken(msg)
			 }
		});
	},

	// after auth
	aftertoken : function (msg){
		var res={};
		eval("res=" + msg.responseText);

		var result={};
		if(res && res.payload){
			result= res.payload;
		}

		if(result.token){
			authval.token = result.token;
			this.getModellist(true);
			this.getDBinfo();
		}else{
			authval={};
			alertDialog({
				"msg" : "This user is not authorized."
			});
		}
	},
	
//// auth end //////////////////////////////////////////////////////////////////

//// show models ///////////////////////////////////////////////////////////////
	getModellist : function (refresh){
		var modellisturl = "apps/modellist/" + authval.dbname + "/" + authval.token;
		var me = this;
		request({
			 "url"     :modellisturl
			,"complete":function(msg){
				me.afterModellist(msg , refresh);
			 }
		});
	},

	// set model table & csv
	afterModellist : function (msg , refresh){
		$("#pooledmodeltbody").html("");
		$("#modelarea").val("");
		$("#keywordarea").val("");

		var res={};
		eval("res=" + msg.responseText);

		var result={};
		if(res && res.payload){
			result= res.payload;
		}

		$(".authinput").hide();
		$(".authview").show();

		if(!result.models){return;}

		var tablestr = "";
		var modelcsv = "";
		var keycsv = "";
		var cnt = 0;
		for(var key in result.models){
			var row = result.models[key];
			if(!row){continue;}

			cnt++;
			var rowclass = (cnt % 2)?"odd":"even";
			tablestr +="<tr class='" + rowclass + "'>";
			tablestr +="<td>" + row.modelid + "</td>";
			tablestr +="<td>" + row.name + "</td>";

			modelcsv += row.modelid + "," + row.name + "\n";

			var keystr = "";
			if(row.keywords && row.keywords.length){
				var first = true;
				for(var keykey in row.keywords){
					var rowkey = row.keywords[keykey];
					if(!rowkey){continue;}

					if(!first){
						keystr +="<br>";
					}else{
						first = false;
					}
					keystr += rowkey.keyword ;

					keycsv += row.modelid + "," + rowkey.keyword + "\n";
				}
			}

			tablestr += "<td>" + keystr + "</td>";
			tablestr += "<td class='delmodelbtn' title='delete this model' style='text-align:center;'>X</td></tr>";
			tablestr += "</tr>";

		}

		$("#pooledmodeltbody").html(tablestr);
		$("#modelarea").val(modelcsv);
		$("#keywordarea").val(keycsv);

		var me = this;
		if(refresh){
			me.initTable(tablestr);
		}

	},
//// show models end ///////////////////////////////////////////////////////////

//// update all data by csv ////////////////////////////////////////////////////

	openCsvDlg : function (){
		showdiv('modelcsv');
		toCenter('modelcsv');
		
	},
	// update by csv
	updatemodels : function (){
		var param = $.extend({}, authval);
		param.modellist = $("#modelarea").val();
		param.keywordlist = $("#keywordarea").val();
		var me = this;
		request({
			 "url"     :"apps/updatebycsv"
			,"pars"    :param
			,"type"    :"POST"
			,"complete":function(msg){
				me.getModellist();
				hidediv('modelcsv');
			 }
		});
	},
//// update all data by csv end ////////////////////////////////////////////////

//// open model dialog /////////////////////////////////////////////////////////
	create : function(){
		this.openModelDlg(null, true);
	},
	openModelDlg : function(tablerow , iscreate){
		if(iscreate){
			this.creatingmodel = true;
			$("#modeldlg_id").text("");
			$("#modeldlg_txtid").val("");
			$("#modeldlg_txtname").val("");
			$("#modeldlg_keywordarea").val("");
			this.targetModelKeywords = {};
			this.targetModel = {
				 "id"   : ""
				,"name" : ""
			};
		}else{
			this.creatingmodel = false;
			var id   = $("td", tablerow).eq(0).text();
			var name = $("td", tablerow).eq(1).text();
			this.targetModel = {
				 "id"   : id
				,"name" : name
			};

			// initialize data
			var keywords = $("td", tablerow).eq(2).html();
			var keywordsarr = keywords.split('<br>');
			this.targetModelKeywords = {};
			if(keywordsarr){
				for (var i=0,len = keywordsarr.length ; i<len ; i++){
					var row = keywordsarr[i];
					if(!row){continue;}
					this.targetModelKeywords[row] = row;
				}
			}

			$("#modeldlg_id").text(id);
			$("#modeldlg_txtid").val(id);
			$("#modeldlg_txtname").val(name);
			$("#modeldlg_keywordarea").val(keywordsarr.join('\n'));

		}

		$("#modeldlg").show();
		if(iscreate){
			$("#modeldlg .new_model").show();
			$("#modeldlg .mod_model").hide();
			$("#modeldlg_upmodel").attr("disabled", "disabled");

		}else{
			$("#modeldlg .new_model").hide();
			$("#modeldlg .mod_model").show();
			$("#modeldlg_upmodel").removeAttr("disabled", "disabled");
		}
		toCenter('modeldlg');

		this.initKeywordtable();

	},
	validateUpmodel : function(){
		if($("#modeldlg_txtid").val() && $("#modeldlg_txtname").val() ){
			$("#modeldlg_upmodel").removeAttr("disabled");
		}else{
			$("#modeldlg_upmodel").attr("disabled", "disabled");
		}
	},
	initKeywordtable:function(){
		if(!this.targetModel){return;}

		var keywordsarr = this.targetModelKeywords;
		var id =   this.targetModel.id;
		var name = this.targetModel.name;
		//adjust data
		var strTBody = "";
		for (var row in this.targetModelKeywords) {
			if(!row){continue;}

			strTBody += "<tr><td>";
			strTBody += row;
			strTBody += "</td>";
			strTBody += "<td class='delkeywordbtn' title='delete this keyword' style='text-align:center;'>X</td></tr>";
		}

		//destroy keyword table
		$("#keywordtbody").html("");
		if($.fn.dataTable.isDataTable("#keywordtable" ) ){
			this.table.off("click")
			.off("mouseenter")
			.off("mouseleave")
			.destroy();
		}
		$("#keywordtbody").unbind();

		$("#keywordtbody").html(strTBody);

		/* dataTable initialize */
		var me = this;
		this.table = $("#keywordtable").DataTable({
			 "scrollY": "200px"
			,"scrollCollapse": true
			,"paging": false
			,"dom": '<"toolbar">frtip'
			,"columnDefs":[{ "width": "20px", "targets": 1 }]
			, scroller: true
		})
		.on("click", "td", function () {
			if($(this).hasClass("delkeywordbtn")){
				//delete keyword
				var keywd = $("td", this.parentNode).eq(0).text();
				delete me.targetModelKeywords[keywd];
				me.initKeywordtable();
			}
		});
	},
	// add keyword
	addKeyword : function (){
		var newKeyword = $("#newkeyword").val();
		if(!newKeyword){return;}

		this.targetModelKeywords[newKeyword] = newKeyword;
		this.initKeywordtable();
		$("#newkeyword").val("");
	},
//// open model dialog end /////////////////////////////////////////////////////

//// update model for each /////////////////////////////////////////////////////

	// update for 1model
	updatemodel : function (){
		var me = this;
		var keyArr = [];
		for(var keykey in me.targetModelKeywords){
			if(!keykey){continue;}
			keyArr.push(keykey);
		}
		
		var param = $.extend({
			 "modelid":$("#modeldlg_txtid").val()
			,"modelname":$("#modeldlg_txtname").val()
			,"keyword": keyArr
		}, authval);

		request({
			 "url"     :"apps/updatemodelandkeyword"
			,"pars"    :param
			,"type"    :"POST"
			,"complete":function(msg){
				me.afterUpdatemodel(msg)
			 }
		});
	},
	afterUpdatemodel: function(msg){
		var res={};
		eval("res=" + msg.responseText);

		var result={};
		if(res && res.payload){
			result= res.payload;

			this.getModellist();

			hidediv('modeldlg');
		}
	},

	// delete 1model
	deletemodel : function (tablerow){

		var me = this;
		confirmDialog({
			 "msg" : "Are you sure to delete this model?"
			,"okFunction":function(dialog){
				me.deleteModelContents(tablerow);
			}
		});
	},
	deleteModelContents : function (tablerow){
		var me = this;
		var modelid = $("td", tablerow).eq(0).text();

		var targetUrl = "apps/deletemodel/" + authval.dbname + "/" + modelid  + "/" + authval.token;

		request({
			 "url"     :targetUrl
			,"pars"    :{}
			,"type"    :"POST"
			,"complete":function(msg){
				me.afterDeletemodel(msg)
			 }
		});
	},
	afterDeletemodel: function(msg){
		var res={};
		eval("res=" + msg.responseText);

		var result={};
		if(res && res.payload){
			result= res.payload;

			this.getModellist();
		}
	},
//// update model for each end /////////////////////////////////////////////////

//// file upload ///////////////////////////////////////////////////////////////
	articleOnChange:function(){
		if (!$("#file_article").val()) {
			return;
		}

		var me = this;
		confirmDialog({
			 "msg" : "It takes a few minutes.<br>Are you ready?"
			,"okFunction":function(dialog){
				me.articleUpload();
			}
			,"cancelFunction":function(dialog){
				$("#articlediv").html("");
				$("#articlediv").html(defaultArticleDevHtml);
			}
		});
	},
	articleUpload:function(){

		var fd = new FormData();
		if ($("#file_article").val()!== '') {
			var fi = $("#file_article").prop("files")[0];
			fd.append( "file", fi );
		}
		fd.append("username" , authval.username);
		fd.append("password" , authval.password);
		fd.append("dbname"   , authval.dbname);
		fd.append("token"    , authval.token);
		fd.append("csrfmiddlewaretoken" , defaulttoken);

		var postData = {
			type : "POST",
			dataType : "json",
			data : fd,
			processData : false,
			contentType : false
		};
		var me = this;
		$("#maskdiv").show();
		$.ajax(
			"keywordlist/getkeyfromarticle", postData
		).done(function( msg ){
			$.ajaxSetup( {data: {
			    csrfmiddlewaretoken: defaulttoken
			}});

			me.afterUpload(msg);

		});
	},
	afterUpload : function(res){

		if(res && res.payload && res.payload.keyword && res.payload.keyword.length){
			var keys = res.payload.keyword;
			var gotkeysmap = {};
			//adjust got keyword
			for (var i=0,len = keys.length ; i<len ; i++){
				var row = keys[i];
				if(!row){continue;}
				gotkeysmap[row]= row;
			}
			var adjkeys = [];
			for (var key in gotkeysmap){
				adjkeys.push(key);
			}
			var gotkeys = adjkeys.length;

			//add keyword
			var addkeys = 0;
			for (var i=0,len = keys.length ; i<len ; i++){
				var row = keys[i];
				if(!row){continue;}
				if(!this.targetModelKeywords[row]){
					addkeys++;
				}
				this.targetModelKeywords[row] = row;
			}
			this.initKeywordtable();
			$("#newkeyword").val("");
		}

		$("#articlediv").html("");
		$("#articlediv").html(defaultArticleDevHtml);
		$("#maskdiv").hide();
		alertDialog({
			"msg": gotkeys + " keywords found , " + addkeys + " keywords added."
		});
	},
//// file upload end ///////////////////////////////////////////////////////////

//// target DB info ////////////////////////////////////////////////////////////
	getDBinfo : function(){
		var me = this;
		
		var targetUrl = "apps/getdbinfo/" + authval.dbname + "/" + authval.token;

		request({
			 "url"     :targetUrl
			,"pars"    :{}
			,"type"    :"POST"
			,"complete":function(msg){
				me.afterGetDBinfo(msg)
			 }
		});
		
	},
	afterGetDBinfo : function(msg){
		var res={};
		eval("res=" + msg.responseText);

		if(res && res.payload && res.payload.dbinfo){
			var resinfo = res.payload.dbinfo;
			$("#url_tempate").val(resinfo.urlformat); 
		}
	},
	updateDBInfo : function(){
		var me = this;
		
		var param = $.extend({
			 "urlformat":$("#url_tempate").val()
		}, authval);

		request({
			 "url"     :"apps/updatedbinfo"
			,"pars"    :param
			,"type"    :"POST"
			,"complete":function(msg){
				me.getDBinfo();
			 }
		});
	}
//// target DB info end ////////////////////////////////////////////////////////
};
