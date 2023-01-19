
// function validateSearch(el){
//     el.preventdefualt()
//     var input = document.getElementById('search_input').val();
//     console.log('sdsadfadssfdvs');
//     if(input.length==0){
//         return false
//     }
//     return true;

// }
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
