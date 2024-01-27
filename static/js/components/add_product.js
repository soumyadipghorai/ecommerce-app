Vue.component('nav-bar', {
    template : `
    <nav class="navbar navbar-expand-lg bg-body-tertiary px-3">
        <div class="container-fluid">
            <a class="navbar-brand" :href="formattedHomePage">Admin Dashboard</a>
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
            dashboard: '',
            homepage : '',
        };
    },
    mounted() {
        const baseUrl = '/dashboard';
        const homePageBase = '/admin-dashboard';
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        this.dashboard = `${baseUrl}/${resourceId}`;
        this.homepage = `${homePageBase}/${resourceId}`
    },
    computed: {
        formattedUrl() {
            return this.dashboard;
        }, 
        formattedHomePage(){
            return this.homepage;
        }
    }
});
  
Vue.component("add-product", {
    template : `
    <div class="dashboard-container mt-5">
        <div class="contegory-form-container shadow w-75 border row">
            <div class="col-sm-7 p-sm-4 p-md-5">
                <h2 class="m-2">Edit products in {{returnCategoryName}}</h2>
                <p class="m-2">To edit the existing product enter the existing product name and enter the new details. For New product add all the details from scratch.</p>
                <form :action="formatFormAction" method = 'POST' class="m-2">
                    <input type="hidden" name="form_name" value="product-form">
                    <div class="row">
                        <div class="col-sm-6">
                            <div class="my-3">
                                <label for="productName">Product Name:</label>
                                <input class="form-control w-100" type="text" name= 'productName' id = 'productName' required>
                            </div>
                            <div class="my-3">
                                <label for="unit">unit:</label>
                                <select name="unit" id="unit" class="form-control w-100" required>
                                    <option value="rs_per_kg">rs/kg</option>
                                    <option value="rs_per_litre">rs/lt</option>
                                    <option value="rs_per_pc">rs/pc</option>
                                    <option value="rs_per_packet">rs/packet</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-sm-6">
                            <div class="my-3">
                                <label for="price">Price:</label>
                                <input class="form-control w-100" type="number" name= 'price' id = 'price' min="0" required>
                            </div>
                            <div class="my-3">
                                <label for="quantity">Quantity:</label>
                                <input class="form-control w-100" type="number" name= 'quantity' id = 'quantity' min="0" required>
                            </div>
                        </div>
                        <div class="my-3">
                            <input type="submit" value="Save" class="btn btn-success">
                        </div>
                    </div>
                </form>
            </div>
            <div class="col-sm-5 image-section"></div>
        </div>
    </div>
    `,
    data() {
        return {
            formAction : '', 
            category : ''
        };
    },
    mounted() {
        const homePageBase = '/add-product';
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        const categoryName = this.$parent.$el.attributes['category'].value;
        this.category = categoryName;
        this.formAction = `${homePageBase}/${resourceId}?category=${categoryName}`;
    },
    computed: {
        formatFormAction(){
            return this.formAction;
        },
        returnCategoryName(){
            return this.category
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


