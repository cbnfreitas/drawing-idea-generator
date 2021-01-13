<template>
  <v-container>
    <v-card class="mx-auto" outlined>
      <v-card-title class="justify-center pb-0">O que desenhar? </v-card-title>
      <v-card-text>
        <p>{{ idea }}</p>
        <v-btn
          color="primary"
          :loading="!showButton"
          :disabled="!showButton"
          @click="submit"
          >Gerar
          <template v-slot:loader>
            <v-progress-circular indeterminate></v-progress-circular>
          </template>
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data: () => ({
    showButton: true,
    terms: '',
    urlToFind: '',
    isCity: true,
    before_first_result: true,
  }),
  computed: {
    ...mapState('ideas', ['idea']),
  },
  methods: {
    submit() {
      this.showButton = false
      this.$store.commit('ideas/RESET_IDEA')

      this.$store
        .dispatch('ideas/getIdea')
        .then(() => {
          this.showButton = true
        })
        .catch((e) => {
          console.log(e)
          this.showButton = true
        })
    },
  },
}
</script>

<style scoped>
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
</style>
