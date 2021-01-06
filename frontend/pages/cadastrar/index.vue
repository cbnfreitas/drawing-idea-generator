<template>
  <v-container>
    <v-card width="320" class="mx-auto" outlined>
      <v-card-title class="justify-center pb-0"
        >Preencha seus dados</v-card-title
      >
      <v-card-text>
        <v-form v-model="valid" :disabled="isDisabled">
          <v-text-field
            v-model="name"
            label="Nome*"
            prepend-icon="mdi-account"
            required
            autocomplete="off"
            :rules="nameRules"
          >
          </v-text-field>
          <v-text-field
            v-model="email"
            label="E-mail*"
            prepend-icon="mdi-email"
            autocomplete="off"
            :rules="emailRules"
            validate-on-blur
          >
          </v-text-field>
          <v-text-field
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            label="Senha*"
            autocomplete="off"
            required
            :rules="passwordRules"
            @click:append="showPassword = !showPassword"
            @keyup.enter.prevent="register"
          >
          </v-text-field>
        </v-form>
        <v-card-actions class="justify-center">
          <v-btn
            color="accent"
            :disabled="isDisabled"
            @click.prevent="register"
            >{{ labelButton }}</v-btn
          >
        </v-card-actions>
      </v-card-text>
    </v-card>
    <v-snackbar
      v-model="snackbar"
      width="50%"
      :timeout="timeout"
      color="primary"
      bottom
      left
    >
      Confirme sua conta através do e-mail enviado para {{ email }}.
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar = false"> OK </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { mapGetters, mapState } from 'vuex'

export default {
  data: () => ({
    snackbar: false,
    timeout: 10000,
    labelButton: 'Registrar',
    isDisabled: false,
    showPassword: false,
    name: '',
    email: '',
    password: '',
    valid: false,
    nameRules: [(v) => !!v || 'Nome precisa ser preenchido.'],
    emailRules: [
      (v) => !!v || 'E-mail obrigatório',
      (v) => /.+@.+/.test(v) || 'E-mail precisa ser preenchido.',
    ],
    passwordRules: [
      (v) => !!v || 'Senha obrigatória.',
      (v) =>
        (v && v.length >= 5) || 'Senha precisa ter no mínimo 5 caracteres.',
    ],
  }),
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
    ...mapState('auth', ['access_token']),
  },
  watch: {
    snackbar(newSnackBar, oldSnackBar) {
      if (newSnackBar === false && oldSnackBar === true) {
        this.$router.push('/')
      }
    },
  },
  methods: {
    register() {
      this.labelButton = '...'
      this.$store
        .dispatch('auth/register', {
          name: this.name,
          email: this.email,
          password: this.password,
        })
        .then(() => {
          this.labelButton = 'Feito!'
          this.isDisabled = true
          this.snackbar = true
        })
        .catch((e) => {
          console.log(e)
          this.labelButton = 'Falhou...'
        })
    },
  },
}
</script>
