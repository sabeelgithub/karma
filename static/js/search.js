

function search(){
    document.getElementById("form").addEventListener("click", function(event){
        event.preventDefault()
      });
        console.log("rftg");
        
        const txt = document.getElementById("search_input").value
        if(txt.length!==0){
            console.log('entered');
            $('#form').submit()
        }
    

}
