

(function($) {
    /* "use strict" */
	
 var dlabChartlist = function(){
	
	var screenWidth = $(window).width();
	//let draw = Chart.controllers.line.__super__.draw; //draw shadow
	
	var redial = function(){
		  var options = {
          series: [70],
          chart: {
          type: 'radialBar',
          offsetY: 0,
		  height:350,
          sparkline: {
            enabled: true
          }
        },
        plotOptions: {
          radialBar: {
            startAngle: -130,
            endAngle: 130,
            track: {
              background: "#F1EAFF",
              strokeWidth: '100%',
              margin: 5,
            },
			
			hollow: {
              margin: 30,
              size: '45%',
              background: '#F1EAFF',
              image: undefined,
              imageOffsetX: 0,
              imageOffsetY: 0,
              position: 'front',
            },
			
            dataLabels: {
              name: {
                show: false
              },
              value: {
                offsetY: 5,
                fontSize: '22px',
				color:'#886CC0',
				fontWeight:700,
              }
            }
          }
        },
		responsive: [{
          breakpoint: 1800,
          options: {
           chart: {
			  height:250
			},
          }
        }
		
		],
        grid: {
          padding: {
            top: -10
          }
        },
		/* stroke: {
          dashArray: 4,
		  colors:'#6EC51E'
        }, */
        fill: {
          type: 'gradient',
		  colors:'#5A45AA',
          gradient: {
              shade: '#0BB6C1',
              shadeIntensity: 0.15,
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 50, 65, 91]
          },
        },
        labels: ['Average Results'],
        };

        var chart = new ApexCharts(document.querySelector("#redial"), options);
        chart.render();
	
	
	}
	var donutChart1 = function(){
		$("span.donut1").peity("donut", {
			width: "80",
			height: "80"
		});
	}
	var pieChart = function(){
		if(jQuery('#pieChart').length > 0 ){
			//doughut chart
			const pieChart = document.getElementById("pieChart").getContext('2d');
			
			// pieChart.height = 100;
			new Chart(pieChart, {
				type: 'doughnut',
				data: {
					weight: 5,	
					defaultFontFamily: 'Poppins',
					datasets: [{
						data: [50, 30, 20],
						borderWidth: 0, 
						borderColor: "rgba(255,255,255,1)",
						backgroundColor: [
							"#8df05f",
							"#ff4b4b",
							"#e3e3e3"
						],
						hoverBackgroundColor: [
							"#8df05f",
							"#ff4b4b",
							"#e3e3e3"
						]

					}],
				},
				options: {
					weight: 1,	
					cutoutPercentage: 70,
					responsive: true,
					maintainAspectRatio: false
				}
			});
		}
	}
	var lineChart = function(){
		var options = {
		  series: [
		  {
			name: "Income",
			data: [10, 30, 20, 40, 20, 45, 10]
		},
		{
			name: "Expense",
			data: [10, 15, 10, 30, 15, 35, 5]
		},
		{
			name: "Unknown",
			data: [5, 15, 5, 15, 10, 25, 5]
		}
		],
		  chart: {
		  height: 170,
		  type: 'line',
		  toolbar:{
			  show:false
		  },
		  zoom: {
			enabled: false
		  }
		},
		colors:['#68e365','#FFB252','#969ba0'],
		dataLabels: {
		  enabled: false
		},
		stroke: {
		  curve: 'smooth',
		  width:3
		},
		legend:{
			show:false
		},
		grid: {
		 
		   xaxis: {
				lines: {
					show: true
				},
				style:{
					color:'#000',
				}
			},  
		},
		xaxis: {
		  categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
		},
		yaxis:{
			show:false
		}
		};

		var chart = new ApexCharts(document.querySelector("#lineChart"), options);
		chart.render();
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
 
	/* Function ============ */
		return {
			init:function(){
			},
			
			
			load:function(){
				redial();
				donutChart1();
				pieChart();
				lineChart();
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