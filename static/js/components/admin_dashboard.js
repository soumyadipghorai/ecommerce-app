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
                <p class="m-0" style="color: white;"><b>₹{{returnSales}}</b></p>
                <p>Total Sales</p>
            </div>
            <div class="col-sm-3">
                <div class="icon-dontainer my-auto">
                    <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                    <svg width="40" height="40" viewBox="0 0 1024 1024" class="icon"  version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M829.06 73.14h-6.48c-30.41 0-58.57 17.11-75.34 45.75-6.12 10.46-22.29 11.71-29.96 2.43-25.52-31.07-59.41-48.18-95.64-48.18-35.98 0-69.86 17.11-95.41 48.18-6.98 8.5-21.25 8.52-28.27-0.02-25.55-31.05-59.43-48.16-95.41-48.16s-69.86 17.11-95.41 48.18c-7.66 9.36-23.82 8.05-29.95-2.43-16.8-28.64-44.96-45.75-75.36-45.75h-7.23c-46.89 0-85.05 38.16-85.05 85.05V865.8c0 46.89 38.16 85.05 85.05 85.05h7.23c30.39 0 58.55-17.11 75.38-45.79 6.07-10.45 22.23-11.79 29.93-2.38 25.55 31.05 59.43 48.16 95.41 48.16s69.86-17.11 95.41-48.18c7.02-8.52 21.29-8.5 28.27 0.02 25.55 31.05 59.43 48.16 95.66 48.16 35.98 0 69.88-17.11 95.38-48.14 7.73-9.36 23.89-8 29.96 2.36 16.79 28.68 44.95 45.79 75.36 45.79h6.48c46.89 0 85.05-38.16 85.05-85.05V158.2c0-46.9-38.17-85.06-85.06-85.06z m11.91 792.66c0 6.57-5.34 11.91-11.91 11.91h-6.48c-6.14 0-10.91-7.34-12.23-9.61-16.36-27.91-46.61-45.25-78.93-45.25-27.43 0-53.16 12.16-70.64 33.39-6.59 8.02-20.41 21.46-39.14 21.46-18.48 0-32.32-13.46-38.91-21.46-34.84-42.45-106.39-42.46-141.27-0.02-6.59 8.02-20.43 21.48-38.91 21.48-18.48 0-32.32-13.46-38.91-21.46-17.43-21.23-43.18-33.39-70.62-33.39-32.36 0-62.61 17.36-78.93 45.25-1.32 2.25-6.11 9.61-12.25 9.61h-7.23c-6.57 0-11.91-5.34-11.91-11.91V158.2c0-6.57 5.34-11.91 11.91-11.91h7.23c6.14 0 10.93 7.36 12.23 9.57 16.34 27.93 46.59 45.29 78.95 45.29 27.45 0 53.2-12.16 70.62-33.38 6.59-8.02 20.43-21.48 38.91-21.48 18.48 0 32.32 13.46 38.91 21.46 34.88 42.48 106.43 42.43 141.27 0.02 6.59-8.02 20.43-21.48 39.16-21.48 18.48 0 32.3 13.45 38.91 21.5 17.46 21.2 43.2 33.36 70.62 33.36 32.32 0 62.57-17.34 78.95-45.29 1.3-2.23 6.07-9.57 12.21-9.57h6.48c6.57 0 11.91 5.34 11.91 11.91v707.6z" fill="#0F1F3C" /><path d="M255.93 548.66h365.71v73.14H255.93zM255.92 694.93h511.82v73.14H255.92zM621.54 329.23h58l-83.85 83.86 51.71 51.71 83.86-83.85v58h73.14V256.09H621.54z" fill="#0F1F3C" /></svg>
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
                    <svg fill="#000000" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                            width="40" height="40" viewBox="0 0 256 253" enable-background="new 0 0 256 253" xml:space="preserve">
                    <path d="M122,219H76v-45h18v14h10v-14h18V219z M182,219h-46v-45h18v14h10v-14h18V219z M152,160h-46v-45h18v14h10v-14h18V160z M2,69
                        c0,13.678,9.625,25.302,22,29.576V233H2v18h252v-18h-22V98.554c12.89-3.945,21.699-15.396,22-29.554v-8H2V69z M65.29,68.346
                        c0,6.477,6.755,31.47,31.727,31.47c21.689,0,31.202-19.615,31.202-31.47c0,11.052,7.41,31.447,31.464,31.447
                        c21.733,0,31.363-20.999,31.363-31.447c0,14.425,9.726,26.416,22.954,30.154V233H42V98.594C55.402,94.966,65.29,82.895,65.29,68.346
                        z M222.832,22H223V2H34v20L2,54h252L222.832,22z"/>
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
                    <?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                    <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M3.04047 2.29242C2.6497 2.15503 2.22155 2.36044 2.08416 2.7512C1.94678 3.14197 2.15218 3.57012 2.54295 3.7075L2.80416 3.79934C3.47177 4.03406 3.91052 4.18961 4.23336 4.34802C4.53659 4.4968 4.67026 4.61723 4.75832 4.74609C4.84858 4.87818 4.91828 5.0596 4.95761 5.42295C4.99877 5.80316 4.99979 6.29837 4.99979 7.03832L4.99979 9.64C4.99979 12.5816 5.06302 13.5523 5.92943 14.4662C6.79583 15.38 8.19028 15.38 10.9792 15.38H16.2821C17.8431 15.38 18.6236 15.38 19.1753 14.9304C19.727 14.4808 19.8846 13.7164 20.1997 12.1875L20.6995 9.76275C21.0466 8.02369 21.2202 7.15417 20.7762 6.57708C20.3323 6 18.8155 6 17.1305 6H6.49233C6.48564 5.72967 6.47295 5.48373 6.4489 5.26153C6.39517 4.76515 6.27875 4.31243 5.99677 3.89979C5.71259 3.48393 5.33474 3.21759 4.89411 3.00139C4.48203 2.79919 3.95839 2.61511 3.34187 2.39838L3.04047 2.29242ZM10.2395 8.87473C10.1703 8.46633 9.78312 8.19135 9.37473 8.26054C8.96633 8.32972 8.69135 8.71688 8.76054 9.12527L9.28872 12.2431C9.35791 12.6515 9.74507 12.9265 10.1535 12.8573C10.5619 12.7881 10.8368 12.401 10.7677 11.9926L10.2395 8.87473ZM15.6536 8.26054C15.2452 8.19135 14.858 8.46633 14.7889 8.87473L14.2607 11.9926C14.1915 12.401 14.4665 12.7881 14.8749 12.8573C15.2833 12.9265 15.6704 12.6515 15.7396 12.2431L16.2678 9.12527C16.337 8.71688 16.062 8.32972 15.6536 8.26054ZM7.5 18C8.32843 18 9 18.6716 9 19.5C9 20.3284 8.32843 21 7.5 21C6.67157 21 6 20.3284 6 19.5C6 18.6716 6.67157 18 7.5 18ZM16.5 18.0001C17.3284 18.0001 18 18.6716 18 19.5001C18 20.3285 17.3284 21.0001 16.5 21.0001C15.6716 21.0001 15 20.3285 15 19.5001C15 18.6716 15.6716 18.0001 16.5 18.0001Z" fill="#1C274C"/>
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
                <div class="poduct-container my-2 h-100" v-for="product in category">
                    <div class="available-product p-2 rounded-2 row bg-body-secondary">
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


