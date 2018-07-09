$(function () {
    $('#mblog').keyup(function () {
        if ($('#mblog').val().length > 150){
            $('#mblog').val().length = 150
        }
    });

    $("#testForm").submit(function () {
        if ($('#mblog').val().length == 0 || $('#title').val().length==0){
            alert('您还没有输入完整哦!');
            return false;
        }else{
            return true;
        }
    });
});