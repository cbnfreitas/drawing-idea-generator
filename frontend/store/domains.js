export const state = () => ({
  domains: [],
})

export const getters = {
  domains_rank_friendly(state) {
    return state.domains.map((domain) => {
      const infoDomain = {
        id: domain.id,
        url: domain.url,
        keywords: domain.keywords.map((keyword) => {
          let lastRank
          let lastRankDate

          if (!keyword.last_rank_date) {
            lastRankDate = '-'
            lastRank = '-'
          } else {
            // const dif = difDaysZeroHour(keyword.last_rank_date)
            // console.log(dif)
            // if (dif === 0) {
            //   lastRankDate = 'Hoje'
            // } else if (dif === 1) {
            //   lastRankDate = 'Ontem'
            // } else {
            //   lastRankDate = 'Hoje'
            // }

            lastRankDate = 'Hoje'
            lastRank = keyword.last_rank || ':-('
          }

          const infoKeyword = {
            id: keyword.id,
            keyword: keyword.keyword,
            last_rank: lastRank,
            last_rank_date: lastRankDate,
          }
          return infoKeyword
        }),
      }
      return infoDomain
    })
  },
}

export const mutations = {
  SET_DOMAINS(state, data) {
    state.domains = data
  },

  ADD_DOMAIN(state, domain) {
    state.domains.push(domain)
  },

  REMOVE_DOMAIN(state, domainId) {
    state.domains = state.domains.filter((obj) => obj.id !== domainId)
  },

  REPLACE_DOMAIN(state, domain) {
    const editedDomainIndex = state.domains
      .map((e) => {
        return e.id
      })
      .indexOf(domain.id)
    Object.assign(state.domains[editedDomainIndex], domain)
  },

  ADD_KEYWORD(state, data) {
    const editedDomainIndex = state.domains
      .map((e) => {
        return e.id
      })
      .indexOf(data.domain_id)

    state.domains[editedDomainIndex].keywords.push(data)
  },

  REPLACE_KEYWORD(state, keyword) {
    const editedDomainIndex = state.domains
      .map((e) => {
        return e.id
      })
      .indexOf(keyword.domain_id)

    const editedKeywordIndex = state.domains[editedDomainIndex].keywords
      .map((e) => {
        return e.id
      })
      .indexOf(keyword.id)

    Object.assign(
      state.domains[editedDomainIndex].keywords[editedKeywordIndex],
      keyword
    )
  },

  REMOVE_KEYWORD(state, data) {
    console.log(data)
    const editedDomainIndex = state.domains
      .map((e) => {
        return e.id
      })
      .indexOf(data.domainId)

    state.domains[editedDomainIndex].keywords = state.domains[
      editedDomainIndex
    ].keywords.filter((obj) => obj.id !== data.keywordId)
  },
}

export const actions = {
  readDomains({ commit }, data) {
    return this.$axios
      .$get('/domains', {
        headers: { authorization: 'Bearer ' + this.state.auth.access_token },
      })
      .then((response) => {
        commit('SET_DOMAINS', response)
      })
      .catch((e) => {
        console.log(e)
        throw e
      })
  },

  // DOMAINS
  createDomain({ commit }, data) {
    const json = {
      url: data.url,
    }

    return this.$axios
      .$post('/domains', json, {
        headers: { authorization: 'Bearer ' + this.state.auth.access_token },
      })
      .then((response) => {
        commit('ADD_DOMAIN', response)
      })
      .catch((e) => {
        console.log(e)
        throw e
      })
  },

  // updateDomain({ commit }, data) {
  //   const json = {
  //     url: data.url,
  //   }

  //   return this.$axios
  //     .$put('/domains/' + data.id, json)
  //     .then((response) => {
  //       commit('REPLACE_DOMAIN', response)
  //     })
  //     .catch((e) => {
  //       console.log(e)
  //       throw e
  //     })
  // },

  deleteDomain({ commit }, domainId) {
    return this.$axios
      .$delete('/domains/' + domainId, {
        headers: { authorization: 'Bearer ' + this.state.auth.access_token },
      })
      .then((response) => {
        commit('REMOVE_DOMAIN', domainId)
      })
      .catch((e) => {
        console.log(e)
        throw e
      })
  },

  // Keywords
  createKeyword({ commit }, data) {
    const json = {
      keyword: data.keyword,
      domain_id: data.domainId,
    }

    return this.$axios
      .$post('/keywords', json, {
        headers: { authorization: 'Bearer ' + this.state.auth.access_token },
      })
      .then((response) => {
        commit('ADD_KEYWORD', response)
      })
      .catch((e) => {
        console.log(e)
        throw e
      })
  },

  // updateKeyword({ commit }, data) {
  //   const json = {
  //     keyword: data.keyword,
  //     domain_id: data.domainId,
  //   }

  //   console.log(json)

  //   return this.$axios
  //     .$put('/keywords/' + data.id, json)
  //     .then((response) => {
  //       commit('REPLACE_KEYWORD', response)
  //     })
  //     .catch((e) => {
  //       console.log(e)
  //       throw e
  //     })
  // },

  deleteKeyword({ commit }, data) {
    return this.$axios
      .$delete('/keywords/' + data.keywordId, {
        headers: { authorization: 'Bearer ' + this.auth.state.access_token },
      })
      .then((response) => {
        commit('REMOVE_KEYWORD', data)
      })
      .catch((e) => {
        console.log(e)
        throw e
      })
  },
}
