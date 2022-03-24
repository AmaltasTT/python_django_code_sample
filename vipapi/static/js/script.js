function applicantlist() {
    var year = document.getElementById("selectyearvalue").value;
    $("#applicantdisplaypane").load("/checkapplicantsbyyear/?year="+year)
}

function domarkaschecked(x) {
    $("#fakediv").load("/markaschecked/?id="+x);
    window.open('/applicantdetails/'+x, '_self');
}

function send_message() {
    document.getElementById("closemessagemodal").click();
    $.post("/sendmessage/", $('#messageform').serialize(), function(data){
       console.log(data); 
       alert(data);
    });
}

function send_email() {
    document.getElementById("closeemailmodal").click();
    $.post("/sendemail/", $('#emailform').serialize(), function(data){
       console.log(data); 
       alert(data);
    });
}

function deleteapplicantaccount(x) {
    document.getElementById("deletemodalbutton").click();
    document.getElementById("storeapplicantid").value = x;
}

function dodeleteapplicantaccount() {
    var recordid = document.getElementById("storeapplicantid").value;
    document.getElementById("closedeletemodal").click();
    window.open('/deleteapplicantaccount/?id='+recordid, '_self'); 
}

