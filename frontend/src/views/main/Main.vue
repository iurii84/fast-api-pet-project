<template>
  <div>
    <v-navigation-drawer  
      :mini-variant="miniDrawer"
      width="290"
      v-model="showDrawer" 
      fixed 
      app
      >
      <v-layout column fill-height>
        <v-list dense>
          <v-subheader v-if="miniDrawer===false">Main menu</v-subheader>

            <v-list-group
              no-action
              :value="false"
              prepend-icon="home"
            >
              <template v-slot:activator>
                <v-list-item-title>My home</v-list-item-title>
              </template>

              <v-list-item to="/main/dashboard">
                <v-list-item-icon>
                  <v-icon>dashboard</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Dashboard</v-list-item-title>
              </v-list-item>

              <v-list-item to="/main/profile/charts">
                <v-list-item-icon>
                  <v-icon>mdi-chart-line</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Charts</v-list-item-title>
              </v-list-item>

              <v-list-item to="/main/profile/register_device">
                <v-list-item-icon>
                  <v-icon>mdi-devices</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Register device</v-list-item-title>
              </v-list-item>

              <v-list-item to="/main/profile/device_data_bind">
                <v-list-item-icon>
                  <v-icon>mdi-link-variant</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Register databind</v-list-item-title>
              </v-list-item>

              <v-list-item to="/main/profile/compress_db">
                <v-list-item-icon>
                  <v-icon>mdi-arrow-collapse-vertical</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Compress DB</v-list-item-title>
              </v-list-item>

              <v-list-item to="/main/profile/static_display_data">
                <v-list-item-icon>
                  <v-icon>mdi-clipboard-list-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Static Display Data</v-list-item-title>
              </v-list-item>

            </v-list-group>

          

          <v-list-item to="/main/profile/view">
            <v-list-item-icon>
              <v-icon>person</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Profile</v-list-item-title>
          </v-list-item>

          <v-list-item to="/main/profile/edit">
            <v-list-item-icon>
              <v-icon>edit</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Edit profile</v-list-item-title>
          </v-list-item>

          <v-list-item to="/main/profile/password">
            <v-list-item-icon>
              <v-icon>vpn_key</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Change Password</v-list-item-title>
          </v-list-item>

        </v-list>

        <v-divider></v-divider>

        <v-list subheader v-show="hasAdminAccess">
          <v-subheader v-if="miniDrawer===false">Admin</v-subheader>

          <v-list-item to="/main/admin/users/all">
            <v-list-item-icon>
              <v-icon>group</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Manage Users</v-list-item-title>
          </v-list-item>

          <v-list-item to="/main/admin/users/create">
            <v-list-item-icon>
              <v-icon>person_add</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Create User</v-list-item-title>
          </v-list-item>

        </v-list>

        <v-spacer></v-spacer>

        <v-list>
          <v-list-item @click="logout">
            <v-list-item-icon>
              <v-icon>close</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>

        <v-list>
          <v-list-item @click="switchMiniDrawer">
            <v-list-item-icon>
              <v-icon v-html="miniDrawer ? 'chevron_right' : 'chevron_left'"></v-icon>
            </v-list-item-icon>
            <v-list-item-title>Collapse</v-list-item-title>
          </v-list-item>
        </v-list>
    
      </v-layout>
    </v-navigation-drawer>
    <v-toolbar dark color="primary" >
      <v-app-bar-nav-icon @click.stop="switchShowDrawer">
        <v-icon>menu</v-icon>
      </v-app-bar-nav-icon>
      <v-toolbar-title v-text="appName"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-menu bottom left offset-y>
        <template v-slot:activator="{ on}">
          <v-btn
            dark
            icon
            v-on="on"
          >
            <v-icon>more_vert</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item to="/main/profile">
            <v-list-item-title>Profile</v-list-item-title>
            <v-list-item-icon>
              <v-icon>person</v-icon>
            </v-list-item-icon>
          </v-list-item>

          <v-list-item @click="logout">
            <v-list-item-title>Logout</v-list-item-title>
            <v-list-item-icon>
              <v-icon>close</v-icon>
            </v-list-item-icon>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-toolbar>
    <v-main>
      <router-view></router-view>
    </v-main>
    <v-footer class="pa-3" fixed app>
      <v-spacer></v-spacer>
      <span>&copy; {{appName}}</span>
    </v-footer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

import { appName } from '@/env';
import { readDashboardMiniDrawer, readDashboardShowDrawer, readHasAdminAccess } from '@/store/main/getters';
import { commitSetDashboardShowDrawer, commitSetDashboardMiniDrawer } from '@/store/main/mutations';
import { dispatchUserLogOut } from '@/store/main/actions';

const routeGuardMain = async (to, from, next) => {
  if (to.path === '/main') {
    next('/main/dashboard');
  } else {
    next();
  }
};

@Component
export default class Main extends Vue {
  public appName = appName;

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }

  get miniDrawer() {
    return readDashboardMiniDrawer(this.$store);
  }

  get showDrawer() {
    return readDashboardShowDrawer(this.$store);
  }

  set showDrawer(value) {
    commitSetDashboardShowDrawer(this.$store, value);
  }

  public switchShowDrawer() {
    commitSetDashboardShowDrawer(
      this.$store,
      !readDashboardShowDrawer(this.$store),
    );
  }

  public switchMiniDrawer() {
    commitSetDashboardMiniDrawer(
      this.$store,
      !readDashboardMiniDrawer(this.$store),
    );
  }

  public get hasAdminAccess() {
    return readHasAdminAccess(this.$store);
  }

  public async logout() {
    await dispatchUserLogOut(this.$store);
  }
}
</script>
