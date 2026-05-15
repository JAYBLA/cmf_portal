


(function($) {
    /* "use strict" */
	
 var dlabChartlist = function(){
	
	var screenWidth = $(window).width();
	//let draw = Chart.controllers.line.__super__.draw; //draw shadow
	
	var totalInvoices = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [100,300, 200, 400, 200, 300,400,200, 100, 200, 200, 200,200, 200, 300],
				/* radius: 30,	 */
			}, 				
		],
		chart: {

			type: 'area',
			height: 70,
			width: 600,
			
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
	var unpaidinvoices = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [200,400, 200, 100, 200, 200,100,300, 100, 400, 200, 200,300, 200, 200],
				/* radius: 30,	 */
			}, 				
		],
			chart: {
			type: 'area',
			height: 70,
			width: 600,
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
		  colors:['#09BD3C'],
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
			colors:'#09BD3C',
			gradient: {
				colorStops:[ 
					
					{
					  offset: 0,
					  color: '#09BD3C',
					  opacity: .4
					},
					{
					  offset: 0.6,
					  color: '#09BD3C',
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

		var chartBar1 = new ApexCharts(document.querySelector("#unpaidinvoices"), options);
		chartBar1.render();
	 
	}
	var paidinvoices = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [200,200, 100, 400, 250, 400,100,300, 100, 200, 200, 300,200, 200, 300],
				/* radius: 30,	 */
			}, 				
		],
			chart: {
			type: 'area',
			height: 70,
			width: 600,
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
		  colors:['#FD5353'],
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
			colors:'#FD5353',
			gradient: {
				colorStops:[ 
					
					{
					  offset: 0,
					  color: '#FD5353',
					  opacity: .4
					},
					{
					  offset: 0.6,
					  color: '#FD5353',
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

		var chartBar1 = new ApexCharts(document.querySelector("#paidinvoices"), options);
		chartBar1.render();
	 
	}
	var widgetChart1 = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [500, 500, 400, 400, 600, 600, 300, 300,500, 500,700,700],
				//radius: 12,	
			}, 				
		],
			chart: {
			type: 'area',
			height: 100,
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
		
		colors:['#5a45aa'],
		dataLabels: {
		  enabled: false,
		},
		markers: {
			shape: "circle",
		},

		legend: {
			show: false,
		},
		stroke: {
		  show: true,
		  width: 3,
		  curve:'straight',
		  colors:['#5a45aa'],
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
			categories: ['Jan', 'feb', 'Mar', 'Apr', 'May', 'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',],
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
		  opacity: 1,
		  colors:'#5a45aa'
		},
		tooltip: {
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

		var chartBar1 = new ApexCharts(document.querySelector("#widgetChart1"), options);
		chartBar1.render();
	 
	}
	var widgetChart2 = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [500, 500, 300, 300, 600, 600, 400, 400,200, 200,500,500],
				//radius: 12,	
			}, 				
		],
			chart: {
			type: 'area',
			height: 100,
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
		
		colors:['#2bc155'],
		dataLabels: {
		  enabled: false,
		},
		markers: {
			shape: "circle",
		},

		legend: {
			show: false,
		},
		stroke: {
		  show: true,
		  width: 3,
		  curve:'straight',
		  colors:['#2bc155'],
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
			categories: ['Jan', 'feb', 'Mar', 'Apr', 'May', 'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',],
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
		  opacity: 1,
		  colors:'#2bc155'
		},
		tooltip: {
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

		var chartBar1 = new ApexCharts(document.querySelector("#widgetChart2"), options);
		chartBar1.render();
	}
	var widgetChart5 = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [500, 500, 400, 400, 600, 600, 300, 300,500, 500,700,700],
				//radius: 12,	
			}, 				
		],
			chart: {
			type: 'area',
			height: 100,
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
		
		colors:['#00aff1'],
		dataLabels: {
		  enabled: false,
		},
		markers: {
			shape: "circle",
		},

		legend: {
			show: false,
		},
		stroke: {
		  show: true,
		  width: 3,
		  curve:'straight',
		  colors:['#00aff1'],
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
			categories: ['Jan', 'feb', 'Mar', 'Apr', 'May', 'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',],
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
		  opacity: 1,
		  colors:'#00aff1'
		},
		tooltip: {
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

		var chartBar1 = new ApexCharts(document.querySelector("#widgetChart5"), options);
		chartBar1.render();
	}
	var widgetChart4 = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [300, 300, 400, 400, 200, 200, 400, 400,500, 500,700,700],
				//radius: 12,	
			}, 				
		],
			chart: {
			type: 'area',
			height: 100,
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
		
		colors:['#f72b50'],
		dataLabels: {
		  enabled: false,
		},
		markers: {
			shape: "circle",
		},

		legend: {
			show: false,
		},
		stroke: {
		  show: true,
		  width: 3,
		  curve:'straight',
		  colors:['#f72b50'],
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
			categories: ['Jan', 'feb', 'Mar', 'Apr', 'May', 'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',],
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
		  opacity: 1,
		  colors:'#f72b50'
		},
		tooltip: {
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

		var chartBar1 = new ApexCharts(document.querySelector("#widgetChart4"), options);
		chartBar1.render();
	}
	var invoicessent = function(){
		var options = {
		  series: [
			{
				name: 'Net Profit',
				data: [100,200, 100, 300, 250, 400,100,300, 100, 400, 100, 300,400, 200, 400],
				/* radius: 30,	 */
			}, 				
		],
			chart: {
			type: 'area',
			height: 70,
			width: 600,
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
		  curve:'straight',
		  colors:['#16afef'],
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
			colors:'#16afef',
			gradient: {
				colorStops:[ 
					
					{
					  offset: 0,
					  color: '#16afef',
					  opacity: .4
					},
					{
					  offset: 0.6,
					  color: '#16afef',
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

		var chartBar1 = new ApexCharts(document.querySelector("#invoicessent"), options);
		chartBar1.render();
	 
	}
	var revenueMap = function(){
		  var options = {
			  series: [
				{
					name: 'Net Profit',
					data: [10, 20, 30, 20, 32, 20, 30],
					//radius: 12,	
				}, 				
			],
				chart: {
				type: 'line',
				height: 280,
				toolbar: {
					show: false,
				},
				
			},
			plotOptions: {
			  bar: {
				horizontal: true,
				columnWidth: '70%',
				endingShape: 'rounded'
			  },
			},
			colors:['#886CC0'],
			dataLabels: {
			  enabled: false,
			},
			markers: {
				shape: "circle",
			},
	
			legend: {
				show: false,
			},
			stroke: {
			  show: true,
			  width: 4,
			  curve:'smooth',
			  colors:['var(--primary)'],
			},
			
			grid: {
				borderColor: '#eee',
				
				 xaxis: {
					lines: {
						show: true,
					}
				},  
				 yaxis: {
					
					lines: {
						show: true,
					}
				},  
			},
			xaxis: {
				
			  categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
			  labels: {
				style: {
					colors: 'var(--text)',
					fontSize: '12px',
					
					fontWeight: 100,
					cssClass: 'apexcharts-xaxis-label',
				},
			  },
			  crosshairs: {
			  show: false,
			  },
			
			},
			yaxis: {
			show:true,	
			labels: {
				offsetX: -15,
			   style: {
				colors: 'var(--text)',
				fontSize: '12px',
				  fontWeight: 100,
				  
				},
				 formatter: function (y) {
						  return y.toFixed(0) + "k";
						}
			  },
			},
			axisBorder: {
			  show: false,
			  color: '#78909C',
			  offsetX: 0,
			  offsetY: 0
			},
			fill: {
			  opacity: 1,
			  colors:'#FAC7B6'
			},
			tooltip: {
			  y: {
				formatter: function (val) {
				  return "$ " + val + " k"
				}
			  }
			}
			};

			var chartBar1 = new ApexCharts(document.querySelector("#revenueMap"), options);
			chartBar1.render();
		 
		 
	}
	var chartBarRunning = function(){
		
		var options  = {
			  series: [
				{
					name: 'Projects',
					 data: [31, 40, 28]
				}, 
				{
				  name: 'Projects',
				   data: [11, 32, 45]
				}, 
				
			],
			chart: {
			type: 'bar',
			height: 350,
			
			
			toolbar: {
				show: false,
			},
			
		},
		plotOptions: {
		  bar: {
			horizontal: false,
			endingShape:'rounded',
			columnWidth: '50%',
			
		  },
		},
		colors:['#625288', '#DE5656'],
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
				colors: '#000000',
				
				},
			markers: {
			width: 18,
			height: 18,
			strokeWidth: 0,
			strokeColor: '#fff',
			fillColors: undefined,
			radius: 15,	
			}
		},
		stroke: {
		  show: true,
		  width: 10,
		  curve: 'straight',
		  width: 10,
		  colors: ['transparent']
		},
		grid: {
			borderColor: '#eee',
		},
		xaxis: {
			
		  categories: ['Sun', 'Mon', 'Tue'],
		  labels: {
		   style: {
			  colors: '#787878',
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
				  colors: '#787878',
				  fontSize: '13px',
				   fontFamily: 'poppins',
				  fontWeight: 100,
				  cssClass: 'apexcharts-xaxis-label',
			  },
		  },
		},
		fill: {
		  opacity: 1,
		  colors:['#816CFF', '#77248B'],
		},
		tooltip: {
		  y: {
			formatter: function (val) {
			  return "$ " + val + " thousands"
			}
		  }
		},
		 responsive: [{
			breakpoint: 575,
			options: {
				plotOptions: {
				  bar: {
					columnWidth: '80%',
				  },
				},
				chart:{
					height:250,
				}
			}
		 }]
		};

		var chart = new ApexCharts(document.querySelector("#chartBarRunning"), options);
		chart.render();
			
	}
	var donutChart1 = function(){
		$("span.donut1").peity("donut", {
			width: "80",
			height: "80"
		});
	}
	var widgetChart3 = function(){
		if(jQuery('#widgetChart3').length > 0 ){
			const widgetChart3 = document.getElementById("widgetChart3").getContext('2d');
			//generate gradient
			const widgetChart3gradientStroke = widgetChart3.createLinearGradient(0, 1, 0, 500);
			widgetChart3gradientStroke.addColorStop(0, "rgba(90, 69, 170, 1)");
			widgetChart3gradientStroke.addColorStop(1, "rgba(90, 69, 170, 1)");

			new Chart(widgetChart3, {
				type: "line",
				data: {
					labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "January", "February", "March", "April"],

					datasets: [{
						label: "Sales Stats",
						borderColor: 'transparent',
						pointBackgroundColor: 'var(--primary)',
						pointBorderColor: 'var(--primary)',
						borderWidth:4,
						borderRadius:10,
						pointHoverBackgroundColor: 'var(--primary)',
						pointHoverBorderColor: 'var(--primary)',
						fill:true,
						tension:0.5,
						backgroundColor: widgetChart3gradientStroke,
						
						data: [12, 20, 16, 13, 16, 24, 20, 21, 19, 23, 17, 14, 24, 21, 13, 15, 27, 29, 21, 11, 14, 19, 21, 17]
					}]
				},
				options: {
					plugins:{
						legend: false, 

						tooltip: {
							intersect: !1,
							mode: "nearest",
							xPadding: 10,
							yPadding: 10,
							caretPadding: 10
						},
					},
					scales: {
						x:{
							display: !1,
							gridLines: !1,
							scaleLabel: {
								display: !0,
								labelString: "Month"
							}
						},
						y:{
							display: !1,
							gridLines: !1,
							scaleLabel: {
								display: !0,
								labelString: "Value"
							},
							ticks: {
								beginAtZero: !0
							}
						}
					},
					
					
					
					
					
					responsive: !0,
					maintainAspectRatio: !1,
					hover: {
						mode: "index"
					},
					
					elements: {
						point: {
							radius: 0,
							borderWidth: 0
						}
					},
					layout: {
						padding: {
							left: 0,
							right: 0,
							top: 5,
							bottom: 0
						}
					}
				}
			});

		}
	}
	var chartBar = function(){
		var options = {
			  series: [
				{
					name: 'Income',
					data: [50, 18, 70, 40, 50, 18, 70, 40],
					//radius: 12,	
				}, 
				{
				  name: 'Expense',
				  data: [80, 40, 55, 20,80, 40, 55, 20]
				}, 
				
			],
				chart: {
				type: 'bar',
				height: 330,
				
				toolbar: {
					show: false,
				},
				
			},
			plotOptions: {
			  bar: {
				horizontal: false,
				columnWidth: '50%',
				endingShape: "rounded",
				borderRadius: 2,
			  },
			  
			},
			states: {
			  hover: {
				filter: 'none',
			  }
			},
			colors:['var(--primary)', 'var(--secondary)'],
			dataLabels: {
			  enabled: false,
			},
			markers: {
		shape: "circle",
		},
		
		
			legend: {
				show: true,
				fontSize: '12px',
				 position: 'top',
				labels: {
					colors: 'var(--text-dark)',
					
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
				borderColor: '#eee',
			},
			xaxis: {
				position: 'bottom',
			  categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
			  labels: {
			   show: false,
			   style: {
				  colors: '#787878',
				  fontSize: '13px',
				  fontFamily: 'poppins',
				  fontWeight: 100,
				  cssClass: 'apexcharts-xaxis-label',
				},
			  },
			   axisBorder:{
				 show: false,  
				   
				 },
			  crosshairs: {
			  show: false,
			  }
			},
			yaxis: {
				labels: {
					offsetX:-16,
				   style: {
					  colors: '#787878',
					  fontSize: '13px',
					   fontFamily: 'poppins',
					  fontWeight: 100,
					  cssClass: 'apexcharts-xaxis-label',
				  },
			  },
			},
			fill: {
			  opacity: 1,
			  colors:['var(--primary)', 'var(--secondary)'],
			},
			tooltip: {
			  y: {
				formatter: function (val) {
				  return "$ " + val + " thousands"
				}
			  }
			},
			};

			var chartBar1 = new ApexCharts(document.querySelector("#chartBar"), options);
			chartBar1.render();
	}
	
	
	
	
	
	
	
	
	
	
	
 
	/* Function ============ */
		return {
			init:function(){
				
			},
			
			
			load:function(){
				//totalInvoices();
				//unpaidinvoices();
				//paidinvoices();
				//invoicessent();
				revenueMap();
				chartBarRunning();
				donutChart1();
				widgetChart3();
				chartBar();
				//widgetChart1();	
				//widgetChart2();
				widgetChart4();
				widgetChart5();
				
				
			},
			
			resize:function(){
				
			}
		}
	
	}();

	
		
	jQuery(window).on('load',function(){
		setTimeout(function(){
			dlabChartlist.load();
		}, 1000); 
		
	});

     

})(jQuery);