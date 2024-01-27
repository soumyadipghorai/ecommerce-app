Vue.component('nav-bar', {
    template: `
    <nav class="navbar bg-body-tertiary mx-4">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">Ecom App</a>
            <div>
                <a :href="formattedUrl" class="btn btn-outline-success mx-3">admin-page</a>
                <a :href="formattedManagerUrl" class="btn btn-outline-success mx-3">manager-page</a>
                <a href="/logout"><button class="btn btn-outline-danger" type="submit">Log out</button></a>
            </div>
        </div>
    </nav>
    `,
    data() {
        return {
            apiUrl: '',  
            managerURL : ''
        };
    },
    mounted() {
        const baseUrl = '/admin-dashboard';
        const managerBase = '/manager-dashboard'
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        this.apiUrl = `${baseUrl}/${resourceId}`;
        this.managerURL = `${managerBase}/${resourceId}`;
    },
    computed: {
        formattedUrl() {
            return this.apiUrl;
        }, 
        formattedManagerUrl() {
            return this.managerURL;
        }
    }
});
  

  
Vue.component("landing-page-section", {
    template : `
    <div class="herosection m-0">
        <div class="row" style="margin:6%;">
            <div class="col-6 text-section p-4">
                <div> 
                    <h1 class="lh-1 text-body-emphasis my-3">Fresh Delights Delivered to Your Doorstep: Shop Now!</h1>
                    <p class="mb-4">Discover convenience and quality at your fingertips with our online grocery store. Browse a diverse selection of fresh produce, pantry staples, and more. Shop from home and experience hassle-free delivery, ensuring your kitchen is always stocked with the finest essentials.
                    </p>
                    <a :href="formattedUrl">
                        <button class="btn btn-primary">Shop Now</button>
                    </a>
                </div>
            </div>
            <div class="col-6 img-section p-4">
                <div class="bg-dark w-40 h-40"></div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            apiUrl: ''
        };
    },
    mounted() {
        const baseUrl = '/products';
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        this.apiUrl = `${baseUrl}/${resourceId}`;
    },
    computed: {
        formattedUrl() {
            return this.apiUrl;
        }
    }
})

new Vue({
    el: '#app'
});
