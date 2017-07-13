function UXDataTableBasic(view) {
	$("#" + view.attrs.ID).DataTable({
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
        order: view.options.order,
        destroy: true
	});
};

function UXDataTableAsync(view) {
	$("#" + view.attrs.ID).DataTable({
		ajax: view.attrs.url,
		searchDelay: 1000,
		processing: true,
		serverSide: true,
		scrollX: false,
    	dom: 'Bfrtip',
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 rows', '25 rows', '50 rows', 'Show all' ]
        ],
        buttons: [
        	{extend:'pageLength', text:'<i class="fa fa-align-justify"></i>', titleAttr:'Rows'},
            {extend:'colvis', text:'<i class="fa fa-th-list"></i>', titleAttr:'Cols'},
        ],
        search: { "regex": false },
        destroy: true
    });
};

function UXFooTable(view) {
	$("#" + view.attrs.ID).footable();
};

function UXFlipClock(view) {
	$("#" + view.attrs.ID).FlipClock({clockFace: 'TwentyFourHourClock'});
}

function UXJustgage(view) {
	setTimeout(function() {
		running_alloc.push(new JustGage({
			id: view.attrs.ID,
			title: view.chart.title,
		    value: view.chart.value,
		    min: view.chart.min,
		    max: view.chart.max,
		    pointer: true,
		    pointerOptions: {
		    	toplength: -15,
		    	bottomlength: 10,
		    	bottomwidth: 12,
		    	color: '#8e8e93',
		    	stroke: '#ffffff',
		    	stroke_width: 3,
		    	stroke_linecap: 'round'
	        },
	        startAnimationTime: 0,
	        refreshAnimationTime: 0,
		}));
	}, 0);
};

function UXDimple(view) {
	var width = view.chart.options.width;
    var height = view.chart.options.height;
    var margin = view.chart.options.margin;
    if (width == null) { width = "100%"; }
    if (height == null) { height = "100%"; }
    var svg = dimple.newSvg("#" + view.attrs.ID, width, height);
    var chart = new dimple.chart(svg);
    running_alloc.push(svg);
    running_alloc.push(chart);
    
    chart.setMargins(margin[0], margin[1], margin[2], margin[3]);//"30px", "20px", "20px", "20px");
    
    var xAxis = null;
    var yAxis = null;
    
    switch (view.chart.type) {
    case "line":
    	if (view.chart.options.pivot == true) {
    		xAxis = chart.addMeasureAxis("x", view.chart.options.ykey);
    		yAxis = chart.addCategoryAxis("y", view.chart.options.xkey);
    	} else {
    		xAxis = chart.addCategoryAxis("x", view.chart.options.xkey);
    		yAxis = chart.addMeasureAxis("y", view.chart.options.ykey);
    	}
    	break;
    case "bar":
    	if (view.chart.options.pivot == true) {
    		if (view.chart.options.stack == true) {
    			xAxis = chart.addMeasureAxis("x", view.chart.options.ykey);
        		yAxis = chart.addCategoryAxis("y", view.chart.options.xkey);
    		} else {
    			xAxis = chart.addMeasureAxis("x", view.chart.options.ykey);
        		yAxis = chart.addCategoryAxis("y", [view.chart.options.xkey, "series"]);
    		}
    	} else {
    		if (view.chart.options.stack == true) {
    			xAxis = chart.addCategoryAxis("x", view.chart.options.xkey);
        		yAxis = chart.addMeasureAxis("y", view.chart.options.ykey);
    		} else {
    			xAxis = chart.addCategoryAxis("x", [view.chart.options.xkey, "series"]);
        		yAxis = chart.addMeasureAxis("y", view.chart.options.ykey);
    		}
    	}
    	break;
    case "pie":
    case "donut":
    	chart.addMeasureAxis("p", view.chart.options.ykey);
    	break;
    };
    
    switch (view.chart.type) {
    case "line":
    case "bar":
    	if (view.chart.options.pivot == true) {
    		if (view.chart.options.min != null) { xAxis.overrideMin = view.chart.options.min; }
            if (view.chart.options.max != null) { xAxis.overrideMax = view.chart.options.max; }
    		if (view.chart.options.xaxis == false) { yAxis.hidden = true; }
            if (view.chart.options.yaxis == false) { xAxis.hidden = true; }
            switch (view.chart.options.order) {
        	case 0: yAxis.addOrderRule(view.chart.labels.reverse()); break;
        	case 1: yAxis.addOrderRule(view.chart.options.ykey); break;
        	case 2: break;
        	}
    	} else {
    		if (view.chart.options.min != null) { yAxis.overrideMin = view.chart.options.min; }
            if (view.chart.options.max != null) { yAxis.overrideMax = view.chart.options.max; }
    		if (view.chart.options.xaxis == false) { xAxis.hidden = true; }
            if (view.chart.options.yaxis == false) { yAxis.hidden = true; }
            switch (view.chart.options.order) {
        	case 0: xAxis.addOrderRule(view.chart.labels); break;
        	case 1: xAxis.addOrderRule(view.chart.options.ykey); break;
        	case 2: break;
        	}
    	}
    	xAxis.title = null;
        yAxis.title = null;
        break;
    }
    
    switch (view.chart.options.color) {
    case "A": break;
    case "H":
    case "U":
    	chart.addColorAxis(view.chart.options.ykey, ["rgba(" + view.chart.options.min_r + "," + view.chart.options.min_g + ",0,0.8)", "rgba(" + view.chart.options.max_r + "," + view.chart.options.max_g + ",0,0.8)"]);
    	break;
    default:
    	chart.addColorAxis(view.chart.options.ykey, view.chart.options.color);
    	break;
    }
    
    if (view.chart.options.legend == true) {
    	chart.addLegend("30px", 0, "100%", "30px", "left");
    }
    
    switch (view.chart.type) {
    case "line":
    	for (var i=0, series; series=view.chart.series[i]; i++) {
    		var s = chart.addSeries(series.series, dimple.plot.line);
    		s.data = series.datasets;
    		s.lineMarkers = true;
    		if (view.chart.options.tooltip == true) { s.tooltipFontSize = "12px"; }
    		else {
    			s.addEventHandler("mouseover", null);
    			s.addEventHandler("mouseleave", null);
    		}
    	}
    	break;
    case "bar":
		var s = chart.addSeries("series", dimple.plot.bar);
    	s.data = view.chart.series;
    	if (view.chart.options.tooltip == true) { s.tooltipFontSize = "12px"; }
		else {
			s.addEventHandler("mouseover", function (e) {});
			s.addEventHandler("mouseleave", function (e) {});
		}
    	break;
    case "pie":
    	for (var i=0, series; series=view.chart.series[i]; i++) {
    		var s = chart.addSeries(view.chart.options.xkey, dimple.plot.pie);
    		s.data = series.datasets;
    		if (view.chart.options.tooltip == true) { s.tooltipFontSize = "12px"; }
    		else {
    			s.addEventHandler("mouseover", null);
    			s.addEventHandler("mouseleave", null);
    		}
    	}
    	break;
    case "donut":
    	var size = 0;
    	var sub_size = view.chart.options.size;
    	for (var i=0, series; series=view.chart.series[i]; i++) {
    		var s = chart.addSeries(view.chart.options.xkey, dimple.plot.pie);
    		s.outerRadius = size;
    		size = size - sub_size;
    		s.innerRadius = size;
    		size = size - sub_size;
    		s.data = series.datasets;
    		if (view.chart.options.tooltip == true) { s.tooltipFontSize = "12px"; }
    		else {
    			s.addEventHandler("mouseover", null);
    			s.addEventHandler("mouseleave", null);
    		}
    	}
    	break;
    }
	
	setTimeout(function() {
	    chart.draw();
	}, 0);
};

function UXPeity(view) {
	switch(view.figure.type) {
	case "line":
		switch (view.figure.color) {
	    case "A": break;
	    case "H":
	    	view.figure.options.fill = "rgb(" + parseInt(255 - ((view.figure.cval * 255) / 100)) + "," + parseInt((view.figure.cval * 255) / 100) + ",0)";
	    	view.figure.options.stroke = "rgb(" + parseInt(255 - ((view.figure.cval * 255) / 100)) + "," + parseInt((view.figure.cval * 255) / 100) + ",0)";
	    	break;
	    case "U":
	    	view.figure.options.fill = "rgb(" + parseInt((view.figure.cval * 255) / 100) + "," + parseInt(255 - ((view.figure.cval * 255) / 100)) + ",0)";
	    	view.figure.options.stroke = "rgb(" + parseInt((view.figure.cval * 255) / 100) + "," + parseInt(255 - ((view.figure.cval * 255) / 100)) + ",0)";
	    	break;
	    default:
	    	view.figure.options.fill = view.figure.color;
	    	view.figure.options.stroke = view.figure.color;
	    	break;
	    }
		$("#" + view.attrs.ID).peity("line", view.figure.options);
		break;
	case "bar":
		switch (view.figure.color) {
	    case "A": break;
	    case "H":
	    	view.figure.options.fill = function(value) { return "rgb(" + parseInt(255 - ((value * 255) / 100)) + "," + parseInt((value * 255) / 100) + ",0)"; };
	    	break;
	    case "U":
	    	view.figure.options.fill = function(value) { return "rgb(" + parseInt((value * 255) / 100) + "," + parseInt(255 - ((value * 255) / 100)) + ",0)"; };
	    	break;
	    default:
	    	view.figure.options.fill = view.figure.color;
	    	break;
	    }
		$("#" + view.attrs.ID).peity("bar", view.figure.options);
		break;
	case "pie":
		switch (view.figure.color) {
	    case "A": break;
	    case "H":
	    	view.figure.options.fill = ["rgb(" + parseInt(255 - ((view.figure.cval * 255) / 100)) + "," + parseInt((view.figure.cval * 255) / 100) + ",0)", "#eee"];
	    	break;
	    case "U":
	    	view.figure.options.fill = ["rgb(" + parseInt((view.figure.cval * 255) / 100) + "," + parseInt(255 - ((view.figure.cval * 255) / 100)) + ",0)", "#eee"];
	    	break;
	    default:
	    	view.figure.options.fill = [view.figure.color, "#eee"];
	    	break;
	    }
		$("#" + view.attrs.ID).peity("pie", view.figure.options);
		break;
	case "donut":
		switch (view.figure.color) {
	    case "A": break;
	    case "H":
	    	view.figure.options.fill = ["rgb(" + parseInt(255 - ((view.figure.cval * 255) / 100)) + "," + parseInt((view.figure.cval * 255) / 100) + ",0)", "#eee"];
	    	break;
	    case "U":
	    	view.figure.options.fill = ["rgb(" + parseInt((view.figure.cval * 255) / 100) + "," + parseInt(255 - ((view.figure.cval * 255) / 100)) + ",0)", "#eee"];
	    	break;
	    default:
	    	view.figure.options.fill = [view.figure.color, "#eee"];
	    	break;
	    }
		$("#" + view.attrs.ID).peity("donut", view.figure.options);
		break;
	};
};

var ArborRenderer = function(canvas){
	var canvas = $(canvas).get(0)
	var ctx = canvas.getContext("2d");
	var gfx = arbor.Graphics(canvas)
	var particleSystem = null
    var that = {
		init:function(system){
			particleSystem = system
			particleSystem.screenSize(canvas.width, canvas.height) 
			particleSystem.screenPadding(40)
			that.initMouseHandling()
		},
		redraw:function(){
			if (!particleSystem) return
			gfx.clear()
			var nodeBoxes = {}
			particleSystem.eachNode(function(node, pt){
				var label = node.data.label||""
				var w = ctx.measureText(""+label).width + 10
				if (!(""+label).match(/^[ \t]*$/)){
					pt.x = Math.floor(pt.x)
					pt.y = Math.floor(pt.y)
				}else{
					label = null
				}
				if (node.data.color) ctx.fillStyle = node.data.color
				else ctx.fillStyle = "rgba(0,0,0,.2)"
					if (node.data.color=='none') ctx.fillStyle = "white"
						if (node.data.shape=='dot'){
							gfx.oval(pt.x-w/2, pt.y-w/2, w,w, {fill:ctx.fillStyle})
							nodeBoxes[node.name] = [pt.x-w/2, pt.y-w/2, w,w]
						}else{
							gfx.rect(pt.x-w/2, pt.y-10, w,20, 4, {fill:ctx.fillStyle})
							nodeBoxes[node.name] = [pt.x-w/2, pt.y-11, w, 22]
						}
				if (label){
					ctx.font = "12px Helvetica";
					ctx.textAlign = "center";
					ctx.fillStyle = "white";
					if (node.data.color=='none') ctx.fillStyle = '#333333';
					ctx.fillText(label||"", pt.x, pt.y+4);
					ctx.fillText(label||"", pt.x, pt.y+4);
				}
			})                
			particleSystem.eachEdge(function(edge, pt1, pt2){
				var weight = edge.data.weight
				var color = edge.data.color
				if (!color || (""+color).match(/^[ \t]*$/)) color = null
				var tail = intersect_line_box(pt1, pt2, nodeBoxes[edge.source.name])
				var head = intersect_line_box(tail, pt2, nodeBoxes[edge.target.name])
				ctx.save() 
				ctx.beginPath()
				ctx.lineWidth = (!isNaN(weight)) ? parseFloat(weight) : 1;
				ctx.strokeStyle = (color) ? color : "#cccccc";
				ctx.fillStyle = null;
				ctx.moveTo(tail.x, tail.y);
				ctx.lineTo(head.x, head.y);
				ctx.stroke();
				ctx.restore();
				if (edge.data.directed){
					ctx.save()
					var wt = !isNaN(weight) ? parseFloat(weight) : 1;
					var arrowLength = 6 + wt;
					var arrowWidth = 2 + wt;
					ctx.fillStyle = (color) ? color : "#cccccc";
					ctx.translate(head.x, head.y);
					ctx.rotate(Math.atan2(head.y - tail.y, head.x - tail.x));
					ctx.clearRect(-arrowLength/2,-wt/2, arrowLength/2,wt);
					ctx.beginPath();
					ctx.moveTo(-arrowLength, arrowWidth);
					ctx.lineTo(0, 0);
					ctx.lineTo(-arrowLength, -arrowWidth);
					ctx.lineTo(-arrowLength * 0.8, -0);
					ctx.closePath();
					ctx.fill();
					ctx.restore()
				}
			})
		},
		initMouseHandling:function(){
			selected = null;
			nearest = null;
			var dragged = null;
			var oldmass = 1;
			var handler = {
					clicked:function(e){
						var pos = $(canvas).offset();
						_mouseP = arbor.Point(e.pageX-pos.left, e.pageY-pos.top);
						selected = nearest = dragged = particleSystem.nearest(_mouseP);
						if (dragged.node !== null) dragged.node.fixed = true
						$(canvas).bind('mousemove', handler.dragged);
						$(window).bind('mouseup', handler.dropped);
						return false
					},
					dragged:function(e){
						var old_nearest = nearest && nearest.node._id;
						var pos = $(canvas).offset();
						var s = arbor.Point(e.pageX-pos.left, e.pageY-pos.top);
						if (!nearest) return
						if (dragged !== null && dragged.node !== null){
							var p = particleSystem.fromScreen(s);
							dragged.node.p = p;
						}
						return false
					},
					dropped:function(e){
						if (dragged===null || dragged.node===undefined) return
						if (dragged.node !== null) dragged.node.fixed = false
						dragged.node.tempMass = 50;
						dragged = null;
						selected = null;
						$(canvas).unbind('mousemove', handler.dragged);
						$(window).unbind('mouseup', handler.dropped);
						_mouseP = null;
						return false
					}
			}
			$(canvas).mousedown(handler.clicked);
		}
	}
	var intersect_line_line = function(p1, p2, p3, p4) {
		var denom = ((p4.y - p3.y)*(p2.x - p1.x) - (p4.x - p3.x)*(p2.y - p1.y));
		if (denom === 0) return false
		var ua = ((p4.x - p3.x)*(p1.y - p3.y) - (p4.y - p3.y)*(p1.x - p3.x)) / denom;
		var ub = ((p2.x - p1.x)*(p1.y - p3.y) - (p2.y - p1.y)*(p1.x - p3.x)) / denom;
		if (ua < 0 || ua > 1 || ub < 0 || ub > 1)  return false
		return arbor.Point(p1.x + ua * (p2.x - p1.x), p1.y + ua * (p2.y - p1.y));
	}
    var intersect_line_box = function(p1, p2, boxTuple) {
    	var p3 = {x:boxTuple[0], y:boxTuple[1]};
    	var w = boxTuple[2];
    	var h = boxTuple[3];
    	var tl = {x: p3.x, y: p3.y};
    	var tr = {x: p3.x + w, y: p3.y};
    	var bl = {x: p3.x, y: p3.y + h};
    	var br = {x: p3.x + w, y: p3.y + h};
    	return intersect_line_line(p1, p2, tl, tr) ||
    		intersect_line_line(p1, p2, tr, br) ||
    		intersect_line_line(p1, p2, br, bl) ||
    		intersect_line_line(p1, p2, bl, tl) ||
    		false
	}
	return that
};

function UXArbor(view) {
	var canvas = $("#" + view.attrs.ID);
	if (view.topo.options.width == 0) { canvas.attr("width", window.innerWidth - 50); }
	else { canvas.attr("width", view.topo.options.width); }
	if (view.topo.options.height == 0) { canvas.attr("height", window.innerHeight - 200); }
	else { canvas.attr("height", view.topo.options.height); }
	var sys = arbor.ParticleSystem();
	running_alloc.push(sys);
	sys.screenSize(window.innerWidth);
	sys.parameters({gravity:true, stiffness:300});
	sys.renderer = ArborRenderer("#" + view.attrs.ID);
	setTimeout(function() {
		sys.graft(view.topo.datasets);
	}, 0);
};
