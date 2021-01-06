<template>
  <v-container>
    <v-card width="320" class="mx-auto" outlined>
      <v-card-title class="justify-center pb-0">Entrar</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            v-model="email"
            label="E-mail"
            prepend-icon="mdi-account"
            autocomplete="off"
          >
          </v-text-field>
          <v-text-field
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            label="Senha"
            autocomplete="off"
            @click:append="showPassword = !showPassword"
            @keyup.enter.prevent="login"
          ></v-text-field>
        </v-form>
        <v-card-actions>
          <v-btn color="accent" @click.prevent="login">{{ labelButton }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="accent" outlined to="/cadastrar" nuxt>
            Criar conta
          </v-btn>
        </v-card-actions>
      </v-card-text>
    </v-card>
    <v-snackbar
      v-model="snackbar"
      width="50%"
      :timeout="timeout"
      color="accent"
      bottom
      left
    >
      {{ text }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar = false"> OK </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { mapGetters, mapState } from 'vuex'

export default {
  middleware: ['isAuthenticated'],
  data: () => ({
    labelButton: 'Entrar',
    showPassword: false,
    email: '',
    password: '',
    snackbar: false,
    text: 'Conta ativa!',
    timeout: 2000,
  }),
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
    ...mapState('auth', ['show_welcome_login']),
  },
  created() {
    if (this.show_welcome_login) {
      this.snackbar = true
      this.$store.commit('auth/SHOW_WELCOME_LOGIN', false)
    }
  },
  methods: {
    login() {
      this.labelButton = 'Carregando'
      this.$store
        .dispatch('auth/login', {
          username: this.email,
          password: this.password,
        })
        .then(() => {
          this.labelButton = 'Pronto'
          this.$router.push('/projetos')
        })
        .catch((e) => {
          console.log(e)
          this.labelButton = 'Falhou...'
        })
    },
  },
}
</script>
