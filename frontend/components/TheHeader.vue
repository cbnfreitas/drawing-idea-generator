<template>
  <v-toolbar color="transparent" flat>
    <v-toolbar-title>
      <nuxt-link to="/" style="text-decoration: none" class="white--text">
        MeuRanking
      </nuxt-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn
      v-for="link in links"
      :key="`${link.label}-header-link`"
      color="white"
      text
      rounded
      :to="link.url"
      >{{ link.label }}</v-btn
    >
    <v-btn v-show="!isAuthenticated" color="white" text rounded to="/login">
      Entrar
    </v-btn>
    <v-btn
      v-show="isAuthenticated"
      color="white"
      text
      rounded
      @click.prevent="logout"
    >
      Logout
    </v-btn>
  </v-toolbar>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'TheHeader',
  data: () => ({
    visible: false,
    links: [{ url: '/projetos', label: 'Projetos' }],
  }),
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
  },
  methods: {
    logout() {
      this.$store
        .dispatch('auth/logout')
        .then(() => {
          this.$router.push('/')
        })
        .catch((e) => {
          console.log(e)
          this.labelButton = 'Falhou...'
        })
    },
  },
}
</script>
