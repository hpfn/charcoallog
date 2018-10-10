Vue.component('all-reg-forms', {
    props: ['pk', 'date', 'money', 'kind', 'tx_op', 'brokerage'],
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
                <input type="number" id="money" name="money" step="0.01" class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :value="mn"
                       :disabled="edit">
                </div>

                <div @input="n_knd">
                <input type="text"  id="kind" name="kind" class="form-inline m-0 p-0 bg-light"
                       size="40" style="font-size:10px;border:none"
                       :value="knd"
                       :disabled="edit">
                </div>

                <div @input="n_tx_p">
                <input type="text"  id="tx_op" name="tx_op" class="form-inline m-0 p-0 bg-light"
                       size="6" style="font-size:10px;border:none"
                       :value="tx_p"
                       :disabled="edit">
                </div>
                
                <div @input="n_brkrg">
                <input type="text" id="brokerage" class="form-inline m-0 p-0 bg-light"
                       size="15" style="font-size:10px;border:none"
                       :value="brkrg"
                       :disabled="edit">
                </div>

                <div class="form-inline m-0 p-0 bg-light" v-if="kind.search('transfer') == -1 && kind != '---'">
                <input type="checkbox" id="checkbox" v-model:value="chk" v-bind="label()">
                <span class="form-text text-muted" style="font-size:9px">update</span>
                </div>


                <div v-if= "kind != '---'" class="form-inline m-0 p-0">
                <button type="submit" class="btn btn-sm m-0 p-0 btn-link" id="button" size="6">{{ method }}</button>
                </div>
            </div>
    `,
    data: function() {
        return {
            method: 'delete',
            edit: true,
            chk: false,
            brkrg: this.brokerage,
            tx_p: this.tx_op,
            knd: this.kind,
            mn: this.money,
            dt: this.date
        }
    },
    methods:{
        n_tx_p: function(event) {
            this.tx_p = event.target.value
        },
        n_brkrg: function(event) {
            this.brkrg = event.target.value
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
        submitForm: function(event) {
            var form = {}
            form["pk"] = event.target.pk.value

            form["tx_op"] = event.target.tx_op.value;
            form["brokerage"] = event.target.brokerage.value;
            form["kind"] = event.target.kind.value;
            form["money"] = Number(event.target.money.value);
            form["date"] = event.target.date.value;

            if ( form['kind'].search('transfer') == -1 && kind != '---' ) {
                event.target.checkbox.checked = false
            }

            http_verb = event.target.button.innerText
            console.log(http_verb)
            http_verb = http_verb == 'delete' ? 'delete' : 'put'

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";

            axios({
                method: http_verb,
                url: 'api/' + form["pk"] + '/',
                data: form
            }).then(response => {
                console.log("HERE")
                if ( http_verb == 'delete') {
                    document.getElementById(form["pk"]).remove()
                }
                // Update line1 data missing
            })
            .catch(function (err) {
                consolelog(err.message);
            })
        }
    }
})
