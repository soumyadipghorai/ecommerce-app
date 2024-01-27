Vue.component('nav-bar', {
    template : `
        <nav class="navbar navbar-expand-lg px-3 bg-body-tertiary">
            <div class="container-fluid">
                <a class="navbar-brand" :href="formattedProductPage">Ecom App</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <a :href="formattedProductPage" class="btn btn-outline-success mx-3">Home</a>
                    <a href="/logout"><button class="btn btn-outline-danger" type="submit">Log out</button></a>
                </div>
            </div>
        </nav>
    `,
    data() {
        return {
            productUrl : '',
        };
    },
    mounted() {
        const productBase = '/products'
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        this.productUrl = `${productBase}/${resourceId}`
    },
    computed: {
        formattedProductPage(){
            return this.productUrl;
        }
    }
});

Vue.component("cart-section", {
    template : `
    <div class="dashboard-container mt-5">
        <h3>List of items</h3>

        <div v-for="product in returnCart">
            <div class="cart-item-card border bg-light rounded-2 my-3 p-4 row mx-0">
                <div class="col-sm-6">
                    <h4>{{product['product_name']}}</h4>
                    <div class="row">
                        <div class="col-sm-3">
                            <p><b>Quantity: </b>{{product['quantity']}}</p>
                        </div>
                        <div class="col-sm-3">
                            <p><b>Price: </b>{{product['price']}}</p>
                        </div>
                    </div>
                </div>
                <div class="col-sm-6">
                    <form method = 'POST'>
                        <input type="hidden" name="form_name" value="update-quantity">
                        <input type="hidden" name="primary_key" :value="product['cart_id']">
                        <div class="input-section mb-3 mt-2">
                            <label for="quantity">Update Quantity : </label>
                            <input type="number" :max="product['max_quantity']" min="0" name="quantity" id="quantity" required>
                        </div>
                        <div v-if="product['max_quantity'] > 0">
                            <button onclick="updateQuantity()" type="submit" class="btn btn-outline-success">Save</button>
                        </div>
                        <div v-else>
                            <button type="submit" class="btn btn-outline-secondary" disabled>Out of Stock</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <p><b>Total Price : </b> {{totalPrice}}</p>

        <form method="POST" class="buy-all-form mb-5">
            <input type="hidden" name="form_name" value="buy-all-form">
            <button type="submit" class="btn btn-success">Buy All</button>
        </form>
    </div>
        `,
        data() {
            return {
                cart : '', 
                userID : '', 
                totalPrice : ''
            };
        },
        mounted() {
        this.userID = this.$parent.$el.attributes['user-id'].value;
        fetch("http://127.0.0.1:8080//api/cart/"+this.userID)
        .then(response => response.json())
        .then(data => {
            this.totalPrice = data['total_price'], 
            this.cart = data['cart']
        })
        .catch(error => {
            console.error("error encountered ", error);
        });
    },
    computed: {
        returnTotalPrice() {
            return this.totalPrice;
        },
        returnCart(){
            return this.cart;
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
