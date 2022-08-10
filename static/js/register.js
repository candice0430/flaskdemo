function bindCaptchaBtnClick() {
$("#btn-send").click(function () {
        var $this = $(this);
        var email = $('input[name="email"]').val();
        if(!email){
            alert("请输入邮箱")
            return
        }
        $.ajax({
            url: "/user/mail",
            data: {
                email: email
            },
            method:"POST",
            success: function (result) {
                alert(result["msg"])
                $this.off("click");
                var countDown = 60;
                var timer = setInterval(function (){
                    if(countDown > 0){
                        $this.text(countDown+"s后重新发送");
                    }else{
                        $this.text("发送验证码");
                        $this.on("click");
                        bindCaptchaBtnClick();
                        clearInterval(timer);
                    }
                    countDown -= 1
                }, 1000);
            }
        });
    });
}

$(function () {
    bindCaptchaBtnClick();
})