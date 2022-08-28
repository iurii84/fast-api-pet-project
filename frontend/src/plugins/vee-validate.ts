import Vue from 'vue';
import VeeValidate from 'vee-validate';

// name conflict resolution
const config = {
    errorBagName:'errorBags',//change if property conflicts.
    fieldsBagName:'fieldBags',
};
Vue.use(VeeValidate, config);
