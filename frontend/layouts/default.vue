<template>
  <v-app>
    <v-app-bar app flat color="primary">
      <template v-slot:img="{ props }">
        <v-img
          v-bind="props"
          gradient="to top right, rgba(106,39,154,1), rgba(137,29,173,1)"
        ></v-img>
      </template>
      <TheHeader />
    </v-app-bar>
    <v-main max-width="600" min-width="320">
      <nuxt />
    </v-main>
    <v-footer app height="50px">
      <TheLogo />
    </v-footer>
  </v-app>
</template>

<script>
import TheHeader from '@/components/TheHeader'
import TheLogo from '@/components/TheLogo'
import { mapGetters } from 'vuex'

export default {
  components: {
    TheHeader,
    TheLogo,
  },
  transition: 'default',
  data: () => ({}),
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
  },
  created() {
    if (this.isAuthenticated) {
      this.$store
        .dispatch('domains/readDomains')
        // .then(() => {})
        .catch((e) => {
          console.log(e)
          console.log('Error!')
        })
    } else {
      // console.log('não autenticado')
    }
  },
}
</script>
