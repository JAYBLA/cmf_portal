


(function($) {
    /* "use strict" */
	
 var dlabChartlist = function(){
	
	var screenWidth = $(window).width();
	//let draw = Chart.controllers.line.__super__.draw; //draw shadow

	
	var Balcence = function(){

		var options = {
			series: [
			{
			  data: [
				{
				  x: '2008',
				  y: [2800, 4500]
				},
				{
				  x: '2009',
				  y: [3200, 4100]
				},
				{
				  x: '2010',
				  y: [2950, 7800]
				},
				{
				  x: '2011',
				  y: [3000, 4600]
				},
				{
				  x: '2012',
				  y: [3500, 4100]
				},
				{
				  x: '2013',
				  y: [4500, 6500]
				},
				{
				  x: '2014',
				  y: [4100, 5600]
				}
			  ]
			}
		  ],
			chart: {
			height: 300,
			type: 'rangeBar',
			zoom: {
			  enabled: false
			},
			toolbar: {
				show: false,
			  },
		  },
		  colors: ['var(--primary)', '#36BDCB'],
		  plotOptions: {
			bar: {
			  isDumbbell: false,
			 
			  columnWidth: 15,
			 
			}
		  },
		  legend: {
			show: false,
			
		  },
		  fill: {
			type: 'solid',
			color:['#000']
			
		  },
		  grid: {
			xaxis: {
			  lines: {
				show: true
			  }
			},
			yaxis: {
			  lines: {
				show: false
			  }
			}
		  },
		  xaxis: {
			tickPlacement: 'on'
		  }
		  };
  
		  var chart = new ApexCharts(document.querySelector("#chart-2"), options);
		  chart.render();
	}
	var pieChart = function(){
		var options = {
			series: [60, 40],
			chart: {
			type: 'donut',
			width: '100'
		  },
		  legend: {
			show: false,
			
		  },
		  plotOptions: {
			pie: {
				offsetY: 10,
			  offsetX: 25, // Adjust the horizontal offset of the pie slices
			}
		  },
		 colors:['var(--rgba-primary-1)', 'var(--primary)'],
		  dataLabels: {
			enabled: false, // enable data labels
		  },
		  responsive: [{
			breakpoint: 480,
			options: {
			  chart: {
				width: 200
			  },
			  legend: {
				position: 'bottom'
			  }
			}
		  }]
		  };
  
		  var chart = new ApexCharts(document.querySelector("#chart"), options);
		  chart.render();


	}
	var pieChartOne = function(){
		var options = {
			series: [60, 30],
			chart: {
			type: 'donut',
			width: '100'
		  },
		  legend: {
			show: false,
			
		  },
		  plotOptions: {
			pie: {
				offsetY: 10,
			  offsetX: 25, // Adjust the horizontal offset of the pie slices
			}
		  },
		 colors:['var(--rgba-primary-1)', 'var(--primary)'],
		  dataLabels: {
			enabled: false, // enable data labels
		  },
		  responsive: [{
			breakpoint: 480,
			options: {
			  chart: {
				width: 200
			  },
			  legend: {
				position: 'bottom'
			  }
			}
		  }]
		  };
  
		  var chart = new ApexCharts(document.querySelector("#chart-1"), options);
		  chart.render();


	}
	var chartBar = function(){
		
		var options = {
			  series: [
				{
					name: 'Running',
					data: [50, 18, 90, 40, 90, 80, 60],
					//radius: 12,	
				}, 
				{
				  name: 'Cycling',
				  data: [80, 40, 55, 20, 45, 50, 80]
				}, 
				
			],
				chart: {
				type: 'bar',
				height: 300,
				
				toolbar: {
					show: false,
				},
				
			},
			plotOptions: {
			  bar: {
				horizontal: false,
				columnWidth: '20%',
				endingShape: "rounded",
				borderRadius: 3,
			  },
			  
			},
			
			states: {
			  hover: {
				filter: 'none',
			  }
			},
			colors:['var(--primary)', '#000'],
			dataLabels: {
			  enabled: false,
			},
			markers: {
		shape: "circle",
		},
		
		
			legend: {
				show: false,
				fontSize: '12px',
				labels: {
					colors: 'var(--text)',
					
					},
				markers: {
				width: 18,
				height: 18,
				strokeWidth: 10,
				strokeColor: '#fff',
				fillColors: undefined,
				radius: 12,	
				}
			},
			stroke: {
			  show: true,
			  width: 4,
			  curve: 'smooth',
			  lineCap: 'round',
			  colors: ['transparent']
			},
			grid: {
				borderColor: 'var(--border)',
				strokeDashArray: 5,
				
			},
			xaxis: {
				 position: 'bottom',
			  categories: ['Week 01', 'Week 02', 'Week 03', 'Week 04', 'Week 05','Week 06','Week 07'],
			  labels: {
			   style: {
				  colors: 'var(--text)',
				  fontSize: '13px',
				  fontFamily: 'poppins',
				  fontWeight: 100,
				  cssClass: 'apexcharts-xaxis-label',
				},
			  },
			  crosshairs: {
			  show: false,
			  }
			},
			yaxis: {
				labels: {
					offsetX:-16,
				   style: {
					  colors: 'var(--text)',
					  fontSize: '13px',
					   fontFamily: 'poppins',
					  fontWeight: 100,
					  cssClass: 'apexcharts-xaxis-label',
				  },
			  },
			},
			fill: {
				type: 'solid',
				
			}, 
			tooltip: {
			  y: {
				formatter: function (val) {
				  return "$ " + val + " thousands"
				}
			  }
			},
			};

			var chartBar1 = new ApexCharts(document.querySelector("#chartBar-3"), options);
			chartBar1.render();
	}
	
	
	var totalInvoices = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [100,300, 200, 400, 200],
				/* radius: 30,	 */
			}, 				
		],
		chart: {

			type: 'area',
			height: 70,
			width: 100,
			
			toolbar: {
				show: false,
			},
			zoom: {
				enabled: false
			},
			sparkline: {
				enabled: true
			}
			
		},
		
		colors:['var(--primary)'],
		dataLabels: {
		  enabled: false,
		},

		legend: {
			show: false,
		},
		stroke: {
		  show: true,
		  width: 3,
		  curve:'smooth',
		  colors:['var(--primary)'],
		},
		
		grid: {
			show:false,
			borderColor: '#eee',
			padding: {
				top: 0,
				right: 0,
				bottom: 0,
				left: 0

			}
		},
		states: {
                normal: {
                    filter: {
                        type: 'none',
                        value: 0
                    }
                },
                hover: {
                    filter: {
                        type: 'none',
                        value: 0
                    }
                },
                active: {
                    allowMultipleDataPointsSelection: false,
                    filter: {
                        type: 'none',
                        value: 0
                    }
                }
            },
		xaxis: {
			categories: ['Jan', 'feb', 'Mar', 'Apr', 'May','June','July','Aug'],
			axisBorder: {
				show: false,
			},
			axisTicks: {
				show: false
			},
			labels: {
				show: false,
				style: {
					fontSize: '12px',
				}
			},
			
			crosshairs: {
				show: false,
				position: 'front',
				stroke: {
					width: 1,
					dashArray: 3
				}
			},
			tooltip: {
				enabled: true,
				formatter: undefined,
				offsetY: 0,
				style: {
					fontSize: '12px',
				}
			}
		},
		yaxis: {
			show: false,
		},
		fill: {
			type: 'gradient', 
			opacity: 0.7,
			colors:'var(--primary)',
			gradient: {
				colorStops:[ 
					
					{
					  offset: 0,
					  color: 'var(--primary)',
					  opacity: .4
					},
					{
					  offset: 0.6,
					  color: 'var(--primary)',
					  opacity: .4
					},
					{
					  offset: 100,
					  color: 'white',
					  opacity: 0
					}
				  ],
			},
		},
	
		tooltip: {
			enabled:false,
			style: {
				fontSize: '12px',
			},
			y: {
				formatter: function(val) {
					return "$" + val + " thousands"
				}
			}
		}
		
		};

		var chartBar1 = new ApexCharts(document.querySelector("#totalInvoices"), options);
		chartBar1.render();
	 
	}
	var totalInvoices1 = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [100,300, 200, 400, 200],
				/* radius: 30,	 */
			}, 				
		],
		chart: {

			type: 'area',
			height: 70,
			width: 100,
			
			toolbar: {
				show: false,
			},
			zoom: {
				enabled: false
			},
			sparkline: {
				enabled: true
			}
			
		},
		
		colors:['var(--primary)'],
		dataLabels: {
		  enabled: false,
		},

		legend: {
			show: false,
		},
		stroke: {
		  show: true,
		  width: 3,
		  curve:'smooth',
		  colors:['var(--primary)'],
		},
		
		grid: {
			show:false,
			borderColor: '#eee',
			padding: {
				top: 0,
				right: 0,
				bottom: 0,
				left: 0

			}
		},
		states: {
                normal: {
                    filter: {
                        type: 'none',
                        value: 0
                    }
                },
                hover: {
                    filter: {
                        type: 'none',
                        value: 0
                    }
                },
                active: {
                    allowMultipleDataPointsSelection: false,
                    filter: {
                        type: 'none',
                        value: 0
                    }
                }
            },
		xaxis: {
			categories: ['Jan', 'feb', 'Mar', 'Apr', 'May','June','July','Aug'],
			axisBorder: {
				show: false,
			},
			axisTicks: {
				show: false
			},
			labels: {
				show: false,
				style: {
					fontSize: '12px',
				}
			},
			
			crosshairs: {
				show: false,
				position: 'front',
				stroke: {
					width: 1,
					dashArray: 3
				}
			},
			tooltip: {
				enabled: true,
				formatter: undefined,
				offsetY: 0,
				style: {
					fontSize: '12px',
				}
			}
		},
		yaxis: {
			show: false,
		},
		fill: {
			type: 'gradient', 
			opacity: 0.7,
			colors:'var(--primary)',
			gradient: {
				colorStops:[ 
					
					{
					  offset: 0,
					  color: 'var(--primary)',
					  opacity: .4
					},
					{
					  offset: 0.6,
					  color: 'var(--primary)',
					  opacity: .4
					},
					{
					  offset: 100,
					  color: 'white',
					  opacity: 0
					}
				  ],
			},
		},
	
		tooltip: {
			enabled:false,
			style: {
				fontSize: '12px',
			},
			y: {
				formatter: function(val) {
					return "$" + val + " thousands"
				}
			}
		}
		
		};

		var chartBar1 = new ApexCharts(document.querySelector("#totalInvoices-1"), options);
		chartBar1.render();
	 
	}
	var pieChart = function(){
		var options = {
			series: [60, 40],
			chart: {
			type: 'donut',
			width: '100'
		  },
		  legend: {
			show: false,
			
		  },
		  plotOptions: {
			pie: {
				offsetY: 10,
			  offsetX: 25, // Adjust the horizontal offset of the pie slices
			}
		  },
		 colors:['var(--rgba-primary-1)', 'var(--primary)'],
		  dataLabels: {
			enabled: false, // enable data labels
		  },
		  responsive: [{
			breakpoint: 480,
			options: {
			  chart: {
				width: 200
			  },
			  legend: {
				position: 'bottom'
			  }
			}
		  }]
		  };
  
		  var chart = new ApexCharts(document.querySelector("#chart"), options);
		  chart.render();


	}
	var pieChartOne = function(){
		var options = {
			series: [60, 30],
			chart: {
			type: 'donut',
			width: '100'
		  },
		  legend: {
			show: false,
			
		  },
		  plotOptions: {
			pie: {
				offsetY: 10,
			  offsetX: 25, // Adjust the horizontal offset of the pie slices
			}
		  },
		 colors:['var(--rgba-primary-1)', 'var(--primary)'],
		  dataLabels: {
			enabled: false, // enable data labels
		  },
		  responsive: [{
			breakpoint: 480,
			options: {
			  chart: {
				width: 200
			  },
			  legend: {
				position: 'bottom'
			  }
			}
		  }]
		  };
  
		  var chart = new ApexCharts(document.querySelector("#chart-1"), options);
		  chart.render();


	}
	/* Function ============ */
		return {
			init:function(){
				
			},
			load:function(){
				totalInvoices();
				chartBar();
				totalInvoices1();
				Balcence();
				pieChart ();
			
				pieChartOne();
			},
			resize:function(){	
				chartBar();
			}
		}
	
	}();

	
		
	jQuery(window).on('load',function(){
		setTimeout(function(){
			dlabChartlist.load();
		}, 1000); 
		
	});

     

})(jQuery);