<template>
  <v-container> </v-container>
</template>

<script>
export default {
  middleware(context) {
    context.store
      .dispatch('auth/activate', {
        activation_token: context.route.params.token,
      })
      .then(() => {
        context.redirect('/login')
      })
      .catch((e) => {
        console.log(e)
        console.log('Falhou...')
        context.redirect('/login')
      })
  },
}
</script>
