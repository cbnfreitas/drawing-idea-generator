<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="keywords"
      sort-by="keyword"
      :disable-pagination="true"
      :hide-default-footer="true"
      :mobile-breakpoint="0"
    >
      <template v-slot:header.keyword>
        Palavra-chave &nbsp;
        <v-dialog v-model="dialog" max-width="320px">
          <template v-slot:activator="{ on }">
            <v-icon v-on="on"> mdi-plus-circle-outline </v-icon>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col>
                    <v-text-field
                      v-model="editedKeyword.keyword"
                      label="Palavra-chave"
                      @keyup.enter="save"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn color="accent" text @click="close"> Cancelar </v-btn>
              <v-btn color="accent" @click="save"> Salvar </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
      <template v-slot:item.keyword="{ item }">
        <div></div>
        {{ item.keyword }} &nbsp;
        <v-icon small @click="deleteKeyword(item)"> mdi-delete </v-icon>
        <v-dialog v-model="dialog2" width="320">
          <v-card>
            <v-card-title class="headline"
              >Apagar "{{ keyword_to_be_deleted }}"?</v-card-title
            >
            <v-card-text>
              CUIDADO: Todos os ranks também serão excluídos!
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="accent" text @click="deleteKeywordYes()">
                Sim
              </v-btn>
              <v-btn color="accent" @click="dialog2 = false"> Não </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>

      <template v-slot:item.last_rank="{ item }">
        <div v-if="item.last_rank <= 100">{{ item.last_rank }} &nbsp;</div>
        <div v-if="item.last_rank > 100">100+</div>
      </template>
      <template v-slot:no-data> Nenhuma palavra-chave. </template>
    </v-data-table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    domainIndex: {
      type: Number,
      required: true,
    },
    domainId: {
      type: Number,
      required: true,
    },
  },
  data: () => ({
    dialog: false,
    dialog2: false,
    headers: [
      {
        text: 'Palavras-chave',
        sortable: false,
        value: 'keyword',
        width: '150px',
      },
      {
        text: 'Rank',
        value: 'last_rank',
        width: '60px',
        align: 'center',
        class: 'pa-2',
      },
      {
        text: '',
        value: 'last_rank_date',
        sortable: false,
        width: '16px',
        align: 'center',
      },
    ],
    keyword_to_be_deleted: '',
    keyword_id_to_be_deleted: '',
    editedIndex: -1,
    editedKeyword: {
      keyword: '',
    },
    defaulKeyword: {
      name: '',
    },
  }),
  computed: {
    formTitle() {
      return this.editedIndex === -1
        ? 'Nova Palavra-chave'
        : 'Editar Palavra-chave'
    },
    ...mapGetters('domains', ['domains_rank_friendly']),
    keywords() {
      return this.domains_rank_friendly[this.domainIndex].keywords
    },
  },
  watch: {
    dialog(val) {
      val || this.close()
    },
  },
  methods: {
    editKeyword(keyword) {
      this.editedIndex = this.keywords.indexOf(keyword)
      this.editedKeyword = Object.assign({}, keyword)
      this.dialog = true
    },
    deleteKeyword(keyword) {
      this.dialog2 = true
      this.keyword_to_be_deleted = keyword.keyword
      this.keyword_id_to_be_deleted = keyword.id
    },
    deleteKeywordYes() {
      this.dialog2 = false
      const data = {
        keywordId: this.keyword_id_to_be_deleted,
        domainId: this.domainId,
      }
      this.$store.dispatch('domains/deleteKeyword', data)
    },
    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedKeyword = Object.assign({}, this.defaultKeyword)
        this.editedIndex = -1
      })
    },
    save() {
      if (this.editedIndex > -1) {
        console.log('edited!!!!!!!!!!')
        this.$store.dispatch('domains/updateKeyword', {
          id: this.editedKeyword.id,
          domainId: this.domainId,
          keyword: this.editedKeyword.keyword,
        })
      } else {
        this.$store.dispatch('domains/createKeyword', {
          domainId: this.domainId,
          keyword: this.editedKeyword.keyword,
        })
      }
      this.close()
    },
  },
}
</script>

<style>
.v-data-table-header__icon {
  opacity: 0.5;
}
.v-data-table-header th {
  white-space: nowrap;
}
</style>
