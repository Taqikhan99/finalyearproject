
const addSection=document.querySelector('.newlocAdding')
addSection.style.visibility='hidden'    

var latitude=document.getElementById('latitude')
var longitude=document.getElementById('longitude')

const newbtn=document.querySelector('.newlocbtn')

const form=document.getElementById('formAddLoc')
const mapdiv=document.getElementById("mapcanvas")
console.log(mapdiv);
// Initialize and add the map
function initMap() {
    // The location of Uluru
    const uluru = { lat: 24.7939785, lng: 67.1359185 };
    // The map, centered at Uluru
    options={
        zoom: 18,
        center: uluru,
      }

    const map = new google.maps.Map(mapdiv,options );
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
      position: uluru,
      map: map,
      draggable:true
    });

    google.maps.event.addListener(marker,'dragend',function(){
        console.log(marker.getPosition().lat());
        console.log(marker.getPosition().lng());

        latitude.value=marker.getPosition().lat()
        longitude.value=marker.getPosition().lng()
    })
  }

window.initMap = initMap;

form.addEventListener('submit',(event)=>{
    
    event.preventDefault()
    var locname=document.getElementById('locname').value
    
    
    // sendUserAndDate(userValue,date)
    if(locname==''||latitude==''||longitude==''){
        alert('Please fill the fields first')
    }
    else{

        sendNewLocation(locname,latitude.value,longitude.value)
        console.log('Success!')
        addSection.style.visibility='hidden'
        alert('Location added') 
    }
      
})


function sendNewLocation(locname,latitude,longitude){

    var xhr= new XMLHttpRequest()

    console.log(locname,latitude)
    xhr.open('POST',`../../addLocation`,true)
    
   

    xhr.onload=function(){
    // document.querySelector('.userdatashow').innerHTML=this.responseText
    console.log(this.responseText)
    
    }

    locationValues={
        'locname':locname,
        'latitude':latitude,
        'longitude':longitude,
        
    }
    xhr.send(JSON.stringify(locationValues))  

}


newbtn.addEventListener('click',(e)=>{

    addSection.style.visibility='visible'
})



