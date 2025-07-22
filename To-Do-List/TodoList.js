const input=document.getElementById("input");
const list=document.getElementById("list");



function addTask(){
    
    if(input.value===""){alert("Please, enter something")}
else{
        let li=document.createElement("li");
        li.innerHTML=input.value;
        list.appendChild(li);

        let span=document.createElement("span");
        span.innerHTML="\u00d7";
        li.appendChild(span);

   
   
}
input.value='';
saveData();
}


list.addEventListener("dblclick",(e)=>{
if(e.target.tagName==="LI"){
    e.target.style.textDecoration="line-through"
    saveData();

}
else if(e.target.tagName==="SPAN"){
    e.target.parentElement.remove();
    saveData();
}
},false)

function saveData(){
    localStorage.setItem("data",list.innerHTML);

}

function show(){
    list.innerHTML=localStorage.getItem("data");
}

show();