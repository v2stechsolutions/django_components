$('.fileListDiv').hide()
function UploadFile(){
    // $('#uploadFile').fileupload({
    //     maxChunkSize: 10000000 // 10 MB
    // });

    var fd = new FormData();
    var files = $('#file')[0].files[0];
    fd.append('file',files);
    alert('hi')
    alert(fd)
    console.log(fd)
    console.log('******************')
    $.ajax({
        url: '',
        type: 'POST',
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            
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
                alert(JsonData)
                parsed_json = JSON.parse(JsonData)
                console.log(parsed_json)
                console.log(parsed_json.FileList)
                console.log(parsed_json.FileList[0])
                $('.fileListDiv').empty();
    
                if(parsed_json.FileList.length == 0){
                    alert('No file found in drive')
                }  
                
                for(i=0; i < parsed_json.FileList.length ; i++){
                    temp = '<p>'+parsed_json.FileList[i].title+'</p>'
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
                alert(JsonData)
                parsed_json = JSON.parse(JsonData)
                console.log(parsed_json)
                console.log(parsed_json.FileList)
                console.log(parsed_json.FileList[0])
                $('.fileListDiv').empty();
    
                if(parsed_json.FileList.length == 0){
                    alert('No file found in drive')
                }  
                
                for(i=0; i < parsed_json.FileList.length ; i++){
                    temp = '<option class=delete_user_options value = '+parsed_json.FileList[i].id+'>'+parsed_json.FileList[i].title+'</option>'
                    $('#downloadDiv').append(temp)
                    // $('.fileListDiv').show();
                }
            },
            error: function(error, xhr, status) {
            }
        })
    }

    GetFileListPre()

    function DownloadFile(){
        filename = $('#downloadDiv').val();
        alert(filename)
        content = {
            id : filename
        }
        $.ajax({
            url : 'download',
            method : 'POST',
            data : JSON.stringify(content),
            contentType : 'application/json',
            dataType : "json",
            async : false,
            success : function(JsonData){
                console.log(JsonData)
                console.log(typeof(JsonData))
                console.log(JsonData.access)
            }
        })
    }