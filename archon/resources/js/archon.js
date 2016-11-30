
$(document).ready(function(){
	
	var brand = $(".navbar-brand");
	var app = $(".app");
	var page = $(".page");
	var app_sel = $(".app-selector");
	var page_sel = $(".page-selector");
	var loading_page = $("#loading-page");
	var dashboard_page = $("#dashboard-page");
	
	app.hide();
	page.collapse({'toggle': false});
	dashboard_page.collapse("show");
	
	brand.click(function() {
		app.hide();
		app_sel.css("background-color", "transparent");
		page_sel.css("color", "#777");
		page.fadeOut(200);
		page.collapse("hide");
		loading_page.fadeIn(200);
		loading_page.collapse("show");
		setTimeout(function() {
			page.fadeOut(200);
			page.collapse("hide");
			dashboard_page.fadeIn(200);
			dashboard_page.collapse("show");
		}, 400);
	});
	
	app_sel.click(function(){
		var this_sel = $(this);
		app.hide();
		app_sel.css("background-color", "transparent");
		this_sel.css("background-color", "#e7e7e7");
		$(this_sel.attr("app")).show();
	});
	
	page_sel.click(function(){
		var this_sel = $(this);
		page_sel.css("color", "#777");
		this_sel.css("color", "#337ab7");
		page.fadeOut(200);
		page.collapse("hide");
		loading_page.fadeIn(200);
		loading_page.collapse("show");
		var page_target = $(this_sel.attr("page"));
		setTimeout(function() {
			page.fadeOut(200);
			page.collapse("hide");
			page_target.fadeIn(200);
			page_target.collapse("show");
		}, 400);
	});
	
});
