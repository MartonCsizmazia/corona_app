


//SECOND SCRIPT CREATED
const actorRows = document.getElementsByClassName('doctor-row');

for (let row of actorRows) {
    row.addEventListener("click", clickHandler);

    function clickHandler() {
        let age = row.querySelector(".age-val");
        let name = row.querySelector(".actor-name");
        if (age.innerHTML >= 50){
            name.innerHTML = "Old" + name.innerHTML
        }
        else{
            name.innerHTML = "Young" + name.innerHTML
        }
        row.removeEventListener("click", clickHandler);
    }

}



/*
    kűlső skope változóit minimalizálni
 */


/*
 {
 var elem1 = document.getElementById('idDiv3');
 var elem2 = elem1.closest("#idDiv2");
 alert(elem2.outerHTML);
 }
*/