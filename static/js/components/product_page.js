Vue.component('nav-bar', {
    template : `
    <nav class="navbar navbar-expand-lg bg-body-tertiary px-3">
        <div class="container-fluid">
            <div class="w-25 h-100">
                <a class="navbar-brand" :href="formattedProductPage">Ecom App</a>
            </div>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
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
  
Vue.component("offers", {
    template : `
    <div>
    <div class="hero-section bg-light row my-5 mx-0 shadow-sm">
        <div class="col-sm-6 p-sm-4 p-md-5">
            <div class="text-section mt-5 mb-4">
                <h2>Available products</h2>
                <p class="description my-2">Welcome, {{name}}! Today We have the following products available for you, you can directly buy products from this page or maybe add to cart and buy every together in future.</p>
            </div>
            <a href="#products"><button class="btn btn-success">View Products</button></a>
        </div>
        <div class="col-sm-6 image-section"></div>
    </div>
    <div class="offer-container mt-5 bg-light p-5 shadow rounded-2">
        <div class="row">
            <div class="col">
                <h2>Offer Section</h2>
                <button class="btn btn-danger" type="button" disabled>
                    <span class="spinner-grow spinner-grow-sm text-warning" aria-hidden="true"></span>
                    <span class="visually-hidden" role="status">Loading...</span>
                </button>
            </div>
                <div class="col-sm-3 product-card rounded-2 border-1 bg-black bg-gradient bg-opacity-75 m-3 p-3 position-relative" v-for="offer in offers">
                    <h4 style="color: white;">{{offer['product_name']}}</h4>
                    <h6 style="color: white;">{{offer['price']}}</h6>
                    <div class="button-container" style="display: flex;">
                        <a :href="returnBuyProductUrl + offer['product_name']" class="btn btn-success">Buy</a>
                        <form method="POST" class="mx-2"> 
                            <input type="hidden" name="form_name" value="add_to_cart"> 
                            <input type="hidden" name="product-name" :value="offer['product_name'] +' + '+ offer['category']"> 
                            <button onclick="cartSuccess()" type="submit" class="btn btn-info">Add to cart</button>
                        </form>
                    </div>
                    <div class="position-absolute discount" style="bottom: -5%; right: -4%">
                        <img src="https://www.pngall.com/wp-content/uploads/2017/11/Starburst-High-Quality-PNG.png" alt="discount-tag" width="60">
                    </div>
                    <div class="position-absolute bottom-0 end-0">
                        <b style="color: white;">{{offer["discount"]}}%<br>off</b>
                    </div>
                </div>
        </div>
    </div>
    <div>
    `,
    data() {
        return {
            offers: '',
            userID : "", 
            buyProudctUrl : ''
        };
    },
    mounted() {
        const base = "/buy-product";
        this.userID = this.$parent.$el.attributes['user-id'].value;
        this.buyProudctUrl = `${base}/${this.userID}?product-name=`;
        
        fetch("http://127.0.0.1:8080//api/offers/"+this.userID)
        .then(response => response.json())
        .then(data => {
            this.offers = data;
        })
        .catch(error => {
            console.error("error encountered ", error);
        });
    },
    computed: {
        returnOffers() {
            return this.offers;
        }, 
        returnBuyProductUrl(){
            return this.buyProudctUrl;
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
            buyProudctUrl : ''
        }
    }, 
    mounted() {
        this.userID = this.$parent.$el.attributes['user-id'].value;
        const base = '/buy-product'; 
        this.buyProudctUrl = `${base}/${this.userID}?product-name=`;
        fetch("http://127.0.0.1:8080//api/product-page/"+this.userID)
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


