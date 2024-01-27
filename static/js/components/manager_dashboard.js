Vue.component('nav-bar', {
    template : `
    <nav class="navbar navbar-expand-lg px-3 bg-body-tertiary rounded-2">
        <div class="container-fluid">
            <a class="navbar-brand" :href="formattedUrl"><h4>Manager's, dashboard</h4></a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup"> 
                <form action="" method = 'POST'>
                    <input type="hidden" name="form_name" value="logout-form"> 
                    <a href="/logout"><button class="btn btn-outline-danger" type="submit">Log out</button></a>
                </form>     
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
        const baseUrl = '/manager-dashboard'; 
        const resourceId = this.$parent.$el.attributes['user-id'].value;
        this.homeUrl = `${baseUrl}/${resourceId}`; 
    },
    computed: {
        formattedUrl() {
            return this.homeUrl;
        }
    }
});

Vue.component("delete-request", {
    template : `
    <div class="pending-resquest-container bg-light mt-5 p-4 rounded-2">
        <h5 class="my-2">Category Delete request</h5>
        <div v-for="category in returnCategoryList">
            <div class="bg-white rounded-2 border">
                <div class="row p-4">
                    <div class="col-6">
                        <h6>{{category["name"]}}</h6>
                    </div>
                    <div class="col-6">
                        <form action="" method = 'POST'>
                            <input type="hidden" name="form_name" value="delete-category"> 
                            <input type="hidden" name="category-id" :value='category["id"]'>
                            <button class="btn btn-danger">Delete</button>
                        </form> 
                    </div>
                </div>
            </div>
        </div>
    </div>
    `, 
    data() {
        return {
            categoryToDelete : ''
        }
    },  
    mounted() {
        this.userID = this.$parent.$el.attributes["user-id"].value;
        fetch("http://127.0.0.1:8080/api/manager-approval/"+this.userID)
        .then(response => response.json())
        .then(data => {
            this.categoryToDelete = data;
        })
    }, 
    computed : {
        returnCategoryList() {
            return this.categoryToDelete;
        }
    }
})

Vue.component("add-request", {
    template : `
    <div class="pending-resquest-container bg-light mt-5 p-4 rounded-2">
        <h5 class="my-2">Category Add request</h5>
        <div v-for="category in returnCategoryList">
            <div class="bg-white rounded-2 border">
                <div class="row p-4">
                    <div class="col-6">
                        <h6>New Category : {{category["name"]}}</h6>
                    </div>
                    <div class="col-6">
                        <form action="" method = 'POST'>
                            <input type="hidden" name="form_name" value="add-category"> 
                            <input type="hidden" name="category-name" :value='category["name"]'>
                            <input type="hidden" name="pending-id" :value='category["id"]'>
                            <button class="btn btn-success">Add</button>
                        </form> 
                    </div>
                </div>
            </div>
        </div>
    </div>
    `, 
    data() {
        return {
            categoryToAdd : ''
        }
    },  
    mounted() {
        this.userID = this.$parent.$el.attributes["user-id"].value;
        fetch("http://127.0.0.1:8080/api/add-caetgory-approval/"+this.userID)
        .then(response => response.json())
        .then(data => {
            this.categoryToAdd = data;
        })
    }, 
    computed : {
        returnCategoryList() {
            return this.categoryToAdd;
        }
    }
})

Vue.component("edit-request", {
    template : `
    <div class="pending-resquest-container bg-light mt-5 p-4 rounded-2">
        <h5 class="my-2">Category Edit request</h5>
        <div v-for="category in returnCategoryList">
            <div class="bg-white rounded-2 border">
                <div class="row p-4">
                    <div class="col-3">
                        <h6>old name : {{category["old_name"]}}</h6>
                    </div>
                    <div class="col-3">
                        <h6>new name : {{category["new_name"]}}</h6>
                    </div>
                    <div class="col-6">
                        <form action="" method = 'POST'>
                            <input type="hidden" name="form_name" value="edit-category"> 
                            <input type="hidden" name="category-id" :value='category["category_id"]'>
                            <input type="hidden" name="old-category-name" :value='category["old_name"]'>
                            <input type="hidden" name="new-category-name" :value='category["new_name"]'>
                            <input type="hidden" name="pending-id" :value='category["id"]'>
                            <button class="btn btn-warning">Edit</button>
                        </form> 
                    </div>
                </div>
            </div>
        </div>
    </div>
    `, 
    data() {
        return {
            categoryToEdit : ''
        }
    },  
    mounted() {
        this.userID = this.$parent.$el.attributes["user-id"].value;
        fetch("http://127.0.0.1:8080/api/edit-category-approval/"+this.userID)
        .then(response => response.json())
        .then(data => {
            this.categoryToEdit = data;
        })
    }, 
    computed : {
        returnCategoryList() {
            return this.categoryToEdit;
        }
    }
})

new Vue({
    el: '#app', 
    delimiters : ['${', '}'],
    data: function(){
        return {
            msg : "hello world from vue"
        }
    } 
});
