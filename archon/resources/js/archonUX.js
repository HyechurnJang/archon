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

function UXChartJS(view) {
	new Chart($("#" + view.attrs.id), view.chart);
};

function UXNextUI(view) {
	(function (nx) {
		var NXUI = nx.define(nx.ui.Application, {
	        methods: {
	            start: function () {
	                var topo = new nx.graphic.Topology({
	                    adaptive: true,
	                    nodeConfig: { label: 'model.name' },
	                    linkConfig: { linkType: 'curve' },
	                    showIcon: true,
	                    showNavigation: false
	                });
	                topo.data(view.chart);
	                topo.attach(this);
	            }
	        }
	    });
	    var nxui = new NXUI();
	    nxui.container(document.getElementById(view.attrs.id));
	    nxui.start();
	})(nx);
};

sigma.classes.graph.addMethod('neighbors', function(nodeId) {
    var k,
		neighbors = {},
        index = this.allNeighborsIndex[nodeId] || {};
    for (k in index)
    	neighbors[k] = this.nodesIndex[k];
	return neighbors;
});

function UXSigmaJS(view) {
	
	setTimeout(function() {
		var s = new sigma({
			container: view.attrs.id,
			graph: view.chart,
			settings: {
				defaultNodeColor: '#ec5148',
			}
		});
		s.graph.nodes().forEach(function(n) { n.originalColor = n.color; });
		s.graph.edges().forEach(function(e) { e.originalColor = e.color; });
		s.bind('clickNode', function(event) {
			var nodeId = event.data.node.id,
				toKeep = s.graph.neighbors(nodeId);
			toKeep[nodeId] = event.data.node;
			s.graph.nodes().forEach(function(n) {
				if (toKeep[n.id]) n.color = n.originalColor;
				else n.color = '#eee';
			});
			s.graph.edges().forEach(function(e) {
				if (e.source == nodeId || e.target == nodeId) e.color = e.originalColor;
				else e.color = '#eee';
			});
			s.refresh();
		});
		s.bind('clickStage', function(event) {
			s.graph.nodes().forEach(function(n) { n.color = n.originalColor; })
			s.graph.edges().forEach(function(e) { e.color = e.originalColor; })
			s.refresh();
		});
	}, 0);
};
