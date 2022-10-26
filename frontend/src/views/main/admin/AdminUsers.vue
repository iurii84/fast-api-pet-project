<template>
 <v-card class="ma-5 pa-5">
    <v-card-title primary-title>
      <div class="headline primary--text">Manage Users</div>
    </v-card-title>
    <v-spacer></v-spacer>
    <v-btn color="primary" to="/main/admin/users/create">Create User</v-btn>
    <v-data-table :headers="headers" :items="users">
      <template v-slot:item.is_active="{ item }" >
        <v-icon v-if=item.is_active>checkmark</v-icon> 
      </template>

      <template v-slot:item.is_superuser="{ item }" >
        <v-icon v-if=item.is_superuser>checkmark</v-icon> 
      </template>

    </v-data-table>
 </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import { readAdminUsers } from '@/store/admin/getters';
import { dispatchGetUsers } from '@/store/admin/actions';

@Component
export default class AdminUsers extends Vue {
  public headers = [
   {
      text: 'ID',
      value: 'id',
    },
    {
      text: 'Name',
      sortable: true,
      value: 'full_name',
      align: 'left',
    },
    {
      text: 'Email',
      sortable: true,
      value: 'email',
      align: 'left',
    },

    {
      text: 'Is Active',
      sortable: true,
      value: 'is_active',
      align: 'left',
    },
    {
      text: 'Is Superuser',
      sortable: true,
      value: 'is_superuser',
      align: 'left',
    },

  ];
  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }
}
</script>
