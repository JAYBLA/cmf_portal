

(function($) {
    /* "use strict" */
	
 var dlabChartlist = function(){
	
	var screenWidth = $(window).width();
	//let draw = Chart.controllers.line.__super__.draw; //draw shadow
		
	var widgetChart4 = function(){
		if(jQuery('#widgetChart4').length > 0 ){
			const widgetChart4 = document.getElementById("widgetChart4").getContext('2d');
			//generate gradient
			const widgetChart4gradientStroke = widgetChart4.createLinearGradient(0, 1, 0, 500);
			widgetChart4gradientStroke.addColorStop(0, "rgba(68, 129, 78, 1)");
			widgetChart4gradientStroke.addColorStop(1, "rgba(68, 129, 78, 1)");

			new Chart(widgetChart4, {
				type: "line",
				data: {
					labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "January", "February", "March", "April"],

					datasets: [{
						label: "Sales Stats",
						borderColor: 'transparent',
						pointBackgroundColor: '#44814E',
						pointBorderColor: '#44814E',
						borderWidth:4,
						borderRadius:10,
						pointHoverBackgroundColor: '#44814E',
						pointHoverBorderColor: '#44814E',
						backgroundColor: widgetChart4gradientStroke,
						
						data: [12, 20, 16, 13, 16, 24, 20, 21, 19, 23, 17, 14, 24, 21, 13, 15, 27, 29, 21, 11, 14, 19, 21, 17]
					}]
				},
				options: {
					title: {
						display: !1
					},
					tooltips: {
						intersect: !1,
						mode: "nearest",
						xPadding: 10,
						yPadding: 10,
						caretPadding: 10
					},
					
					legend: {
						display: !1
					},
					responsive: !0,
					maintainAspectRatio: !1,
					hover: {
						mode: "index"
					},
					scales: {
						xAxes: [{
							display: !1,
							gridLines: !1,
							scaleLabel: {
								display: !0,
								labelString: "Month"
							}
						}],
						yAxes: [{
							display: !1,
							gridLines: !1,
							scaleLabel: {
								display: !0,
								labelString: "Value"
							},
							ticks: {
								beginAtZero: !0
							}
						}]
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
	var widgetChart5 = function(){
		if(jQuery('#widgetChart5').length > 0 ){
			const widgetChart5 = document.getElementById("widgetChart5").getContext('2d');
			//generate gradient
			const widgetChart4gradientStroke = widgetChart5.createLinearGradient(0, 1, 0, 500);
			widgetChart4gradientStroke.addColorStop(0, "rgba(90, 69, 170, 1)");
			widgetChart4gradientStroke.addColorStop(1, "rgba(90, 69, 170, 1)");

			new Chart(widgetChart5, {
				type: "line",
				data: {
					labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "January", "February", "March", "April"],

					datasets: [{
						label: "Sales Stats",
						borderColor: 'transparent',
						pointBackgroundColor: '#5a45aa',
						pointBorderColor: '#5a45aa',
						borderWidth:4,
						borderRadius:10,
						pointHoverBackgroundColor: '#5a45aa',
						pointHoverBorderColor: '#5a45aa',
						fill:true,
						tension:0.5,
						backgroundColor: widgetChart4gradientStroke,
						
						data: [12, 20, 16, 13, 16, 24, 20, 21, 19, 23, 17, 14, 24, 21, 13, 15, 27, 29, 21, 11, 14, 19, 21, 17]
					}]
				},
				options: {
					title: {
						display: !1
					},
					tooltips: {
						intersect: !1,
						mode: "nearest",
						xPadding: 10,
						yPadding: 10,
						caretPadding: 10
					},
					
					plugins:{
						legend:false
					},

					responsive: !0,
					maintainAspectRatio: !1,
					hover: {
						mode: "index"
					},
					scales: {
						x: {
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
	var chartTimeline3 = function(){
		var optionsTimeline = {
			chart: {
				type: "bar",
				height: 320,
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
					data: [10, 50, 65, 20, 30]
				},
				{
					name: "Retained Clients",
					data: [-40, -60, -90, -25, -40]
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
				show: true,
				categories: ['01', '02', '03', '04', '05'],
				labels: {
					style: {
						colors: 'var(--text-dark)',
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
				show: true,
				labels: {
					style: {
						colors: 'var(--text-dark)',
						fontSize: '13px',
						fontFamily: 'Poppins',
						fontWeight: 400
						
					},
				},
				axisBorder: {
				  show: true,
				  color: '#78909C',
				  offsetX: 0,
				  offsetY: 0
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
 
	/* Function ============ */
		return {
			init:function(){
			},
			
			
			load:function(){
				widgetChart4();
				widgetChart5();
				chartTimeline3();
				
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