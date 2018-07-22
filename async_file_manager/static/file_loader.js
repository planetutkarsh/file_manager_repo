$(function(){

    var socket = new WebSocket('ws://' + window.location.host + '/file/');
    socket.onopen = function open(){
        console.log('web socket connected');
    }

    socket.onmessage = function(message){
        var message_data = JSON.parse(message.data);
        if(message_data.status == "loaded"){
           var div_block = $('#loaded-files');
           $('#in-progress').hide();
       } else{
           var div_block = $('#in-progress');
       }
        var new_msg = "<div>" + message_data.msg + "</div>";
        div_block.append(new_msg);
    }

    $('#file-upload').click(function(){
        socket.send({'data': 'hello'});
    })
})
