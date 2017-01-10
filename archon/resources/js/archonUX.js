function UXDataTable(view) {
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
};

function UXFooTable(view) {
	$("#" + view.attrs.id).footable();
};

function UXJustgage(view) {
	setTimeout(function() {
		var g = new JustGage({
			id: view.attrs.id,
			title: view.chart.title,
		    value: view.chart.value,
		    min: view.chart.min,
		    max: view.chart.max,
		});
	}, 250);
};

function UXDimple(view) {
	var width = view.chart.options.width;
    var height = view.chart.options.height;
    if (width == 0) { width = "100%"; }
    if (height == 0) { height = "100%"; }
    var svg = dimple.newSvg("#" + view.attrs.id, width, height);
    var chart = new dimple.chart(svg);
    chart.setMargins("30px", "20px", "20px", "20px");
    
    var xAxis = null
    switch (view.chart.type) {
    case "line":
    	xAxis = chart.addCategoryAxis("x", view.chart.options.xkey);
    	xAxis.addOrderRule(view.chart.options.xkey);
    	break;
    case "bar":
    	xAxis = chart.addCategoryAxis("x", [view.chart.options.xkey, "series"]);
    	if (view.chart.options.health == true) {
    		xAxis.addOrderRule(view.chart.options.ykey);
    	} else {
    		xAxis.addOrderRule(view.chart.options.xkey);
    	}
    	break;
    case "pie":
    case "donut":
    	pAxis = chart.addMeasureAxis("p", view.chart.options.ykey);
    	break;
    };
    switch(view.chart.type) {
    case "line":
    case "bar":
        var yAxis = chart.addMeasureAxis("y", view.chart.options.ykey);
        xAxis.title = null;
        yAxis.title = null;
        if (view.chart.options.xaxis == false) { xAxis.hidden = true;}
        if (view.chart.options.yaxis == false) { yAxis.hidden = true;}
        if (view.chart.options.min != null) { yAxis.overrideMin = view.chart.options.min; }
        if (view.chart.options.max != null) { yAxis.overrideMax = view.chart.options.max; }
        break;
    }
    
    if (view.chart.options.health == true) {
    	chart.addColorAxis(view.chart.options.ykey, ["rgb(" + view.chart.options.health_min_r + "," + view.chart.options.health_min_g + ",0)", "rgb(" + view.chart.options.health_max_r + "," + view.chart.options.health_max_g + ",0)"]);
    }
    
    switch (view.chart.type) {
    case "line":
    	for (var i=0, series; series=view.chart.series[i]; i++) {
    		var s = chart.addSeries(series.series, dimple.plot.line);
    		s.data = series.datasets;
    	    s.tooltipFontSize = "14px";
    	    s.lineMarkers = true;
    	}
    	break;
    case "bar":
    	var s = chart.addSeries("series", dimple.plot.bar);
    	s.data = view.chart.series;
    	s.tooltipFontSize = "14px";
    	break;
    case "pie":
    	for (var i=0, series; series=view.chart.series[i]; i++) {
    		var s = chart.addSeries(view.chart.options.xkey, dimple.plot.pie);
    		s.data = series.datasets;
    	    s.tooltipFontSize = "14px";
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
    	    s.tooltipFontSize = "14px";
    	}
    	break;
    }
    
    if (view.chart.options.legend == true) {
    	chart.addLegend("30px", 0, "100%", "30px", "left");
    }
	
	setTimeout(function() {
	    chart.draw();
	}, 0);
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
		if (denom === 0) return false // lines are parallel
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
	var canvas = $("#" + view.attrs.id);
	if (view.topo.options.width == 0) { canvas.attr("width", window.innerWidth - 50); }
	else { canvas.attr("width", view.topo.options.width); }
	if (view.topo.options.height == 0) { canvas.attr("height", window.innerHeight - 200); }
	else { canvas.attr("height", view.topo.options.height); }
	var sys = arbor.ParticleSystem();
	sys.screenSize(window.innerWidth);
	sys.parameters({gravity:true, stiffness:300});
	sys.renderer = ArborRenderer("#" + view.attrs.id);
	setTimeout(function() {
		sys.graft(view.topo.datasets);
	}, 0);
};
