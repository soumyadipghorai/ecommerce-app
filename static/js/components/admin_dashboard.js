Vue.component('nav-bar', {
    template : `
    <nav class="navbar bg-body-tertiary rounded-2">
        <div class="container-fluid">
            <a class="navbar-brand" :href="formattedUrl"><h4>Admin's, dashboard</h4></a>
            <div>
                <a :href="formattedSummaryPage" class="btn btn-outline-success mx-3">Summary</a>            
                <a href="/logout"><button class="btn btn-outline-danger" type="submit">Log out</button></a>
            </div>
        </div>
    </nav>
    `,
    data() {
        return {
            homeUrl: '',
            summaryUrl : '',
        };
    },
    mounted() {
        const baseUrl = '/admin-dashboard';
        const productBase = '/dashboard'
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        this.homeUrl = `${baseUrl}/${resourceId}`;
        this.summaryUrl = `${productBase}/${resourceId}`
    },
    computed: {
        formattedUrl() {
            return this.homeUrl;
        }, 
        formattedSummaryPage(){
            return this.summaryUrl;
        }
    }
});
  
Vue.component("hero-component", {
    template : `
    <div class="dashboard-container mt-5">
    <div class="hero-data-container">
        <div class="hero-card mx-2 rounded-2 p-3 row m-0">
            <div class="col-sm-9">
                <p class="m-0" style="color: white;"><b>₹{{returnInventory}}</b></p>
                <p>Total Sales</p>
            </div>
            <div class="col-sm-3">
                <div class="icon-dontainer my-auto">
                    <?xml version="1.0" encoding="utf-8"?>
                    <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                    <svg width="40px" height="40px" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                        <title>currency-revenue</title>
                        <g id="Layer_2" data-name="Layer 2">
                            <g id="invisible_box" data-name="invisible box">
                            <rect width="48" height="48" fill="none"/>
                            </g>
                            <g id="Q3_icons" data-name="Q3 icons">
                            <path d="M44,7.1V14a2,2,0,0,1-2,2H35a2,2,0,0,1-2-2.3A2.1,2.1,0,0,1,35.1,12h2.3A18,18,0,0,0,6.1,22.2a2,2,0,0,1-2,1.8h0a2,2,0,0,1-2-2.2A22,22,0,0,1,40,8.9V7a2,2,0,0,1,2.3-2A2.1,2.1,0,0,1,44,7.1Z"/>
                            <path d="M4,40.9V34a2,2,0,0,1,2-2h7a2,2,0,0,1,2,2.3A2.1,2.1,0,0,1,12.9,36H10.6A18,18,0,0,0,41.9,25.8a2,2,0,0,1,2-1.8h0a2,2,0,0,1,2,2.2A22,22,0,0,1,8,39.1V41a2,2,0,0,1-2.3,2A2.1,2.1,0,0,1,4,40.9Z"/>
                            <path d="M24.7,22c-3.5-.7-3.5-1.3-3.5-1.8s.2-.6.5-.9a3.4,3.4,0,0,1,1.8-.4,6.3,6.3,0,0,1,3.3.9,1.8,1.8,0,0,0,2.7-.5,1.9,1.9,0,0,0-.4-2.8A9.1,9.1,0,0,0,26,15.3V13a2,2,0,0,0-4,0v2.2c-3,.5-5,2.5-5,5.2s3.3,4.9,6.5,5.5,3.3,1.3,3.3,1.8-1.1,1.4-2.5,1.4h0a6.7,6.7,0,0,1-4.1-1.3,2,2,0,0,0-2.8.6,1.8,1.8,0,0,0,.3,2.6A10.9,10.9,0,0,0,22,32.8V35a2,2,0,0,0,4,0V32.8a6.3,6.3,0,0,0,3-1.3,4.9,4.9,0,0,0,2-4h0C31,23.8,27.6,22.6,24.7,22Z"/>
                            </g>
                        </g>
                    </svg>
                </div>
            </div>
        </div>
        <div class="hero-card mx-2 rounded-2 p-3 row m-0">
            <div class="col-sm-9">
                <p class="m-0" style="color: white;"><b>₹{{returnInventory}}</b></p>
                <p>Total inventory</p>
            </div>
            <div class="col-sm-3">
                <div class="icon-dontainer my-auto">
                    <?xml version="1.0" encoding="utf-8"?>
                    <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                    <svg width="40px" height="40px" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                        <title>currency-revenue</title>
                        <g id="Layer_2" data-name="Layer 2">
                            <g id="invisible_box" data-name="invisible box">
                            <rect width="48" height="48" fill="none"/>
                            </g>
                            <g id="Q3_icons" data-name="Q3 icons">
                            <path d="M44,7.1V14a2,2,0,0,1-2,2H35a2,2,0,0,1-2-2.3A2.1,2.1,0,0,1,35.1,12h2.3A18,18,0,0,0,6.1,22.2a2,2,0,0,1-2,1.8h0a2,2,0,0,1-2-2.2A22,22,0,0,1,40,8.9V7a2,2,0,0,1,2.3-2A2.1,2.1,0,0,1,44,7.1Z"/>
                            <path d="M4,40.9V34a2,2,0,0,1,2-2h7a2,2,0,0,1,2,2.3A2.1,2.1,0,0,1,12.9,36H10.6A18,18,0,0,0,41.9,25.8a2,2,0,0,1,2-1.8h0a2,2,0,0,1,2,2.2A22,22,0,0,1,8,39.1V41a2,2,0,0,1-2.3,2A2.1,2.1,0,0,1,4,40.9Z"/>
                            <path d="M24.7,22c-3.5-.7-3.5-1.3-3.5-1.8s.2-.6.5-.9a3.4,3.4,0,0,1,1.8-.4,6.3,6.3,0,0,1,3.3.9,1.8,1.8,0,0,0,2.7-.5,1.9,1.9,0,0,0-.4-2.8A9.1,9.1,0,0,0,26,15.3V13a2,2,0,0,0-4,0v2.2c-3,.5-5,2.5-5,5.2s3.3,4.9,6.5,5.5,3.3,1.3,3.3,1.8-1.1,1.4-2.5,1.4h0a6.7,6.7,0,0,1-4.1-1.3,2,2,0,0,0-2.8.6,1.8,1.8,0,0,0,.3,2.6A10.9,10.9,0,0,0,22,32.8V35a2,2,0,0,0,4,0V32.8a6.3,6.3,0,0,0,3-1.3,4.9,4.9,0,0,0,2-4h0C31,23.8,27.6,22.6,24.7,22Z"/>
                            </g>
                        </g>
                    </svg>
                </div>
            </div>
        </div>
        <div class="hero-card mx-2 rounded-2 p-3 row m-0">
            <div class="col-sm-9">
                <p class="m-0" style="color: white;"><b>{{returnItems}}</b></p>
                <p>Total Products</p>
            </div>
            <div class="col-sm-3">
                <div class="icon-dontainer my-auto">
                    <?xml version="1.0" encoding="utf-8"?>
                    <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                    <svg width="40px" height="40px" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                        <title>currency-revenue</title>
                        <g id="Layer_2" data-name="Layer 2">
                            <g id="invisible_box" data-name="invisible box">
                            <rect width="48" height="48" fill="none"/>
                            </g>
                            <g id="Q3_icons" data-name="Q3 icons">
                            <path d="M44,7.1V14a2,2,0,0,1-2,2H35a2,2,0,0,1-2-2.3A2.1,2.1,0,0,1,35.1,12h2.3A18,18,0,0,0,6.1,22.2a2,2,0,0,1-2,1.8h0a2,2,0,0,1-2-2.2A22,22,0,0,1,40,8.9V7a2,2,0,0,1,2.3-2A2.1,2.1,0,0,1,44,7.1Z"/>
                            <path d="M4,40.9V34a2,2,0,0,1,2-2h7a2,2,0,0,1,2,2.3A2.1,2.1,0,0,1,12.9,36H10.6A18,18,0,0,0,41.9,25.8a2,2,0,0,1,2-1.8h0a2,2,0,0,1,2,2.2A22,22,0,0,1,8,39.1V41a2,2,0,0,1-2.3,2A2.1,2.1,0,0,1,4,40.9Z"/>
                            <path d="M24.7,22c-3.5-.7-3.5-1.3-3.5-1.8s.2-.6.5-.9a3.4,3.4,0,0,1,1.8-.4,6.3,6.3,0,0,1,3.3.9,1.8,1.8,0,0,0,2.7-.5,1.9,1.9,0,0,0-.4-2.8A9.1,9.1,0,0,0,26,15.3V13a2,2,0,0,0-4,0v2.2c-3,.5-5,2.5-5,5.2s3.3,4.9,6.5,5.5,3.3,1.3,3.3,1.8-1.1,1.4-2.5,1.4h0a6.7,6.7,0,0,1-4.1-1.3,2,2,0,0,0-2.8.6,1.8,1.8,0,0,0,.3,2.6A10.9,10.9,0,0,0,22,32.8V35a2,2,0,0,0,4,0V32.8a6.3,6.3,0,0,0,3-1.3,4.9,4.9,0,0,0,2-4h0C31,23.8,27.6,22.6,24.7,22Z"/>
                            </g>
                        </g>
                    </svg>
                </div>
            </div>
        </div>
    </div>
</div>
    `,

    data() {
        return {
            sales : '', 
            inventory : '', 
            items : '',
            userid : '', 
            catgoryList : ''
        };
    },
    mounted() {
        this.userid = this.$parent.$el.attributes['user-id'].value;
        fetch("http://127.0.0.1:8080//api/admin/"+this.userid)
        .then(response => response.json())
        .then(data => {
            this.sales = data['sales'],
            this.items = data['items'],
            this.inventory = data['inventory'],
            this.catgoryList = data['catgoryList']
        })
        .catch(error => {
            console.error("error encountered ", error);
        })
    },
    computed: {
        returnSales() {
            return this.sales;
        }, 
        returnItems() {
            return this.items;
        }, 
        returnInventory() {
            return this.inventory;
        }, 
        returnCategoryList(){
            return this.catgoryList
        }, 
        returnUserID(){
            return this.userid
        }
    }
});

Vue.component("main-dashboard-body", {
    template : `
    <div class="dashboard-container mt-5">
        <div class="category-card-container my-2" v-for="(category, categoryNameAPI) in returncatgoryList">
            <div class="category-container p-4 w-100 bg-light mx-2 t-3 p-2 border rounded-2">
                <form action="" method = "POST">
                    <input type="hidden" name="form_name" value="category-edit-form">
                    <input type="hidden" name="category-to-edit" :value="categoryNameAPI">
                    <div class="row" style="width: max-content;">
                        <div class="col-4">
                            <h4 class="my-2">{{categoryNameAPI}}</h4>
                        </div>
                        <div class="col-8" :id="categoryNameAPI">
                            <input @click="insertInputBox(categoryName = categoryNameAPI)" class="btn btn-outline-success py-0 px-2 mt-2" value="Edit" style="width: 50%;">
                        </div>
                    </div>
                </form>
                <div class="poduct-container mb-2 h-25" v-for="product in category">
                    <div class="available-product p-2 rounded-2 my-2 row bg-body-secondary">
                        <div class="col-sm-5">
                            <p class="m-0">{{product['product-name']}}</p>
                        </div>
                        <div class="col-sm-3">
                            <p class="m-0 p-2 border rounded-2 bg-white" style="color: black;">{{product['product-quantity']}}</p>
                        </div>
                        <div class="col-sm-4">
                            <form action="" method = "POST">
                                <input type="hidden" name="form_name" value="product-delete-form">
                                <input type="hidden" name="product" :value="product['product-name']">
                                <input onclick="deleteWarningProduct()" class="btn btn-outline-danger mx-2" type="submit" value="Delete" id="{{product['product-name']}}">
                            </form>
                        </div>
                    </div>
                </div>
                <form action="" method = 'POST'>
                    <input type="hidden" name="form_name" value="category-delete-form">
                    <input type="hidden" name="category" :value="categoryNameAPI">
                    <a class="btn btn-outline-warning" :href="returnEditUrl+categoryNameAPI">Edit</a>
                    <input onclick="deleteWarning()" class="btn btn-outline-danger mx-2" type="submit" value="Delete">
                </form>
            </div>
        </div>
        <a :href="returnaddCategoryUrl" class="btn btn-outline-success mx-2 my-3">Add Category</a>
    </div>
    `, 
    data(){
        return {
            catgoryList : '',
            addCategoryUrl : '',
            editUrl : ''
        }
    }, 
    mounted() {
        this.userid = this.$parent.$el.attributes['user-id'].value;
        const baseUrl = '/add-category'; 
        const baseEditUrl = '/add-product'; 
        this.addCategoryUrl = `${baseUrl}/${this.userid}`;
        this.editUrl = `${baseEditUrl}/${this.userid}?category=`;
        fetch("http://127.0.0.1:8080//api/admin/"+this.userid)
        .then(response => response.json())
        .then(data => {
            this.catgoryList = data['catgoryList']
        })
    }, 
    computed : {
        returncatgoryList() {
            return this.catgoryList;
        }, 
        returnaddCategoryUrl(){
            return this.addCategoryUrl;
        }, 
        returnEditUrl(){
            return this.editUrl
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


