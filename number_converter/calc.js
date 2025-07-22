const buttons=document.querySelectorAll("button");
const display=document.getElementById("display");
let storedValue="";
buttons.forEach(button=>{
    button.addEventListener("click",()=>{
if(button.textContent!=="%"&&button.textContent!=="x2"&&button.textContent!=="&#8656")
        {storedValue+=(button.textContent);
        display.value=storedValue;
        console.log(display.value);
    }
    })
});



document.querySelectorAll("button")[2].addEventListener("click",()=>{
    storedValue=storedValue*0.01;
    display.value=storedValue;
})

document.querySelectorAll("button")[3].addEventListener("click",()=>{
    storedValue=storedValue*storedValue;
    display.value=storedValue;
})

document.getElementById("clear").addEventListener("click",()=>{
    storedValue="";
    display.value="";
})

document.getElementById("del").addEventListener("click",()=>{
    storedValue=storedValue.slice(0,-2);
    display.value=storedValue;
})

document.addEventListener("keydown",(e)=>{
    if(document.activeElement===display){
    var keyPressed=e.key;
    if(!isNaN(keyPressed)||['+','-','*','/','.'].includes(keyPressed)){
        storedValue+=keyPressed;
    }

    if (e.key === "Backspace") {
        // Remove the last character from the display input
        storedValue = storedValue.slice(0, -1);
        display.value=storedValue;
    }

    if(e.key==="Enter"){
        try{
            display.value=eval(storedValue);
            storedValue=display.value;}
            catch(e){
                display.value="error"
            }
    }
    console.log(storedValue);
    }
})

document.getElementById("equal").addEventListener("click",()=>{
    //using eval() is not wise actually^_^;
    try{

    storedValue=storedValue.slice(0,-1);
    if(storedValue==="0+0"||display.value==="0+0"){
        storedValue="Hello World :)";
        display.value=storedValue;
    }
    else{
    display.value=eval(storedValue);
    storedValue=display.value;}
    
       }
    catch(e){
        display.value="error"
    }
})