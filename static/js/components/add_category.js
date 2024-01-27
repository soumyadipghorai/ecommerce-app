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
        <div class="category-form-container shadow border row h-100">
            <div class="col-sm-7 p-sm-4 p-md-5 text-section">
                <div class="text-section mt-5 mb-4">
                    <h2 class="m-2 lh-1">Create New category</h2>
                    <p class="m-2 section-description">You can create New category here by entering the new category and pressing the create button. Make Sure that the category is not already present.</p>
                </div>
                <form :action="formattedHomePage" method = 'POST' class="m-2">
                    <input type="hidden" name="form_name" value="category-form">
                    <label for="category"><p class="m-0">Category Name :</p></label>
                    <input type="text" name="categoryName" id="categoryName" placeholder="Enter Category Name..." class="mb-3 w-75 p-2 rounded-2 border-1" required> 
                    <div class="button-container">
                        <input type="submit" value="Create" class="btn btn-success px-3">
                    </div>
                </form>
            </div>
            <div class="col-sm-5 img-section">
                
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            homepage : '', 
            message : ''
        };
    },
    mounted() {
        const homePageBase = '/add-category';
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        this.homepage = `${homePageBase}/${resourceId}`
        this.message = this.$parent.$el.attributes['message'].value
    },
    computed: {
        formattedHomePage(){
            return this.homepage;
        }, 
        returnMessage(){
            return this.message
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


