Vue.component('all-reg-forms', {
    props: ['pk', 'date', 'money', 'kind', 'which_target', 'tx_op', 'brokerage'],
    template:`
            <div class="form-inline m-0 p-0">
                <input type="hidden" id="pk" name="pk" :value="pk">
                <div @input="n_dt">
                <input type="date" id="date" class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :value="dt"
                       :disabled="edit">
                </div>

                <div @input="n_mn">
                <input type="text" id="money" class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :value="mn"
                       :disabled="edit">
                </div>

                <div @input="n_knd">
                <input type="text"  id="kind" name="kind" class="form-inline m-0 p-0 bg-light"
                       size="15" style="font-size:10px;border:none"
                       :value="knd"
                       :disabled="edit">
                </div>

                <div @input="n_whch_trgt">
                <input type="text" id="which_target" class="form-inline m-0 p-0 bg-light"
                       size="15" style="font-size:10px;border:none"
                       :value="whch_trgt"
                       :disabled="edit">
                </div>

                <div @input="n_txop">
                <input type="text" id="tx_op" class="form-inline m-0 p-0 bg-light"
                       size="8" style="font-size:10px;border:none"
                       :value="txop"
                       :disabled="edit">
                </div>

                <div @input="n_brkrg">
                <input type="text" id="brokerage" class="form-inline m-0 p-0 bg-light"
                       size="15" style="font-size:10px;border:none"
                       :value="brkrg"
                       :disabled="edit">
                </div>
                <div v-if= "kind != '---' && which_target != '---'" class="form-inline m-0 p-0">
                <input type="checkbox" id="checkbox" v-model:value="chk" v-bind="label()" >
                <span class="form-text text-muted" style="font-size:9px">update</span>
                <button type="submit" class="btn btn-sm m-0 p-0 btn-link" size="8" id="button" @click="dflt()">{{ method }}</button>
                </div>
            </div>
    `,
     data: function() {
         return {
             method: 'delete',
             edit: true,
             chk: false,
             brkrg: this.brokerage,
             txop: this.tx_op,
             whch_trgt: this.which_target,
             knd: this.kind,
             mn: this.money,
             dt: this.date
         }
    },
    methods:{
        n_brkrg: function(event) {
            this.brkrg = event.target.value
        },
        n_txop: function(event) {
            this.txop = event.target.value
        },
        n_whch_trgt: function(event) {
            this.whch_trgt = event.target.value
        },
        n_knd: function(event) {
            this.knd = event.target.value
        },
        n_mn: function(event) {
            this.mn = event.target.value
        },
        n_dt: function(event) {
            this.dt = event.target.value
        },
        dflt: function() {
            this.chk = false
        },

        label: function(){
            this.method = this.chk ? 'update' : 'delete';
            this.edit = this.chk == false ? true : false
        },
    },
});

new Vue({
    el: "#vue_ajax",
    methods: {
        submitForm: function(pk, old_money, event) {
            var form = {}
            form["tx_op"] = Number(event.target.tx_op.value);
            form["brokerage"] = event.target.brokerage.value;
            form["basic_data"] = {
                 "date": event.target.date.value,
                 "money": Number(event.target.money.value),
                 "kind": event.target.kind.value,
                 "which_target": event.target.which_target.value,
                 //pk': pk
            }

            event.target.checkbox.checked = false

            http_verb = event.target.button.innerText
            http_verb = http_verb == 'delete' ? 'delete' : 'put'
            event.target.button.innerText = 'delete'

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";


            // tem que ser put e delete
            axios({
                method: http_verb,
                url: 'api/' + pk + '/',
                data: form
            }).then(response => {
                console.log("HERE")
                if ( http_verb == 'delete') {
                    document.getElementById(pk).remove()
                }
            })
            // .catch errors
        }
    }
})
