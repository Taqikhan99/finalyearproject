
// for (var option of document.querySelectorAll('.options'))
// { 
//   option.remove();
// }

const pathdiv=document.getElementById('showpath')
const form=document.getElementById('formpred')

form.addEventListener('submit',(event)=>{
    
    event.preventDefault()
    var users=document.getElementById('userlist')
    var userValue = users.options[users.selectedIndex].value;

    var date=document.getElementById('cdate').value

    sendUserAndDate(userValue,date)
    console.log(date);
    console.log(userValue)
})


function sendUserAndDate(users,date){
    var xhr= new XMLHttpRequest()

    uservalue={userID:users}
    pathList=[]
    xhr.open('GET',`../../predictUserPath/${users}/${date}`,true)
    xhr.setRequestHeader('Content-type','application/json')

    xhr.onload=function(){

    
    // document.querySelector('.userdatashow').innerHTML=this.responseText
    pathList=JSON.parse( this.responseText)
    console.log(pathList)
    pathList=pathList.join(' --> ')
    if (pathList.length >0){
        pathdiv.innerText=`Path taken by user ${users} will be \n `+pathList
    }
    alert('Training completed!')
}
    xhr.send(JSON.stringify(uservalue))  
}