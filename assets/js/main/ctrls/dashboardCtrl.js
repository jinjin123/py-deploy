define(['/assets/js/main/ctrls/module.js'],function(fabric){
    fabric.controller('dashboardCtrl',['$rootScope','$scope','$http','$location', function($rootScope,$scope,$http,$location){
			var visitsChartData = [{
				label: '冰果写作系统',
				data: [
					[1, 1300],
					[2, 1600],
					[3, 1900],
					[4, 2100],
					[5, 2500],
					[6, 2200],
					[7, 2000],
					[8, 1950],
					[9, 1900],
					[10, 2000]
				]
			}, {
				// Returning Visits
				label: '冰果写作系统',
				data: [
					[1, 500],
					[2, 600],
					[3, 550],
					[4, 600],
					[5, 800],
					[6, 900],
					[7, 800],
					[8, 850],
					[9, 830],
					[10, 1000]
				],
				filledPoints: true
			}];
        $('#visits-chart').simplePlot(visitsChartData, {
				series: {
					points: {
						show: true,
						radius: 5
					},
					lines: {
						show: true
					}
				},
				xaxis: {
					tickDecimals: 2
				},
				yaxis: {
					tickSize: 1000
				}
			}, {
				height: 205,
				tooltipText: "y + ' visitors at ' + x + '.00h'"
			});

    }])
})
