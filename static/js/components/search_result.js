Vue.component('nav-bar', {
    template : `
    <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
            <div class="w-25 h-100">
                <a class="navbar-brand" :href="formattedProductPage">Ecom App</a>
            </div>
            <div class="w-75 d-flex justify-content-between align-items-center"> 
                <form class="row ms-auto mt-3" method="POST"> 
                    <input type="hidden" name="form_name" value="search_product"> 
                    <div class="col-auto">
                        <label for="inputValue" class="visually-hidden">Password</label>
                        <input type="text" class="form-control" id="inputValue" placeholder="Search items..." name="querry">
                    </div>
                    <div class="col-auto">
                        <button type="submit" class="btn btn-primary mb-3">
                            Search
                            <?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M16.6725 16.6412L21 21M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </form>
                <div class="my-0">
                    <a :href="formattedUrl" class="btn btn-outline-success mx-3">Cart</a>
                    <a href="/logout"><button class="btn btn-outline-danger" type="submit">Log out</button></a>
                </div>
            </div>
        </div>
    </nav>

    `,
    data() {
        return {
            cartUrl: '',
            dahsboardUrl : '',
        };
    },
    mounted() {
        const baseUrl = '/cart';
        const adminBase = '/products'
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        this.cartUrl = `${baseUrl}/${resourceId}`;
        this.dahsboardUrl = `${adminBase}/${resourceId}`
    },
    computed: {
        formattedUrl() {
            return this.cartUrl;
        }, 
        formattedProductPage(){
            return this.dahsboardUrl;
        },
        submitForm(event) {
            event.preventDefault(); 
            const queryInput = document.getElementById('inputValue');
            const query = encodeURIComponent(queryInput.value.trim()); 
            console.log(query);
            window.location.href = `/search_results?q=${query}`;
        }
    }
});
   
Vue.component("main-product-section", {
    template : `
    <div class="product-container mt-5" id="products">
        <div class="category-container bg-light border rounded-2 my-3 p-3" v-for="(products, categoryName) in returnMainProduct">
            <h3 class="m-2 category-name">{{categoryName}}</h3>
            <div class="product-card-container" style="display: flex;"> 

                <div class="product-card bg-white p-4 m-2 border rounded-2" v-for="(product, value) in products">
                    <div class="product-info mb-3">
                            <h5 class="product-name">{{product['name']}}</h5>
                            <p class="product-price">
                                <b>₹{{product['price']}}</b>
                            </p>
                    </div>

                    <div class="button-container" style="display: flex;" v-if="product['quantity'] > 0">
                        <a :href="returnBuyProductUrl + product['name']" class="btn btn-success">Buy</a>
                        <form method="POST" class="mx-2">
                            <input type="hidden" name="form_name" value="add_to_cart"> 
                            <input type="hidden" name="product-name" :value="product['name'] + ' + ' + categoryName"> 
                            <button onclick="cartSuccess()" type="submit" class="btn btn-outline-secondary">Add to cart</button>
                        </form>
                    </div>
                    <div v-else>
                        <button type="button" class="btn btn-outline-secondary" disabled>Out of stock</button>
                    </div>
                </div> 

            </div>
        </div>
    </div>
    `, 
    data() {
        return {
            userID : '',
            mainPoducts : '',
            buyProudctUrl : '', 
            queryString : ''
        }
    }, 
    mounted() {
        this.userID = this.$parent.$el.attributes['user-id'].value;
        this.queryString = this.$parent.$el.attributes['query-string'].value;
        const base = '/buy-product'; 
        this.buyProudctUrl = `${base}/${this.userID}?product-name=`;
        console.log("http://127.0.0.1:8080//api/search/"+this.userID+"?q="+this.queryString);
        fetch("http://127.0.0.1:8080//api/search/"+this.userID+"?q="+this.queryString)
        .then(response => response.json())
        .then(data => {
            this.mainPoducts = data;
        })
        .catch(error => {
            console.error("error encountered ", error);
        });
    },
    computed : {
        returnMainProduct(){
            return this.mainPoducts;
        }, 
        returnUserID(){
            return this.userID;
        }, 
        returnBuyProductUrl(){
            return this.buyProudctUrl;
        }
    }
})

new Vue({
    el: '#app', 
    delimiters : ['${', '}'],
});


