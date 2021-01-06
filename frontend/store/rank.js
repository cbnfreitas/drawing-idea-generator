export const state = () => ({
  contains: null,
  rank: null,
  links: null,
  meme: null,
})

export const getters = {}

export const mutations = {
  SET_CONTAINS_AND_RANK_AND_LIST(state, data) {
    state.contains = data.contains
    if (data.contains) {
      state.rank = data.rank
    } else {
      state.rank = null
    }
    state.links = data.links
    state.meme = data.meme
  },
  RESET_CONTAINS_AND_RANK_LIST(state) {
    state.contains = null
    state.rank = null
    state.links = null
    state.meme = null
  },
}

export const actions = {
  findRank({ commit }, data) {
    const json = {
      terms: data.terms,
      url_to_find: data.urlToFind,
      is_city: data.isCity,
    }

    return this.$axios
      .$post('/find_rank', json)
      .then((response) => {
        commit('SET_CONTAINS_AND_RANK_AND_LIST', response)
      })
      .catch((e) => {
        console.log(e)
        throw e
      })
  },
}
