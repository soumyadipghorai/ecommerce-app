Vue.component('nav-bar', {
    template : `
    <nav class="navbar navbar-expand-lg bg-body-tertiary px-3">
        <div class="container-fluid">
            <a class="navbar-brand" :href="formattedProductPage">Admin's Dashboard</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <a :href="formattedUrl" class="btn btn-outline-success mx-3">Summary</a>
                <a href="/logout"><button class="btn btn-outline-danger" type="submit">Log out</button></a>
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
        const baseUrl = '/dashboard';
        const adminBase = '/admin-dashboard'
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
        }
    }
});
  
Vue.component("dashboard", {
    template : `
    <div class="dashboard-container mt-5">
        <div class="category-card-container rounded-2 bg-light mb-3" style="height: fit-content;">
            <div class="row">
                <div class="col-5 m-3">
                    <img class="rounded-2 img-fluid w-100" src="/static/images/category-wise-sale.png" alt="" width="400">
                </div>
                <div class="col-5 m-3">
                    <img class="rounded-2 img-fluid w-100" src="/static/images/category-wise-stock.png" alt="" width="400">
                </div>
            </div>
        </div>

        <a :href="returnHome" class="btn btn-outline-success">Go to Home</a>
        <a href="/static/data/order_data.csv" class="btn btn-danger">Export</a>
    </div>
    `,
    data() {
        return {
            home: '',
        };
    },
    mounted() {
        const base = "/admin-dashboard";
        const userID = this.$parent.$el.attributes['product-name'].value;
        this.home = `${base}/${userID}`;
    },
    computed: {
        returnHome() {
            return this.home;
        }
    }
});

new Vue({
    el: '#app', 
    delimiters : ['${', '}'],
});


