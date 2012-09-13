function showNext(element){
    if( element.val() == 1){
        element.parents('tr').next().show().effect("highlight", {}, 1000);
    }else{
        element.parents('tr').next().hide()
    }
}