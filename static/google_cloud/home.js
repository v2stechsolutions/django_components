$('.fileListDiv').hide()
function UploadFile(){
 
    var fd = new FormData();
    var files = $('#file')[0].files[0];
    fd.append('file',files);

    $.ajax({
        url: 'upload',
        type: 'POST',
        data: fd,
        contentType: 'application/json',
        processData: false,
        dataType : "text",
        async : false,
        success: function(JsonData){
            alert(JsonData)
        },
    });
}


function GetFileList(){
    
        $.ajax({
            url : 'filelist',
            method : 'GET',
            dataType : 'text',
            async : false,
            success : function(JsonData){
                // alert(JsonData)
                parsed_json = JSON.parse(JsonData)
                console.log(parsed_json)
                console.log(parsed_json.FileList)
                console.log(parsed_json.FileList[0])
                $('.fileListDiv').empty();
    
                if(parsed_json.FileList.length == 0){
                    alert('No file found in cloud')
                }  
                
                for(i=0; i < parsed_json.FileList.length ; i++){
                    temp = '<p>'+parsed_json.FileList[i]+'</p>'
                    $('.fileListDiv').append(temp)
                    $('.fileListDiv').show();
                }
            },
            error: function(error, xhr, status) {
            }
        })
    }

    function GetFileListPre(){
    
        $.ajax({
            url : 'filelist',
            method : 'GET',
            dataType : 'text',
            async : false,
            success : function(JsonData){
                // alert(JsonData)
                parsed_json = JSON.parse(JsonData)
                console.log(parsed_json)
                console.log(parsed_json.FileList)
                console.log(parsed_json.FileList[0])
                $('.fileListDiv').empty();
    
                if(parsed_json.FileList.length == 0){
                    alert('No file found in cloud')
                }  
                
                for(i=0; i < parsed_json.FileList.length ; i++){
                    temp = '<option class=delete_user_options value = '+parsed_json.FileList[i]+'>'+parsed_json.FileList[i]+'</option>'
                    $('#downloadDiv').append(temp)
                }
            },
            error: function(error, xhr, status) {
            }
        })
    }

    GetFileListPre()



    function DownloadFile(){
        filename = $('#downloadDiv').val();
        content = {
            filename : filename
        }
        $.ajax({
            url : 'download',
            method : 'POST',
            data : JSON.stringify(content),
            contentType : 'application/json',
            dataType : "text",
            async : false,
            success : function(JsonData){
                window.location.href = JsonData
            },
            erro : function(){
                alert('Error While downloading file please try again.')
            }
        })
    }