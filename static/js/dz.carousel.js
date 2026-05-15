function carouselReview(){
	
	function checkDirection() {
		var htmlClassName = document.getElementsByTagName('html')[0].getAttribute('class');
		if(htmlClassName == 'rtl') {
			return true;
		} else {
			return false;
		}
	}
	
	jQuery('.owl-bank-wallet').owlCarousel({
		loop:true,
		autoplay:true,
		margin:0,
		nav:false,
		center:true,
		dots: false,
		rtl:checkDirection(),
		navText: [''],
		responsive:{
			0:{
				items:1
			},
			
			575:{
				items:2
			},			
			
			991:{
				items:2
			},
			1200:{
				items:2
			},
			1600:{
				items:2
			}
		}
	})			
	
	jQuery('.testimonial-one').owlCarousel({
		loop:true,
		autoplay:true,
		margin:15,
		nav:true,
		dots: false,
		rtl:checkDirection(),
		center:true,
		navText: ['<i class="las la-long-arrow-alt-left"></i>', '<i class="las la-long-arrow-alt-right"></i>'],
		responsive:{
			0:{
				items:3
			},
			600:{
				items:5
			},	
			991:{
				items:8
			},			
			
			1200:{
				items:4
			},
			1600:{
				items:6
			}
		}
	})	
	
	jQuery('.card-slider').owlCarousel({
		loop:true,
		margin:20,
		nav:false,
		autoplay:true,
		slideSpeed: 1000,
		paginationSpeed: 1000,
		dots: false,
		navText: ['', ''],
		responsive:{
			0:{
				items:1
			},
			576:{
				items:2
			},	
			768:{
				items:2
			},			
			991:{
				items:2
			},
			1200:{
				items:3
			},
			1600:{
				items:4
			}
		}
	})
	
}

jQuery(window).on('load',function(){
	setTimeout(function(){
		carouselReview();
	}, 1000); 
});