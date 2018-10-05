Vue.component('all-reg-forms', {
    props: ['pk', 'date', 'money', 'kind', 'tx_op', 'brokerage'],
    template:`
            <div class="form-inline m-0 p-0">
                <input type="hidden" id="pk" name="pk" :value="pk">
                <div>
                <input type="date" id="date" class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :value="date"
                       disabled="true">
                </div>

                <div>
                <input type="text" id="money" class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :value="money"
                       disabled="true">
                </div>

                <div>
                <input type="text"  id="kind" name="kind" class="form-inline m-0 p-0 bg-light"
                       size="40" style="font-size:10px;border:none"
                       :value="kind"
                       disabled="true">
                </div>

                <div>
                <input type="text" id="tx_op" class="form-inline m-0 p-0 bg-light"
                       size="8" style="font-size:10px;border:none"
                       :value="tx_op"
                       disabled="true">
                </div>

                <div>
                <input type="text" id="brokerage" class="form-inline m-0 p-0 bg-light"
                       size="15" style="font-size:10px;border:none"
                       :value="brokerage"
                       disabled="true">
                </div>
                <div v-if= "kind != '---'" class="form-inline m-0 p-0">
                <button type="submit" class="btn btn-sm m-0 p-0 btn-link" size="8">remove</button>
                </div>
            </div>
    `,
    // all this for update is not necessary anymore. DELETE ONLY
     data: function() {
         return {
             text: ''
         }
    },
});

new Vue({
    el: "#vue_ajax",
    methods: {
        submitForm: function(event) {
            var form = {}
            form["pk"] = event.target.pk.value

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";


            // tem que ser delete
            axios({
                method: 'delete',
                url: 'api/' + form["pk"] + '/',
                data: {}
            }).then(response => {
                console.log("HERE")
                // if ( http_verb == 'delete') {
                document.getElementById(form["pk"]).remove()
                //}
                // Update line1 data missing
            })
            // .catch errors
        }
    }
})
