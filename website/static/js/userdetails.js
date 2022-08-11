// $(function() {
//     $('#btnloaddata').on('click', function(e) {
//       e.preventDefault()
//       alert('btn clicked')
//       $.getJSON('/sum',
//           function(data) {
//         //do nothing
//         console.log(data)
//       });
//       return false;
//     });
//   });

function makingCall(userid){
    var xhr= new XMLHttpRequest()

    uservalue={userID:userid}
    xhr.open('GET',`../../loaduserdata/${userid}`,true)
    xhr.setRequestHeader('Content-type','application/json')

    xhr.onload=function(){

    
    // document.querySelector('.userdatashow').innerHTML=this.responseText
    console.log(this.responseText)
    alert('Called python function')
}
    xhr.send(JSON.stringify(uservalue))  
}


function training(userid){
    var xhr= new XMLHttpRequest()

    uservalue={userID:userid}
    xhr.open('GET',`../../trainingdata/${userid}`,true)
    xhr.setRequestHeader('Content-type','application/json')

    xhr.onload=function(){

    
    // document.querySelector('.userdatashow').innerHTML=this.responseText
    console.log(this.responseText)
    alert('Training completed!')
}
    xhr.send(JSON.stringify(uservalue))  
}


