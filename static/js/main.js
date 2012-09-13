function showNext(element){
    if( element.val() == 1){
        element.parents('tr').next().show().effect("highlight", {}, 1000);
    }else{
        element.parents('tr').next().hide()
    }
}

function addSuffix(element, suffix){
        element.ready(function(){
            $(this).val($(this).val().replace(" "+suffix,""))
        }).focus(function(){
            $(this).val($(this).val().replace(" "+suffix,""))
        }).blur(function(){
            var content = $(this).val($(this).val() + " "+suffix)
        })
}

$(document).ready(function(){
    $("td").each(function(){
        $(this).html( $(this).html().replace('?</label>:','?</label>'))
    })
})