function showNext(element, bool){
    if( bool === undefined ) { bool = 1}
    if( element.val() == bool ){
        element.parents('tr').next().effect("highlight", {}, 100)
    }else{
        element.parents('tr').next().hide()
    }
    element.unbind('change').bind('change', function(){ showNext(element, 1) })
}

function showNextTwo(element){
    if( element.val() == 1){
        element.parents('tr').next().effect("highlight", {}, 100)
        element.parents('tr').next().next().effect("highlight", {}, 100)
    }else{
        element.parents('tr').next().hide()
        element.parents('tr').next().next().hide()
    }
    element.unbind('change').bind('change', function(){ showNextTwo(element) })
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

function hideElements(element, limit){
    if( element.val() == 0 ){
        element.parents('tr').nextUntil(limit, 'tr').hide()
    }else{
        element.parents('tr').nextUntil(limit, 'tr').effect("highlight", {}, 100)
    }
    element.unbind('change').bind('change', function(){ hideElements(element, limit) })

}