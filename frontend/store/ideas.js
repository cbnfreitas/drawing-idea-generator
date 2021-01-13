export const state = () => ({
  idea: null,
})

export const getters = {}

export const mutations = {
  SET_IDEA(state, data) {
    state.idea = data
  },
  RESET_IDEA(state) {
    state.idea = null
  },
}

export const actions = {
  getIdea({ commit }) {
    return this.$axios
      .$get('/ideas')
      .then((response) => {
        commit('SET_IDEA', response.detail)
      })
      .catch((e) => {
        console.log(e)
        throw e
      })
  },
}
