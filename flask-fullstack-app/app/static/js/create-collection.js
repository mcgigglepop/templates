$(document).ready(function(){
    dropdown('#collection_visibility');
    function dropdown(e){
        var obj = $(e+'.dropdown');
        var btn = obj.find('.btn-selector');
        var dd = obj.find('ul');
        var opt = dd.find('li');
                    
        obj.on("mouseenter", function() {
            dd.show();
            $(this).css("z-index",1000);
        }).on("mouseleave", function() {
            dd.hide();
            $(this).css("z-index","auto")
        })
                        
        opt.on("click", function() {
            dd.hide();
            var txt = $(this).text();
            if(dd.parent().attr('id') == "collection_visibility"){
                document.getElementById("hidden_collection_visibility").value= txt;
            }
            // populatePreview(dd.parent().attr('id'), txt);
            opt.removeClass("active");
            $(this).addClass("active");
            btn.text(txt);
        });
    }
});