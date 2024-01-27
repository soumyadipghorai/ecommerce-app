Vue.component('nav-bar', {
    template : `
    <nav class="navbar navbar-expand-lg px-3 bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" :href="formattedProductPage">Ecom App</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <a :href="formattedUrl" class="btn btn-outline-success mx-3">Cart</a>
                <a href="/logout"><button class="btn btn-outline-danger" type="submit">Log out</button></a>
            </div>
        </div>
    </nav>
    `,
    data() {
        return {
            cartUrl: '',
            productUrl : '',
        };
    },
    mounted() {
        const baseUrl = '/cart';
        const productBase = '/products'
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        this.cartUrl = `${baseUrl}/${resourceId}`;
        this.productUrl = `${productBase}/${resourceId}`
    },
    computed: {
        formattedUrl() {
            return this.cartUrl;
        }, 
        formattedProductPage(){
            return this.productUrl;
        }
    }
});
  
Vue.component("buy-product", {
    template : `
    <div class="dashboard-container mt-5 shadow border row mx-0" style="border-radius: 10px;" >
        <div class="contegory-form-container p-4 col-md-6">
            <h2 class="m-2">Buy {{returnProductName}}</h2>
            <p class="m-2 mb-5">Shop Smarter, Eat Fresher – Your Cart, Your Culinary Adventure!</p>

            <form method = 'POST' class="m-2">
                <input type="hidden" name="form_name" value="buy-product">
                <div class="my-3">
                    <p>Price per unit : <b>{{returnProductPrict}}/-</b></p>
                    <p>Units available : <b>{{returnMaxLimit}}</b></p>
                </div>
                <div class="my-3 mb-0">
                    <label class="mb-2" for="quantity">Enter Quantity:</label>
                    <input class="form-control mb-4" type="number" name= 'quantity' id = 'quantity' min="0" :max="maxLimit" :placeholder="maxLimit" required>
                </div>
                <div class="my-3 mb-2">
                    <p>Total : <span class="totalPrice" id="totalPrice">0</span></p>
                </div>
                <div class="my-3">
                    <button onclick="checkTotal()" type="button" class="btn btn-outline-success py-2 px-3">Check total</button>
                    <input type="submit" value="Buy" class="btn-success btn py-2 px-5">
                </div>
            </form>
            <div :product-name="productNameAPI"></div>
        </div>
        <div class="col-md-6 image-section">
    
        </div>
    </div>
    `,
    data() {
        return {
            productName: '',
            productPrice : '',
            maxLimit : '',
            cartUrl : '', 
            productID : '',
            productNameAPI : 'ajdcn', 
            productPriceAPI : 'ajdc'
        };
    },
    mounted() {
        this.productName = this.$parent.$el.attributes['product-name'].value;
        this.productPrice = this.$parent.$el.attributes['product-price'].value;
        this.maxLimit = this.$parent.$el.attributes['max-limit'].value;
        fetch("http://localhost:8080/api/category/"+this.productName)
        .then(response => response.json())
        .then(data => {
            this.productNameAPI = data['name'],
            this.productPriceAPI = data['price']
        })
        .catch(error => {
            console.error("error encountered ", error);
        })
        
        console.log(this.productNameAPI, this.productPriceAPI)
    },
    computed: {
        returnProductName() {
            return this.productName;
        }, 
        returnProductPrict(){
            return this.productPrice
        },
        returnMaxLimit(){
            return this.maxLimit
        }
    }
});

new Vue({
    el: '#app', 
    delimiters : ['${', '}'],
    data: function(){
        return {
            msg : "hello world from vue"
        }
    } 
});


