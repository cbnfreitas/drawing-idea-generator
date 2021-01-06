export const state = () => ({
  show_welcome_login: false,
  access_token: localStorage.getItem('access_token') || null,
})

export const getters = {
  isAuthenticated: (state) => !!state.access_token,
}

export const mutations = {
  SET_ACCESS_TOKEN(state, data) {
    state.access_token = data
    if (data) {
      localStorage.setItem('access_token', data)
    } else {
      localStorage.removeItem('access_token')
    }
  },

  SHOW_WELCOME_LOGIN(state, data) {
    state.show_welcome_login = data
  },
}

export const actions = {
  login({ commit, dispatch }, data) {
    const params = new URLSearchParams()
    params.append('username', data.username)
    params.append('password', data.password)

    return this.$axios
      .$post('/auth/login', params)
      .then((response) => {
        commit('SET_ACCESS_TOKEN', response.access_token)
        this.dispatch('domains/readDomains')
      })
      .catch((e) => {
        console.log(e)
        throw e
      })
  },

  register({ commit, dispatch }, data) {
    const json = {
      full_name: data.name,
      email: data.email,
      password: data.password,
    }
    return (
      this.$axios
        .$post('/auth/register', json)
        // .then((response) => { })
        .catch((e) => {
          console.log(e)
          throw e
        })
    )
  },

  activate({ commit, dispatch }, data) {
    const json = {
      activation_token: data.activation_token,
    }
    return this.$axios
      .$post('/auth/activation', json)
      .then((response) => {
        commit('SHOW_WELCOME_LOGIN', true)
      })
      .catch((e) => {
        console.log(e)
        throw e
      })
  },

  logout({ commit, dispatch }, data) {
    commit('SET_ACCESS_TOKEN', null)
    this.commit('domains/SET_DOMAINS')
  },
}
