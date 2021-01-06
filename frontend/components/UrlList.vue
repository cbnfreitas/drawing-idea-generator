<template>
  <v-container>
    <v-card width="100%" class="mx-auto" outlined>
      <v-card-title>
        Domínios &nbsp;
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
                      v-model="editedDomain.url"
                      label="URL do site"
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
      </v-card-title>

      <v-expansion-panels v-model="panel" multiple width="100%">
        <v-expansion-panel v-for="(domain, index) in domains" :key="domain.id">
          <v-expansion-panel-header>
            <div>
              {{ domain.url }}
              <!-- <v-icon small @click.native.stop="editDomain(domain)">
              mdi-pencil
            </v-icon>
            -->
              &nbsp;
              <v-icon small @click.native.stop="deleteDomain(domain)">
                mdi-delete
              </v-icon>
              <v-dialog v-model="dialog2" width="320">
                <v-card>
                  <v-card-title class="headline"
                    >Apagar "{{ domain_url_to_be_deleted }}"?</v-card-title
                  >
                  <v-card-text>
                    CUIDADO: Todas as palavra-chaves e ranks também serão
                    excluídos!
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="accent" text @click="deleteDomainYes()">
                      Sim
                    </v-btn>
                    <v-btn color="accent" @click="dialog2 = false"> Não </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </div>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <UrlRow :domain-index="index" :domain-id="domain.id"></UrlRow>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'
import UrlRow from '@/components/UrlRow'
export default {
  components: {
    UrlRow,
  },
  data: () => ({
    panel: [0],
    domain_url_to_be_deleted: '',
    domain_id_to_be_deleted: '',
    dialog: false,
    dialog2: false,
    editedIndex: -1,
    editedDomain: {
      url: '',
    },
    defaulDomain: {
      url: '',
    },
  }),
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'Novo Domínio' : 'Editar Domínio'
    },
    ...mapState('domains', ['domains']),
  },
  watch: {
    dialog(val) {
      val || this.close()
    },
  },
  methods: {
    editDomain(domain) {
      this.editedIndex = this.domains.indexOf(domain)
      this.editedDomain = Object.assign({}, domain)
      this.dialog = true
    },
    deleteDomain(domain) {
      this.dialog2 = true
      this.domain_url_to_be_deleted = domain.url
      this.domain_id_to_be_deleted = domain.id
    },
    deleteDomainYes() {
      this.dialog2 = false
      this.$store.dispatch('domains/deleteDomain', this.domain_id_to_be_deleted)
    },
    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedDomain = Object.assign({}, this.defaulDomain)
        this.editedIndex = -1
      })
    },
    save() {
      if (this.editedIndex > -1) {
        this.$store.dispatch('domains/updateDomain', {
          id: this.editedDomain.id,
          url: this.editedDomain.url,
        })
      } else {
        this.$store.dispatch('domains/createDomain', {
          url: this.editedDomain.url,
        })
      }
      this.close()
    },
  },
}
</script>
