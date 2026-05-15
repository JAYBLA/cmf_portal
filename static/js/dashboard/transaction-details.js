

(function($) {
    /* "use strict" */
	
 var dlabChartlist = function(){
	
	var screenWidth = $(window).width();
	
		var chartTimeline3 = function(){
		var optionsTimeline = {
			chart: {
				type: "bar",
				height: 189,
				stacked: true,
				toolbar: {
					show: false
				},
				sparkline: {
					//enabled: true
				},
				backgroundBarRadius: 5,
				offsetX: 0,
			},
			series: [
				 {
					name: "New Clients",
					data: [10, 50, 65, 20, 30,10, 50, 65]
				},
				{
					name: "Retained Clients",
					data: [-40, -60, -90, -25, -40,-40, -60, -90]
				} 
			],
			
			plotOptions: {
				bar: {
					columnWidth: "30%",
					endingShape: "rounded",
					colors: {
						backgroundBarColors: ['var(--light)', 'var(--light)', 'var(--light)', 'var(--light)', 'var(--light)'],
						backgroundBarOpacity: 1,
						backgroundBarRadius: 5,
						opacity:0
					},

				},
				distributed: true
			},
			colors:['var(--primary)', 'var(--primary)'],
			
			grid: {
				show: false,
			},
			legend: {
				show: false
			},
			stroke:{
				curve: 'smooth',
				 width: 2,
				  lineCap: 'butt',
			},
			fill: {
				opacity: 1
			},
			dataLabels: {
				enabled: false,
				colors:['#2953E8', '#09268A'],
				dropShadow: {
					enabled: true,
					top: 1,
					left: 1,
					blur: 1,
					opacity: 1
				}
			},
			xaxis: {
				categories: ['01', '02', '03', '04', '05','06','0.7','0.8'],
				labels: {
				 show: true,
					style: {
						colors: '#787878',
						fontSize: '13px',
						fontFamily: 'Poppins',
						fontWeight: 400
						
					},
				},
				crosshairs: {
					show: false,
				},
				axisBorder: {
					show: false,
				},
			},
			
			yaxis: {
				show: false,
				labels: {
					offsetX:-15,
					style: {
						colors: '#787878',
						fontSize: '13px',
						fontFamily: 'Poppins',
						fontWeight: 400
						
					},
				},
			},
			
			tooltip: {
				x: {
					show: true
				}
			}
		};
		var chartTimelineRender =  new ApexCharts(document.querySelector("#chartTimeline3"), optionsTimeline);
		 chartTimelineRender.render();
	}
	var revenueMap = function(){
		  var options = {
			  series: [
				{
					name: 'Net Profit',
					data: [20, 40, 20, 30, 50, 40, 60,],
					//radius: 12,	
				}, 				
			],
				chart: {
				type: 'line',
				height: 230,
				toolbar: {
					show: false,
				},
				
			},
			plotOptions: {
			  bar: {
				horizontal: false,
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
				show: true,
				 xaxis: {
					lines: {
						show: true,
					}
				},  
				 yaxis: {
					lines: {
						show: false,
					}
				},  
			},
			xaxis: {
				
			  categories: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
			  labels: {
				style: {
					colors: '#7E7F80',
					fontSize: '13px',
					fontFamily: 'Poppins',
					fontWeight: 100,
					cssClass: 'apexcharts-xaxis-label',
				},
			  },
			  crosshairs: {
			  show: false,
			  }
			},
			yaxis: {
			show:false,	
			labels: {
				offsetX: -15,
			   style: {
				  colors: '#7E7F80',
				  fontSize: '14px',
				   fontFamily: 'Poppins',
				  fontWeight: 100,
				  
				},
				 formatter: function (y) {
						  return y.toFixed(0) + "k";
						}
			  },
			},
			fill: {
			  opacity: 1,
			  colors:'#FAC7B6'
			},
			tooltip: {
			  y: {
				formatter: function (val) {
				  return "$ " + val + " hundred"
				}
			  }
			}
			};

			var chartBar1 = new ApexCharts(document.querySelector("#revenueMap"), options);
			chartBar1.render();
		 
		 
	 }
	 var reservationChart = function(){
		 var options = {
          series: [{
          name: 'series1',
          data: [400, 400, 650, 500, 900, 750, 850,400, 400, 650]
        }, {
          name: 'series2',
          data: [350, 350, 420, 370, 500, 400, 550,350, 350, 420]
        }],
          chart: {
          height: 300,
          type: 'line',
		  toolbar:{
			  show:false
		  }
        },
		colors:["var(--primary)","#09BD3C"],
        dataLabels: {
          enabled: false
        },
        stroke: {
			width:4,
			curve: 'smooth',
        },
		legend:{
			show:true,
			fontWeight: 400,
			fontSize:14,
		},
		grid:{
			borderColor: '#EBEBEB',
			strokeDashArray: 6,
		},
		markers:{
			strokeWidth: 6,
			 hover: {
			  size: 15,
			}
		},
		yaxis: {
		  labels: {
			offsetX:-12,
			style: {
				colors: '#787878',
				fontSize: '13px',
				fontFamily: 'Poppins',
				fontWeight: 400
				
			}
		  },
		},
        xaxis: {
          categories: ["Week 01","Week 02","Week 03","Week 04","Week 05","Week 06","Week 07","Week 08","Week 09","Week 10"],
		  labels:{
			  style: {
				colors: '#787878',
				fontSize: '13px',
				fontFamily: 'Poppins',
				fontWeight: 400
				
			},
		  }
        },
		fill:{
			type:"solid",
			/* opacity:0.1 */
		},
        tooltip: {
          x: {
            format: 'dd/MM/yy HH:mm'
          },
        },
        };

        var chart = new ApexCharts(document.querySelector("#reservationChart"), options);
        chart.render();
	}
	var emailchart = function(){
		 var options = {
          series: [27, 11, 22,25],
          chart: {
          type: 'donut',
		  height:250
        },
		dataLabels:{
			enabled: false
		},
		stroke: {
          width: 0,
        },
		colors:['#F87C22', '#2251F8', '#50D37D','#AB31E4'],
		legend: {
              position: 'bottom',
			  show:false
            },
        responsive: [{
          breakpoint: 1800,
          options: {
           chart: {
			  height:200
			},
          }
        },
		{
          breakpoint: 1800,
          options: {
           chart: {
			  height:200
			},
          }
        }
		]
        };

        var chart = new ApexCharts(document.querySelector("#emailchart"), options);
        chart.render();
    
	}
	var handleWorldMap = function(trigger = 'load'){
		var vmapSelector = $('#world-map');
		if(trigger == 'resize')
		{
			vmapSelector.empty();
			vmapSelector.removeAttr('style');
		}
		
		vmapSelector.delay( 500 ).unbind().vectorMap({ 
			map: 'world_en',
			backgroundColor: 'transparent',
			borderColor: 'rgb(239, 242, 244)',
			borderOpacity: 0.25,
			borderWidth: 1,
			color: 'rgb(239, 242, 244)',
			enableZoom: true,
			hoverColor: 'rgba(239, 242, 244 0.9)',
			hoverOpacity: null,
			normalizeFunction: 'linear',
			scaleColors: ['#b6d6ff', '#005ace'],
			selectedColor: 'rgba(239, 242, 244 0.9)',
			selectedRegions: null,
			showTooltip: true,
			onRegionClick: function(element, code, region)
			{
				var message = 'You clicked "'
					+ region
					+ '" which has the code: '
					+ code.toUpperCase();
		 
				alert(message);
			}
		});
	}
	
	
		
	
	
	
	
	
 
	/* Function ============ */
		return {
			init:function(){
			},
			
			
			load:function(){
				//chartTimeline3();
				revenueMap();
				reservationChart();
				emailchart();
				handleWorldMap();
				
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