function showNext(element){
    if( element.val() == 1){
        element.parents('tr').next().show()
    }else{
        element.parents('tr').next().hide()
    }
    /* change event added every fricking time! have to check somehow */
    element.change(function(){ showNext(element) })
}

function showNextTwo(element){
    if( element.val() == 1){
        element.parents('tr').next().show()
        element.parents('tr').next().next().show()
    }else{
        element.parents('tr').next().hide()
        element.parents('tr').next().next().hide()
    }
    /* change event added every fricking time! have to check somehow */
    element.change(function(){ showNextTwo(element) })
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
        element.parents('tr').nextUntil(limit, 'tr').show()
    }
    /* change event added every fricking time! have to check somehow */
    element.change(function(){ hideElements(element, limit) })
}