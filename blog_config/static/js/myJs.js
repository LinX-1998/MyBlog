var mySwiper = new Swiper ('.swiper-container', {
    
    autoplay: {
        delay: 2000,
        stopOnLastSlide: false,
        disableOnInteraction: false,
    },

    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

    loop: true, // 循环模式选项
    
    // 如果需要分页器
    pagination: {
      el: '.swiper-pagination',
    },
    
    // 如果需要前进后退按钮
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },

})

$(function(){
	var back = $('.back');
	back.click(function(){
	//用setInterval可以设置每20ms就时窗口高度减少50，一直到
	//窗口已经到最上部，此时把timer清除
		var timer = setInterval(function(){
			$(window).scrollTop($(window).scrollTop()-50);
			if($(window).scrollTop() == 0){
				clearInterval(timer);
			}
		},20);
	});
	//当窗口在滚动是，高度小于250就隐藏按钮
	$(window).scroll(function(){
		if($(window).scrollTop() < 250){
			back.hide(50);
		}
		else{
			back.show(50);
		}
	});
});

$(function(){
    $(document).ready(function(){
        $("#one-icon").hover(function(){
            $("#two-icon").css("display","block");
    },function(){
            $("#two-icon").css("display","none");
        });
    });
});

$(function(){
    var music_on=document.getElementById("music_on");
    var music_off=document.getElementById("music_off");
    var clicknum=0;
    music_on.onclick=function(){
	    clicknum++;
	    var num=clicknum%2;
	    if(num==0){
		    music_off.style.display="block";
		    music_on.style.display="none"
		    stop();
	    }
	    else if(num==1){
		    play();
	    }
    };
    music_off.onclick=function(){
	    clicknum++;
	    var num=clicknum%2;
	    if(num==1){
		    music_off.style.display="none";
		    music_on.style.display="block"
		    play();
	    }
	    else if(num==0){
		    stop();
	    }
    };
    //音乐播放
    function play(){
	    document.getElementById('media').play();
    }
	//音乐暂停
    function stop(){
	    document.getElementById('media').pause();
    }
});
