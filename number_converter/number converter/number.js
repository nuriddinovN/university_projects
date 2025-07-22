
let decimal=document.getElementById("decimal");
let hex=document.getElementById("hexa");
let octal=document.getElementById("octal");
let binary_u=document.getElementById("binary-u");
let binary_s=document.getElementById("binary-s");
let binary_o=document.getElementById("binary-o");
let binary_t=document.getElementById("binary-t");
let binary_ieee=document.getElementById("binary-ieee");

var labels = document.querySelectorAll('label[hidden]');
var buttonText = document.getElementById('more');


function showToast(message, duration) {
    // Create a new div element for the toast
    var toast = document.createElement('div');
    toast.classList.add('toast');
    toast.textContent = message;

    // Append the toast to the body
    document.body.appendChild(toast);

    // Automatically remove the toast after the specified duration
    setTimeout(function() {
        toast.remove();
    }, duration);
}



document.getElementById('more').addEventListener('click', function() {

    if (buttonText.innerText === 'more') {
        labels.forEach(function(label) {
           label.setAttribute("h2","binary-Unsigned");
            label.hidden = !label.hidden;
        });
        buttonText.innerText = 'less';
    } else if(buttonText.innerText==="less"){
        labels.forEach((label)=>{
            label.setAttribute("hidden",'');

        });
        buttonText.innerText="more"
    }
});



 function decimal2IEEE(num){
   {
    let buffer = new ArrayBuffer(4);
    let floatView = new Float32Array(buffer);
    let intView = new Uint32Array(buffer);

    floatView[0] = num;
    let hex = intView[0].toString(16).toUpperCase().padStart(8, '0');
    let binary = intView[0].toString(2).padStart(32, '0');

    return { hex: hex, binary: binary };
    }
}

//clwaer
document.getElementById("clear").addEventListener("click",()=>{
decimal.value='';
hex.value='';
octal.value='';
binary_u.value='';
binary_s.value='';
binary_o.value='';
binary_t.value='';
binary_ieee.value='';
//extara
storedValue="";
displayedNum.value="";

})

const convert = document.getElementById("convert");

convert.addEventListener("click", () => {
    showToast('click one more time', 3000); 
    //intialization
    const decimalInput = parseFloat(decimal.value);
    const binaryInput_u = binary_u.value.trim(); //tosting
    const octalInput=octal.value.trim();
    const hexInput=hex.value.trim();

    const binaryInput_s=binary_s.value.trim();
    let binaryInput_o=binary_o.value.trim();
    const binaryInput_t=binary_t.value.trim();
    




   //decimal
    if (!isNaN(decimalInput)) {
        binary_u.value = parseFloat(decimalInput, 10).toString(2);
        octal.value = parseFloat(decimalInput, 10).toString(8);
        hex.value = parseFloat(decimalInput, 10).toString(16);

if(decimalInput!=='NaN')
{        const ieeeSingle=`(0x${decimal2IEEE(decimalInput).hex})<=(${decimal2IEEE(decimalInput).binary})`;
        binary_ieee.value=ieeeSingle;
        console.log(ieeeSingle);
    }
    else{
        binary_ieee.value="0x7FC00000";
    }

        if(decimalInput>0){
            binary_s.value=parseFloat(decimalInput, 10).toString(2);
            binary_o.value=parseFloat(decimalInput, 10).toString(2);
            binary_t.value=parseFloat(decimalInput, 10).toString(2);


        }
    //signed
        else if(decimalInput<0){
            let positiveBinary = parseFloat(Math.abs(decimalInput),10).toString(2);
            let positiveBinaryDemo='0'+positiveBinary;
            let signMagnitude='1'+positiveBinary;

            
            binary_s.value=signMagnitude;
            binary_u.value=`-(${(positiveBinaryDemo)})`;


        //one's complement
        function binaryToOnes(binaryNumber){
        var onesComplement=positiveBinaryDemo.split('').map(bit => (bit === '0' ? '1' : '0')).join('');
        if(binaryNumber.length<=4){
            onesComplement=onesComplement.padStart(4,'1');
        }    
        else if(binaryNumber.length>4&&binaryNumber.length<8){
                onesComplement=onesComplement.padStart(8,'1');
            }
            else if(binaryNumber.length>8&&binaryNumber.length<16){
                onesComplement=onesComplement.padStart(16,'1');
            }
            
        
            return onesComplement;
        }  
            let onesComplement=binaryToOnes(positiveBinaryDemo);
            binary_o.value=onesComplement;

            //two's complement
            function onesToTwosComplement(onesComplement) {
                return (parseInt(onesComplement, 2) + 1).toString(2).padStart(onesComplement.length, '0');
            }
          let twosComplement=onesToTwosComplement(onesComplement);
          binary_t.value=twosComplement;
        }

        



        
    } 
    //binary
    else if (binaryInput_u) {
       
        const [integerPart, fractionalPart] = binaryInput_u.split('.');

        let intDec = 0;
        let bits = 1;
        for (let i = integerPart.length - 1; i >= 0; i--) {
            const currentDigit = parseInt(integerPart[i], 10);
            intDec += currentDigit * bits;
            bits *= 2;
        }

        let floatDec = 0;
        if (fractionalPart) {
            let floatBits = 0.5;
            for (let i = 0; i < fractionalPart.length; i++) {
                const currentDigit = parseInt(fractionalPart[i], 10);
                floatDec += currentDigit * floatBits;
                floatBits /= 2;
            }
        }

        
        const binary2Dec = intDec + floatDec;
        decimal.value = binary2Dec.toFixed(2); // Display with 2 decimal places
        octal.value=binary2Dec.toString(8);
        hex.value=binary2Dec.toString(16);
    }
//for octal part
    else if(octalInput){

        const [integerPart, fractionalPart] = octalInput.split('.');
    
        let intDec = 0;
        let bits = 1;
        for (let i = integerPart.length - 1; i >= 0; i--) {
            const currentDigit = parseInt(integerPart[i], 8); 
            intDec += currentDigit * bits;
            bits *= 8;
        }
    
    
        let floatDec = 0;
        if (fractionalPart) {
            let floatBits = 1 / 8; 
            for (let i = 0; i < fractionalPart.length; i++) {
                const currentDigit = parseInt(fractionalPart[i], 8); 
                floatDec += currentDigit * floatBits;
                floatBits /= 8;
            }
        }
    
        const octal2Dec = intDec + floatDec;
        decimal.value=octal2Dec;
        hex.value=octal2Dec.toString(16);
        binary_u.value=octal2Dec.toString(2);

    }

//HEX CONVET
else if(hexInput){
    const realHex=hexInput.split('').reverse().join('');
    console.log(realHex);
    const [integerPart] = realHex.split('.');
    let intDec=0;
    let bits=1;
    for(let i=0;i<integerPart.length;i++){
        const currentDigit=parseInt(integerPart[i],16);
        intDec+=currentDigit*bits;
        bits*=16;
    }

  const floatDec=0;

const hex2Dec=intDec+floatDec;
decimal.value=hex2Dec;
octal.value=hex2Dec.toString(8);
binary_u.value=hex2Dec.toString(2);
}

//singed binary
else if(binaryInput_s){
const magnitudeBi=binaryInput_s.slice(1);
const [integerPart, fractionalPart] = magnitudeBi.split('.');

        let intDec = 0;
        let bits = 1;
        for (let i = integerPart.length - 1; i >= 0; i--) {
            const currentDigit = parseInt(integerPart[i], 10);
            intDec += currentDigit * bits;
            bits *= 2;
        }

        let floatDec = 0;
        if (fractionalPart) {
            let floatBits = 0.5;
            for (let i = 0; i < fractionalPart.length; i++) {
                const currentDigit = parseInt(fractionalPart[i], 10);
                floatDec += currentDigit * floatBits;
                floatBits /= 2;
            }
        }
const dec=intDec+floatDec;
const sign=-1;
const negaviteDec=sign*dec;
decimal.value=negaviteDec;
octal.value=negaviteDec.toString(8);
hex.value=negaviteDec.toString(16);
binary_u.value=`abs(${negaviteDec.toString(2).slice(1)})`;
}

//ones complement
else if(binaryInput_o){

    const sign=-1;
    const onesSign=(binaryInput_o[0]*(Math.pow(2,(binaryInput_o.length-1)))-1)*sign;

    let slicedones=binaryInput_o.slice(1);
    let intDec = 0;
        let bits = 1;
        for (let i = slicedones.length - 1; i >= 0; i--) {
            const currentDigit = parseInt(slicedones[i], 10);
            intDec += currentDigit * bits;
            bits *= 2;
        }
const decimalDemo=onesSign+intDec;
decimal.value=decimalDemo;

}

//two's complment
else if(binaryInput_t){
    const sign=-1;
    const onesSign=(binaryInput_t[0]*(Math.pow(2,(binaryInput_t.length-1))))*sign;

    let slicedones=binaryInput_t.slice(1);
    let intDec = 0;
        let bits = 1;
        for (let i = slicedones.length - 1; i >= 0; i--) {
            const currentDigit = parseInt(slicedones[i], 10);
            intDec += currentDigit * bits;
            bits *= 2;
        }
const decimalDemo=onesSign+intDec;
decimal.value=decimalDemo;
}

})
/////////////////////////////////////////////////////////////////////////*****************************************///////////////////////////////
var buttons = document.querySelectorAll('.numbers .col button');
let  displayedNum = document.getElementById("display");
var storedValue = "";

const and=document.getElementById("and");
const or=document.getElementById("or");
const not=document.getElementById("not");


    //validatiopn
function onlyBinary(key){
    var buttons=document.querySelectorAll(".numbers .col button");
    for(let i=1;i<9;i++){
        buttons[i].style.color="rgb(38, 53, 41)";
    }

    
}


//display menu key
displayedNum.addEventListener("keydown",(e)=>{
    onlyBinary();
    var clickedKey=e.key;
    if(clickedKey==="0"||clickedKey==="1"||clickedKey==="."){
        storedValue+=clickedKey;
        
    }else if(clickedKey==="Backspace"){
        storedValue=storedValue.slice(0,-1);
        
    }
    else{
        e.preventDefault();
    }
})






//buttons for display menu
displayedNum.addEventListener("click",()=>{
    onlyBinary()

buttons.forEach((button)=>{
    button.addEventListener("click",()=>{
        onlyBinary()
            if((button.textContent==='1'||button.textContent==='0'||button.textContent===".")&&button.textContent!=="+/-"){
            storedValue+=button.textContent;
            displayedNum.value=storedValue;
            console.log(storedValue);
            }
        })
    })

   

})



//decimal validation
function onlydecimal(){
    var buttons=document.querySelectorAll(".numbers .col button");
    for(let i=1;i<9;i++){
        buttons[i].style.color="rgb(222, 251, 221)";
    }
}
  
//deciaml button
decimal.addEventListener("click",()=>{
    onlydecimal();
    var storedDec=""  
    buttons.forEach((button)=>{
        button.addEventListener("click",()=>{
            onlydecimal();
            
            if(button.textContent!=="+/-")
               { storedDec+=button.textContent;
                decimal.value=storedDec;}
            else if(button.textContent==="⌫"){
                storedDec=convertingVal.slice(0,-1);
                decimal.value=storedDec;

            }
        })
    })
})



///octal validation
function onlyOctal(){
    var buttons=document.querySelectorAll(".numbers .col button");
   buttons[7].style.color="rgb(38, 53, 41)";
   buttons[8].style.color="rgb(38, 53, 41)";
}
///octal button
octal.addEventListener("click",()=>{
    onlyOctal();
    var convertingVal=""  
    buttons.forEach((button)=>{
        button.addEventListener("click",()=>{
            onlyOctal();
            
            if(button.textContent!=="+/-"&&buttonText==="8"&&button.textContent==="9")
               { convertingVal+=button.textContent;
                octal.value=convertingVal;
                console.log(convertingVal);
        }
            else if(button.textContent==="⌫"){
                convertingVal=convertingVal.slice(0,-1);
                octal.value=convertingVal;

            }
        })
    })
})



document.getElementById("delete").addEventListener("click",()=>{
storedValue=storedValue.slice(0,-1);
displayedNum.value=storedValue;
});


const equal=document.getElementById("equal");







