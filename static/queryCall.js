
function testQuery(){
    console.log("Test begin")
	jQuery.ajax({
                url: "http://127.0.0.1:5001/accounts/validateLogin",
                type: "PUT",
                success: function(data){ console.log("Success! Data: " + data); },
                crossDomain: true,
                dataType: 'json',
                contentType: "application/json",
                data: JSON.stringify({ username: "user1", password: "pass1" })
                });
}