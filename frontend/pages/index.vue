<template>
  <v-container>
    <v-card class="mx-auto" outlined>
      <v-card-title class="justify-center pb-0"
        >Qual o meu ranking no Google Brasil?
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="urlToFind"
                  prepend-icon="mdi-home-outline"
                  label="URL do site"
                  autocomplete="off"
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="terms"
                  prepend-icon="mdi-search-web"
                  label="Palavra-chave"
                  dense
                  autocomplete="off"
                  @keyup.enter.prevent="submit"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row align="center" dense>
              <v-col class="text-center" cols="12" sm="6">
                <v-checkbox
                  v-show="false"
                  v-model="isCity"
                  shrink
                  label="Por cidade"
                ></v-checkbox>
              </v-col>
              <v-col class="text-center" cols="12" sm="6">
                <v-btn
                  color="primary"
                  :loading="!showButton"
                  :disabled="!showButton"
                  @click="submit"
                  >Buscar
                  <template v-slot:loader>
                    <v-progress-circular indeterminate></v-progress-circular>
                  </template>
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
    </v-card>
    <v-card
      v-show="showButton && !before_first_result"
      class="mx-auto"
      outlined
    >
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6">
              <v-alert
                :type="alert_type"
                class="center"
                outlined
                max-width="320px"
                >{{ result }}</v-alert
              >
              <a :href="meme" target="_blank" style="text-decoration: none">
                <v-img :src="meme" class="center" width="320px" />
                <v-img
                  class="center"
                  src="https://cdn.worldvectorlogo.com/logos/giphy-logo.svg"
                  width="75px"
                />
              </a>
            </v-col>
            <v-col cols="12" sm="6">
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">Rank</th>
                      <th class="text-left">Site</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in links" :key="item.link">
                      <td>{{ item.index }}</td>
                      <td>
                        <a
                          :href="item.link"
                          style="text-decoration: none"
                          target="_blank"
                        >
                          {{ item.link }}
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-col>
          </v-row>
        </v-container>
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
    ...mapState('rank', ['contains', 'rank', 'links', 'meme']),
    alert_type() {
      if (this.contains) {
        if (this.rank <= 10) {
          return 'success'
        } else {
          return 'warning'
        }
      } else {
        return 'error'
      }
    },
    result() {
      if (this.before_first_result) {
        return ''
      }
      if (this.contains) {
        return 'Posição ' + this.rank
      } else {
        return 'Fora do top 100'
      }
    },
  },

  methods: {
    submit() {
      this.showButton = false
      this.$store.commit('rank/RESET_CONTAINS_AND_RANK_LIST')

      this.$store
        .dispatch('rank/findRank', {
          terms: this.terms,
          urlToFind: this.urlToFind,
          isCity: this.isCity,
        })
        .then(() => {
          this.before_first_result = false
          this.showButton = true
        })
        .catch((e) => {
          console.log(e)
          this.before_first_result = false
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
