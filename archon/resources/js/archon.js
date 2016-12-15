var page_current = null;

$(document).ready(function() {

	var brand = $(".navbar-brand");
	var apps = $(".app");
	var pages = $(".page");
	var dynpages = $(".dynpage");
	var app_selector = $(".app-selector");
	var page_selector = $(".page-selector");
	var loading_page = $("#loading-page");
	var subject_page = $("#subject-page");
	var dashboard_page = $("#dashboard-page");

	apps.hide();
	pages.collapse({'toggle': false});
	dashboard_page.collapse("show");
	
	brand.click(function() {
		app_selector.css("background-color", "transparent");
		page_selector.css("color", "#777");
		page_current = dashboard_page;
		apps.fadeOut(350);
		dashboard_page.fadeOut(350);
		subject_page.fadeOut(350);
		dynpages.fadeOut(350);
		dashboard_page.collapse("hide");
		subject_page.collapse("hide");
		dynpages.collapse("hide");
		loading_page.collapse("show");
		setTimeout(function() {
			loading_page.collapse("hide");
			dashboard_page.css("height", "calc(100% - 50px)");
			dashboard_page.fadeIn(350);
			dashboard_page.collapse("show");
		}, 400);
	});
	
	app_selector.click(function() {
		var selector = $(this);
		var app = $(selector.attr("app"));
		apps.hide();
		app_selector.css("background-color", "transparent");
		selector.css("background-color", "#e7e7e7");
		app.fadeIn(200);
	});
	
	page_selector.click(function() {
		var selector = $(this);
		var page = $(selector.attr("page"));
		var url = selector.attr("view");
		page_current = page;
		page_selector.css("color", "#777");
		selector.css("color", "#337ab7");
		dashboard_page.fadeOut(350);
		subject_page.fadeOut(350);
		dynpages.fadeOut(350);
		dashboard_page.collapse("hide");
		subject_page.collapse("hide");
		dynpages.collapse("hide");
		loading_page.collapse("show");
		
		setTimeout(function() {
			$.ajax({
				url : url,
				dataType : "json",
				success : function(data) {
					if ( page_current == page ) {
						$("#subject-title").html(selector.html());
						$("#subject-title").attr("onclick", "GetData('" + url + "');");
						$("#subject-menu").html(ParseViewDom(page.attr("id") + '-m-', data.menu))
						ParseViewData(data.menu);
						page.html(ParseViewDom(page.attr("id") + '-', data.page));
						ParseViewData(data.page);
						page.css("height", "calc(100% - 100px)");
						loading_page.collapse("hide");
						subject_page.fadeIn(350);
						page.fadeIn(350);
						subject_page.collapse("show");
						page.collapse("show");
					}
				},
				error : function(xhr, status, thrown) {
					window.alert(status);
					window.location.replace('/');
				}
			});
		}, 400);
		
	});
});

function GetCookie(c_name)
{
	if (document.cookie.length > 0) {
		c_start = document.cookie.indexOf(c_name + "=");
		if (c_start != -1) {
			c_start = c_start + c_name.length + 1;
			c_end = document.cookie.indexOf(";", c_start);
			if (c_end == -1) c_end = document.cookie.length;
			return unescape(document.cookie.substring(c_start,c_end));
		}
	}
	return "";
}

function GetData(url) {
	var dynpages = $(".dynpage");
	var subject_page = $("#subject-page");
	dynpages.fadeOut(350);
	dynpages.collapse("hide");
	setTimeout(function() {
		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			success : function(data) {
				$("#subject-menu").html(ParseViewDom(page_current.attr("id") + '-m-', data.menu))
				ParseViewData(data.menu);
				page_current.html(ParseViewDom(page_current.attr("id") + '-', data.page));
				ParseViewData(data.page);
				page_current.css("height", "calc(100% - 100px)");
				page_current.fadeIn(350);
				page_current.collapse("show");
			},
			error : function(xhr, status, thrown) {
				window.alert(status);
				window.location.replace('/');
			}
		});
	}, 400);
};

function PostData(uuid, url) {
	var dynpages = $(".dynpage");
	var subject_page = $("#subject-page");
	var data = {};
	$(uuid).each(function(index) {
		view = $(this);
		data[view.attr("name")] = view.val();
	});
	dynpages.fadeOut(350);
	dynpages.collapse("hide");
	setTimeout(function() {
		$.ajax({
			type: "POST",
			url: url,
			contentType: "application/json; charset=utf-8",
			headers: { "X-CSRFToken": GetCookie("csrftoken") },
			dataType: "json",
			data: JSON.stringify(data),
			success : function(data) {
				$("#subject-menu").html(ParseViewDom(page_current.attr("id") + '-m-', data.menu))
				ParseViewData(data.menu);
				page_current.html(ParseViewDom(page_current.attr("id") + '-', data.page));
				ParseViewData(data.page);
				page_current.css("height", "calc(100% - 100px)");
				page_current.fadeIn(350);
				page_current.collapse("show");
			},
			error : function(xhr, status, thrown) {
				window.alert(status);
				window.location.replace('/');
			}
		});
	}, 400);
};

function DeleteData(url) {
	var dynpages = $(".dynpage");
	var subject_page = $("#subject-page");
	dynpages.fadeOut(350);
	dynpages.collapse("hide");
	setTimeout(function() {
		$.ajax({
			type: "DELETE",
			url: url,
			dataType: "json",
			success : function(data) {
				$("#subject-menu").html(ParseViewDom(page_current.attr("id") + '-m-', data.menu))
				ParseViewData(data.menu);
				page_current.html(ParseViewDom(page_current.attr("id") + '-', data.page));
				ParseViewData(data.page);
				page_current.css("height", "calc(100% - 100px)");
				page_current.fadeIn(350);
				page_current.collapse("show");
			},
			error : function(xhr, status, thrown) {
				window.alert(status);
				window.location.replace('/');
			}
		});
	}, 400);
};

function ParseViewDom(page, view) {
	if (typeof view == "object") {
		var html = "";
		var attrs = view.attrs;
		var elements = view.elements;
		
		html += "<" + view.type;
		for ( var key in attrs) {
			html += ' ' + key + '="' + attrs[key] + '"';
		}
		html += ">";
		for (var i = 0, element; element = elements[i]; i++) {
			html += ParseViewDom(page, element);
		}
		html += "</" + view.type + ">";
		return html;
	}
	return view;
};

function ParseViewData(view) {
	if (typeof view == "object") {
		var elements = view.elements;
		for (var i = 0, element; element = elements[i]; i++) { ParseViewData(element); }
		switch(view.type) {
		case "TABLE": UXTable(view); break;
		}
	}
};

function UXTable(view) {
	if (view.attrs.lib == "datatable") {
		$("#" + view.attrs.id).DataTable({
			scrollX: false,
	    	dom: 'Bfrtip',
	        lengthMenu: [
	            [ 10, 25, 50, -1 ],
	            [ '10 rows', '25 rows', '50 rows', 'Show all' ]
	        ],
	        buttons: [
	        	{extend:'pageLength', text:'<i class="fa fa-align-justify"></i>', titleAttr:'Rows'},
	            {extend:'colvis', text:'<i class="fa fa-th-list"></i>', titleAttr:'Cols'},
	            {extend:'excelHtml5', text:'<i class="fa fa-file-excel-o"></i>', titleAttr:'Excel'},
	            {extend:'pdfHtml5', text:'<i class="fa fa-file-pdf-o"></i>', titleAttr:'PDF'},
	            {extend:'print', text:'<i class="fa fa-print"></i>', titleAttr:'Print'}
	        ],
	        search: { "regex": false },
	        destroy: true
	    });
	} else if (view.attrs.lib == "footable") {
		$("#" + view.attrs.id).footable();
	}
};
