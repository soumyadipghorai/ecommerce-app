Vue.component("buy-product", {
    data : function(){
        return {
            "message" : "hello"
        }
    },
    template : `
        {{message}}
    `
});

let app = new Vue({
    el : "#app", 
    delimiters : ['${', '}']
})