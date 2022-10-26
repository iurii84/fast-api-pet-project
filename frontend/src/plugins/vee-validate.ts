import Vue from 'vue';
import VeeValidate from 'vee-validate';

// name conflict resolution
const config = {
    errorBagName: 'veeErrors', // change if property conflicts.
    fieldsBagName: 'veeFields',
};
Vue.use(VeeValidate, config);
